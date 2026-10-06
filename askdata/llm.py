"""Fournisseurs de modeles derriere une interface commune.

L'agent ne connait que Session.envoyer et Session.renvoyer. Chaque
fournisseur garde l'historique dans son propre format et ne fait que
l'allonger : on n'edite jamais un tour deja envoye, ce qui garde le cache de
prompt valide et respecte les blocs de raisonnement que certains modeles
renvoient.

Trois fournisseurs :
- anthropic  API Messages, SDK officiel ;
- openai     Chat Completions, SDK officiel ;
- rejeu      relit des reponses deja produites (fichier JSONL). Sert aux
             tests, et a noter des sorties obtenues hors de ce harnais.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from .jeu import id_opaque
from .prompt import Outil


@dataclass
class Usage:
    entree: int = 0
    sortie: int = 0
    cache_lecture: int = 0
    cache_ecriture: int = 0
    appels: int = 0

    def __add__(self, autre: "Usage") -> "Usage":
        return Usage(
            self.entree + autre.entree,
            self.sortie + autre.sortie,
            self.cache_lecture + autre.cache_lecture,
            self.cache_ecriture + autre.cache_ecriture,
            self.appels + autre.appels,
        )


@dataclass
class Appel:
    id: str
    nom: str
    arguments: dict


@dataclass
class Tour:
    texte: str
    appels: list[Appel]
    arret: str          # outil | fin | refus | max_tokens | autre
    usage: Usage


@dataclass
class ResultatOutil:
    id: str
    contenu: str
    erreur: bool = False


class Session(Protocol):
    def envoyer(self, texte: str) -> Tour: ...
    def renvoyer(self, resultats: list[ResultatOutil]) -> Tour: ...


class Fournisseur(Protocol):
    nom: str
    modele: str
    def ouvrir(self, systeme: str, outils: list[Outil], etiquette: str) -> Session: ...


# Prix publics en dollars par million de jetons : entree, sortie, lecture de
# cache. L'ecriture en cache coute 1,25 fois l'entree. Un modele absent de la
# table n'a pas de cout affiche, plutot qu'un cout invente.
PRIX = {
    "claude-opus-5-5": (4.00, 20.00, 0.20),
    "claude-sonnet-5-5": (2.00, 10.00, 0.20),
    "claude-haiku-4-5": (1.00, 5.00, 0.10),
}


def cle_api(nom: str) -> str | None:
    """La cle d'API, prise dans l'environnement du processus, ou a defaut dans
    l'environnement utilisateur Windows.

    Le second cas couvre un terminal ouvert avant que la cle soit enregistree
    (setx), ou par une application lancee avant : la variable existe pour
    l'utilisateur mais pas dans ce processus. Renvoie None si elle n'existe
    nulle part ; le SDK cherche alors ses autres sources d'identification.
    """
    valeur = os.environ.get(nom)
    if valeur or os.name != "nt":
        return valeur or None
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as cle:
            valeur, _ = winreg.QueryValueEx(cle, nom)
    except OSError:
        return None
    return valeur or None


def cout(modele: str, u: Usage) -> float | None:
    if modele not in PRIX:
        return None
    entree, sortie, lecture = PRIX[modele]
    return (u.entree * entree + u.sortie * sortie + u.cache_lecture * lecture
            + u.cache_ecriture * entree * 1.25) / 1e6


# ---------------------------------------------------------------------------
# Anthropic
# ---------------------------------------------------------------------------

class SessionAnthropic:
    ARRETS = {"tool_use": "outil", "end_turn": "fin", "refusal": "refus",
              "max_tokens": "max_tokens"}

    def __init__(self, client, modele, systeme, outils, effort):
        self.client = client
        self.modele = modele
        # Le prompt systeme (schema compris) est identique pour toutes les
        # questions d'un run : on le met en cache.
        self.systeme = [{"type": "text", "text": systeme,
                         "cache_control": {"type": "ephemeral"}}]
        self.outils = [{"name": o.nom, "description": o.description,
                        "input_schema": o.schema, "strict": True} for o in outils]
        self.effort = effort
        self.messages: list[dict] = []

    def _appeler(self) -> Tour:
        options = {"output_config": {"effort": self.effort}} if self.effort else {}
        r = self.client.messages.create(
            model=self.modele,
            max_tokens=16_000,
            system=self.systeme,
            tools=self.outils,
            messages=self.messages,
            **options,
        )
        self.messages.append({"role": "assistant", "content": r.content})
        u = r.usage
        usage = Usage(u.input_tokens, u.output_tokens,
                      u.cache_read_input_tokens or 0,
                      u.cache_creation_input_tokens or 0, 1)
        texte = "".join(b.text for b in r.content if b.type == "text")
        appels = [Appel(b.id, b.name, dict(b.input)) for b in r.content
                  if b.type == "tool_use"]
        return Tour(texte, appels, self.ARRETS.get(r.stop_reason, "autre"), usage)

    def envoyer(self, texte: str) -> Tour:
        self.messages.append({"role": "user", "content": texte})
        return self._appeler()

    def renvoyer(self, resultats: list[ResultatOutil]) -> Tour:
        self.messages.append({"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": r.id, "content": r.contenu,
             "is_error": r.erreur} for r in resultats]})
        return self._appeler()


class FournisseurAnthropic:
    nom = "anthropic"

    def __init__(self, modele: str = "claude-opus-5-5", effort: str | None = None, client=None):
        if client is None:
            import anthropic
            client = anthropic.Anthropic(max_retries=4,
                                         api_key=cle_api("ANTHROPIC_API_KEY"))
        self.client = client
        self.modele = modele
        # Haiku 4.5 ne prend pas le parametre effort.
        self.effort = effort if not modele.startswith("claude-haiku") else None

    def ouvrir(self, systeme, outils, etiquette) -> SessionAnthropic:
        return SessionAnthropic(self.client, self.modele, systeme, outils, self.effort)


# ---------------------------------------------------------------------------
# OpenAI
# ---------------------------------------------------------------------------

class SessionOpenAI:
    ARRETS = {"tool_calls": "outil", "stop": "fin", "length": "max_tokens",
              "content_filter": "refus"}

    def __init__(self, client, modele, systeme, outils):
        self.client = client
        self.modele = modele
        self.outils = [{"type": "function", "function": {
            "name": o.nom, "description": o.description,
            "parameters": o.schema, "strict": True}} for o in outils]
        self.messages: list[dict] = [{"role": "system", "content": systeme}]

    def _appeler(self) -> Tour:
        r = self.client.chat.completions.create(
            model=self.modele, messages=self.messages, tools=self.outils)
        choix = r.choices[0]
        m = choix.message
        appels_bruts = m.tool_calls or []
        self.messages.append({
            "role": "assistant",
            "content": m.content,
            **({"tool_calls": [{"id": a.id, "type": "function",
                                "function": {"name": a.function.name,
                                             "arguments": a.function.arguments}}
                               for a in appels_bruts]} if appels_bruts else {}),
        })
        appels = []
        for a in appels_bruts:
            try:
                arguments = json.loads(a.function.arguments)
            except json.JSONDecodeError:
                arguments = {"_json_invalide": a.function.arguments}
            appels.append(Appel(a.id, a.function.name, arguments))
        u = r.usage
        details = getattr(u, "prompt_tokens_details", None)
        en_cache = (getattr(details, "cached_tokens", 0) or 0) if details else 0
        usage = Usage(u.prompt_tokens - en_cache, u.completion_tokens, en_cache, 0, 1)
        return Tour(m.content or "", appels, self.ARRETS.get(choix.finish_reason, "autre"), usage)

    def envoyer(self, texte: str) -> Tour:
        self.messages.append({"role": "user", "content": texte})
        return self._appeler()

    def renvoyer(self, resultats: list[ResultatOutil]) -> Tour:
        for r in resultats:
            self.messages.append({"role": "tool", "tool_call_id": r.id, "content": r.contenu})
        return self._appeler()


class FournisseurOpenAI:
    nom = "openai"

    def __init__(self, modele: str, client=None):
        if client is None:
            import openai
            client = openai.OpenAI(max_retries=4, api_key=cle_api("OPENAI_API_KEY"))
        self.client = client
        self.modele = modele

    def ouvrir(self, systeme, outils, etiquette) -> SessionOpenAI:
        return SessionOpenAI(self.client, self.modele, systeme, outils)


# ---------------------------------------------------------------------------
# Rejeu
# ---------------------------------------------------------------------------

@dataclass
class SessionRejeu:
    enregistrement: dict | None
    deja_repondu: bool = field(default=False)

    def _tour(self) -> Tour:
        if self.enregistrement is None or self.deja_repondu:
            return Tour("", [], "fin", Usage())
        self.deja_repondu = True
        return Tour("", [Appel("rejeu", "repondre", self.enregistrement)], "outil", Usage())

    def envoyer(self, texte: str) -> Tour:
        return self._tour()

    def renvoyer(self, resultats: list[ResultatOutil]) -> Tour:
        return self._tour()


class FournisseurRejeu:
    """Relit un fichier JSONL : une ligne par question, cle 'id' (l'identifiant
    de la question ou son identifiant opaque, voir Question.id_opaque).

    Chaque ligne porte les champs de l'outil repondre. Une question absente
    du fichier se comporte comme un modele qui n'a rien repondu.
    """

    nom = "rejeu"

    def __init__(self, chemin: Path, modele: str = "inconnu"):
        self.modele = modele
        self.reponses = {}
        # Une ligne illisible est une faute de format du modele : la question
        # correspondante comptera comme sans reponse, le run continue.
        self.lignes_invalides = []
        self.normalisations: list[str] = []
        for ligne in Path(chemin).read_text(encoding="utf-8").splitlines():
            ligne = ligne.strip()
            if not ligne or ligne.startswith("```"):
                continue
            try:
                e = json.loads(ligne)
                self.reponses[e["id"]] = self._normaliser(e)
            except (json.JSONDecodeError, KeyError, TypeError, AttributeError):
                self.lignes_invalides.append(ligne[:200])

    STATUTS = ("reponse", "clarification", "hors_perimetre")

    def _normaliser(self, e: dict) -> dict:
        """Ramene un enregistrement aux champs de l'outil repondre.

        Par l'API, le schema strict de l'outil garantit les valeurs de statut.
        Hors API rien ne les garantit : un statut inconnu accompagne d'une
        requete est lu comme "reponse", et chaque correction est comptee pour
        figurer au rapport. Aucune autre correction n'est faite.
        """
        sql = (e.get("sql") or "").strip()
        statut = e.get("statut")
        if statut not in self.STATUTS:
            self.normalisations.append(f"statut {statut!r} -> reponse" if sql
                                       else f"statut {statut!r} sans requete")
            statut = "reponse" if sql else "clarification"
        return {
            "statut": statut,
            "sql": sql,
            "ambiguite": bool(e.get("ambiguite", False)),
            "interpretation": e.get("interpretation") or "",
            "reponse": e.get("reponse") or "",
        }

    def ouvrir(self, systeme, outils, etiquette) -> SessionRejeu:
        return SessionRejeu(self.reponses.get(etiquette)
                            or self.reponses.get(id_opaque(etiquette)))


def creer(nom: str, modele: str | None, effort: str | None = None,
          rejeu: Path | None = None) -> Fournisseur:
    if nom == "anthropic":
        return FournisseurAnthropic(modele or "claude-opus-5-5", effort)
    if nom == "openai":
        if not modele:
            raise ValueError("--modele est obligatoire avec openai")
        return FournisseurOpenAI(modele)
    if nom == "rejeu":
        if rejeu is None:
            raise ValueError("--rejeu est obligatoire avec le fournisseur rejeu")
        return FournisseurRejeu(rejeu, modele or "inconnu")
    raise ValueError(f"fournisseur inconnu : {nom}")
