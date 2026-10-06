"""Prompt systeme et definition des outils de l'agent.

Les consignes sont les memes pour toutes les variantes ; seule la
description de la base change (voir schema.py). Elles ont ete reglees sur
les questions du split dev uniquement.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from . import schema
from .db import Base

CONSIGNES = """\
Tu réponds à des questions sur la Coupe du monde de football 2018 en
interrogeant une base PostgreSQL (schéma sb), décrite plus bas.

Règles pour le SQL :
- Une seule requête SELECT (ou WITH ... SELECT), dialecte PostgreSQL.
- Renvoie des colonnes lisibles : noms d'équipes ou de joueurs plutôt que des
  identifiants, avec la mesure qui justifie la réponse.
- Pour une question « quelle équipe » ou « quel joueur », renvoie toutes les
  lignes ex aequo en tête plutôt qu'une seule : un LIMIT 1 sur une égalité
  cache les autres bonnes réponses.
- N'arrondis pas dans le SQL ; l'arrondi se fait à l'affichage.

Avant de répondre, demande-toi si la question admet plusieurs lectures
raisonnables qui donneraient des réponses différentes. Si oui, mets
ambiguite à true, réponds selon la lecture la plus probable et décris-la
dans interpretation. Si aucune lecture n'est raisonnable sans précision de
l'utilisateur, utilise le statut clarification et pose ta question dans
reponse.

Si la base ne contient pas l'information demandée, utilise le statut
hors_perimetre et dis ce qui manque. N'approxime pas avec une donnée
voisine.
"""

CONSIGNES_AGENT = """\
Tu disposes de l'outil executer_sql pour lancer des requêtes exploratoires
(vérifier un nom, une valeur, la forme d'un résultat) et pour tester ta
requête finale. Termine toujours en appelant l'outil repondre, avec la
requête finale et une réponse en une ou deux phrases fondée sur son
résultat.
"""

CONSIGNES_DIRECT = """\
Tu ne peux pas exécuter de requête : appelle directement l'outil repondre.
Dans reponse, dis en une phrase ce que la requête calcule.
"""


@dataclass(frozen=True)
class Outil:
    nom: str
    description: str
    schema: dict


OUTIL_SQL = Outil(
    nom="executer_sql",
    description=(
        "Exécute une requête SELECT en lecture seule sur la base et renvoie les "
        "colonnes, au plus 20 lignes et le nombre total de lignes, ou l'erreur "
        "PostgreSQL."
    ),
    schema={
        "type": "object",
        "properties": {"sql": {"type": "string", "description": "Une requête SELECT."}},
        "required": ["sql"],
        "additionalProperties": False,
    },
)

OUTIL_REPONDRE = Outil(
    nom="repondre",
    description="Donne la réponse finale à l'utilisateur. À appeler une seule fois, en dernier.",
    schema={
        "type": "object",
        "properties": {
            "statut": {
                "type": "string",
                "enum": ["reponse", "clarification", "hors_perimetre"],
                "description": "reponse si une requête répond à la question.",
            },
            "sql": {
                "type": "string",
                "description": "La requête finale. Chaîne vide si statut n'est pas reponse.",
            },
            "ambiguite": {
                "type": "boolean",
                "description": ("true si la question admet plusieurs lectures "
                                "qui changent la réponse."),
            },
            "interpretation": {
                "type": "string",
                "description": "La lecture retenue si ambiguite est true, sinon chaîne vide.",
            },
            "reponse": {
                "type": "string",
                "description": "Le texte destiné à l'utilisateur.",
            },
        },
        "required": ["statut", "sql", "ambiguite", "interpretation", "reponse"],
        "additionalProperties": False,
    },
)

MODES = ("agent", "direct")


def outils(mode: str) -> list[Outil]:
    if mode == "agent":
        return [OUTIL_SQL, OUTIL_REPONDRE]
    if mode == "direct":
        return [OUTIL_REPONDRE]
    raise ValueError(f"mode inconnu : {mode}")


CONSIGNES_LOT = """# Format de sortie

Les questions ci-dessous sont indépendantes : traite chacune comme si elle
était seule, sans t'appuyer sur les autres. Pour chacune, écris exactement
les champs que tu passerais à l'outil repondre, en une ligne JSON :

{"id": "...", "statut": "...", "sql": "...", "ambiguite": false, "interpretation": "...", "reponse": "..."}

Une ligne par question, dans l'ordre, rien d'autre.

# Questions

"""


def construire_lot(base: Base, variante: str, questions) -> str:
    """Prompt pour evaluer un modele hors harnais (interface web, autre outil) :
    le prompt du mode direct, suivi des questions et du format attendu. Les
    reponses se notent ensuite avec le fournisseur rejeu."""
    # Le schema de l'outil est donne tel quel : par l'API il accompagne la
    # requete, et c'est lui qui fixe les valeurs permises de statut.
    schema_outil = json.dumps(OUTIL_REPONDRE.schema, ensure_ascii=False, indent=1)
    lignes = "\n".join(f"{q.id_opaque} : {q.question}" for q in questions)
    return (f"{construire(base, variante, 'direct')}\n"
            f"# Schéma de l'outil repondre\n\n{schema_outil}\n\n{CONSIGNES_LOT}{lignes}\n")


def construire(base: Base, variante: str, mode: str) -> str:
    consignes_mode = CONSIGNES_AGENT if mode == "agent" else CONSIGNES_DIRECT
    return f"{CONSIGNES}\n{consignes_mode}\n# La base\n\n{schema.decrire(base, variante)}\n"
