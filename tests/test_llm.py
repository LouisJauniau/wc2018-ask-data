"""Les adaptateurs de fournisseurs, avec des clients factices : on verifie la
forme des requetes envoyees et la lecture des reponses, sans reseau."""

import json
from types import SimpleNamespace as NS

from askdata.llm import (FournisseurAnthropic, FournisseurOpenAI, FournisseurRejeu,
                         ResultatOutil, Usage, cout)
from askdata.prompt import outils


def _en_json(objet):
    return json.loads(json.dumps(objet, default=lambda o: o.__dict__))


class ClientAnthropique:
    def __init__(self, reponses):
        self.reponses = list(reponses)
        self.requetes = []
        self.messages = self

    def create(self, **kw):
        self.requetes.append(_en_json(kw))
        return self.reponses.pop(0)


def reponse_anthropic(contenu, arret):
    return NS(content=contenu, stop_reason=arret,
              usage=NS(input_tokens=100, output_tokens=20,
                       cache_read_input_tokens=3000, cache_creation_input_tokens=None))


def test_anthropic_boucle_outil():
    appel = NS(type="tool_use", id="toolu_1", name="executer_sql", input={"sql": "SELECT 1"})
    client = ClientAnthropique([
        reponse_anthropic([NS(type="text", text="Je vérifie."), appel], "tool_use"),
        reponse_anthropic([NS(type="text", text="fini")], "end_turn"),
    ])
    session = FournisseurAnthropic("claude-opus-5-5", effort="low", client=client).ouvrir(
        "SYSTEME", outils("agent"), "q1")

    tour = session.envoyer("question")
    assert tour.arret == "outil" and tour.appels[0].arguments == {"sql": "SELECT 1"}
    assert tour.texte == "Je vérifie."
    assert tour.usage == Usage(100, 20, 3000, 0, 1)
    req = client.requetes[0]
    assert req["system"][0]["cache_control"] == {"type": "ephemeral"}
    assert all(t["strict"] for t in req["tools"])
    assert req["output_config"] == {"effort": "low"}
    # Ni temperature ni tool_choice force : refuses par les modeles recents.
    assert "temperature" not in req and "tool_choice" not in req

    tour = session.renvoyer([ResultatOutil("toolu_1", "1 ligne", erreur=True)])
    assert tour.arret == "fin"
    msgs = client.requetes[1]["messages"]
    assert [m["role"] for m in msgs] == ["user", "assistant", "user"]
    assert msgs[2]["content"][0] == {"type": "tool_result", "tool_use_id": "toolu_1",
                                     "content": "1 ligne", "is_error": True}


def test_anthropic_haiku_sans_effort():
    client = ClientAnthropique([reponse_anthropic([], "refusal")])
    s = FournisseurAnthropic("claude-haiku-4-5", effort="low", client=client).ouvrir(
        "S", outils("direct"), "q")
    assert s.envoyer("q").arret == "refus"
    assert "output_config" not in client.requetes[0]


class ClientOpenAI:
    def __init__(self, reponses):
        self.reponses = list(reponses)
        self.requetes = []
        self.chat = NS(completions=self)

    def create(self, **kw):
        self.requetes.append(_en_json(kw))
        return self.reponses.pop(0)


def test_openai_boucle_outil():
    appel = NS(id="call_1", function=NS(name="repondre", arguments='{"statut": "reponse"}'))
    client = ClientOpenAI([
        NS(choices=[NS(message=NS(content=None, tool_calls=[appel]), finish_reason="tool_calls")],
           usage=NS(prompt_tokens=1000, completion_tokens=50,
                    prompt_tokens_details=NS(cached_tokens=800))),
        NS(choices=[NS(message=NS(content="ok", tool_calls=None), finish_reason="stop")],
           usage=NS(prompt_tokens=10, completion_tokens=1, prompt_tokens_details=None)),
    ])
    s = FournisseurOpenAI("modele-x", client=client).ouvrir("SYSTEME", outils("direct"), "q")
    tour = s.envoyer("question")
    assert tour.appels[0].arguments == {"statut": "reponse"}
    assert tour.usage == Usage(200, 50, 800, 0, 1)
    req = client.requetes[0]
    assert req["messages"][0] == {"role": "system", "content": "SYSTEME"}
    assert req["tools"][0]["function"]["strict"] is True

    tour = s.renvoyer([ResultatOutil("call_1", "ok")])
    assert tour.arret == "fin"
    msgs = client.requetes[1]["messages"]
    assert msgs[2]["tool_calls"][0]["id"] == "call_1"
    assert msgs[3] == {"role": "tool", "tool_call_id": "call_1", "content": "ok"}


def test_rejeu(tmp_path):
    f = tmp_path / "r.jsonl"
    f.write_text(json.dumps({"id": "q1", "sql": "SELECT 1", "ambiguite": True}) + "\n",
                 encoding="utf-8")
    fournisseur = FournisseurRejeu(f)
    tour = fournisseur.ouvrir("", [], "q1").envoyer("question")
    assert tour.appels[0].arguments["sql"] == "SELECT 1"
    assert tour.appels[0].arguments["statut"] == "reponse"
    assert fournisseur.ouvrir("", [], "absente").envoyer("question").appels == []


def test_rejeu_tolere_les_lignes_illisibles(tmp_path):
    f = tmp_path / "r.jsonl"
    f.write_text('```json\n{"id": "q1", "sql": "SELECT 1"}\n{"id": "q2", "sql": "SELECT\n```\n',
                 encoding="utf-8")
    fournisseur = FournisseurRejeu(f)
    assert set(fournisseur.reponses) == {"q1"}
    assert len(fournisseur.lignes_invalides) == 1  # la cloture ``` est ignoree


def test_rejeu_normalise_les_statuts_hors_schema_et_le_compte(tmp_path):
    f = tmp_path / "r.jsonl"
    lignes = [{"id": "a", "statut": "ok", "sql": "SELECT 1"},
              {"id": "b", "statut": "hors_perimetre", "sql": None},
              {"id": "c", "statut": "success", "sql": ""}]
    f.write_text("\n".join(json.dumps(l) for l in lignes), encoding="utf-8")
    fournisseur = FournisseurRejeu(f)
    assert fournisseur.reponses["a"]["statut"] == "reponse"
    assert fournisseur.reponses["b"] == {"statut": "hors_perimetre", "sql": "",
                                         "ambiguite": False, "interpretation": "",
                                         "reponse": ""}
    assert fournisseur.reponses["c"]["statut"] == "clarification"
    assert fournisseur.normalisations == ["statut 'ok' -> reponse",
                                          "statut 'success' sans requete"]


def test_cout():
    assert cout("modele-inconnu", Usage(10, 10)) is None
    assert abs(cout("claude-haiku-4-5", Usage(1_000_000, 0)) - 1.0) < 1e-9


def test_cle_api_prise_dans_l_environnement(monkeypatch):
    from askdata import llm
    monkeypatch.setenv("CLE_DE_TEST", "valeur")
    assert llm.cle_api("CLE_DE_TEST") == "valeur"
    monkeypatch.delenv("CLE_DE_TEST")
    monkeypatch.setattr(llm.os, "name", "posix")
    assert llm.cle_api("CLE_DE_TEST") is None
