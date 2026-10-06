"""Ligne de commande.

  python -m askdata ask "Quelle équipe a tenté le plus de tirs hors de la surface ?"
  python -m askdata eval --modele claude-opus-5-5 --variante documente --split dev
  python -m askdata noter runs/<run>
  python -m askdata comparer runs/<run1> runs/<run2>
  python -m askdata figer           # reecrit evals/references.json
  python -m askdata lot --variante brut --split dev > lot.md   # modele hors harnais
  python -m askdata prompt --variante brut
  python -m askdata sql "SELECT count(*) FROM sb.matches"
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

from . import agent, arbitrages, evaluation, garde, jeu, llm, prompt, rapport, references
from .db import DSN, Base, ErreurConnexion, dsn_affichable
from .schema import VARIANTES


def _options_modele(p: argparse.ArgumentParser) -> None:
    p.add_argument("--fournisseur", default="anthropic", choices=["anthropic", "openai", "rejeu"])
    p.add_argument("--modele", default=None, help="defaut anthropic : claude-opus-5-5")
    p.add_argument("--effort", default=None, choices=["low", "medium", "high", "xhigh", "max"])
    p.add_argument("--variante", default="documente", choices=VARIANTES)
    p.add_argument("--mode", default="agent", choices=prompt.MODES)
    p.add_argument("--rejeu", type=Path, help="fichier JSONL pour le fournisseur rejeu")


def cmd_ask(a) -> None:
    fournisseur = llm.creer(a.fournisseur, a.modele, a.effort, a.rejeu)
    base = Base(DSN)
    systeme = prompt.construire(base, a.variante, a.mode)
    t = agent.repondre(a.question, fournisseur, base, systeme, a.mode)
    for e in t.etapes:
        print(f"-- requete{' (ERREUR ' + e.erreur + ')' if e.erreur else ''}\n{e.sql}\n")
    if t.final is None:
        print(f"pas de reponse : {t.incident}")
        return
    f = t.final
    print(f"statut : {f['statut']}" + ("  [question ambigue]" if f.get("ambiguite") else ""))
    if f.get("interpretation"):
        print(f"lecture retenue : {f['interpretation']}")
    if f.get("sql"):
        print(f"\n{f['sql']}\n")
        try:
            r = base.executer(garde.verifier(f["sql"]))
            print(" | ".join(r.colonnes))
            for ligne in r.apercu(10):
                print(" | ".join(str(v) for v in ligne))
        except Exception as e:
            print(f"(la requete finale echoue : {e})")
    print(f"\n{f.get('reponse', '')}")
    cout = llm.cout(fournisseur.modele, t.usage)
    print(f"\n[{t.tours} tour(s), {t.usage.entree + t.usage.cache_lecture} jetons en entree, "
          f"{t.usage.sortie} en sortie" + (f", {cout:.4f} $" if cout is not None else "") + "]")


def cmd_eval(a) -> None:
    questions = jeu.filtrer(jeu.charger(), a.split, a.questions.split(",") if a.questions else None)
    fournisseur = llm.creer(a.fournisseur, a.modele, a.effort, a.rejeu)
    paralleles = 1 if a.fournisseur == "rejeu" else a.paralleles
    dossier = evaluation.lancer(questions, fournisseur, a.variante, a.mode,
                                a.repetitions, paralleles, a.reprendre)
    _noter_et_ecrire(dossier, questions)


def _noter_et_ecrire(dossier: Path, questions=None) -> None:
    evaluation.noter_run(dossier, questions)
    texte = rapport.rapport_run(dossier)
    (dossier / "rapport.md").write_text(texte, encoding="utf-8")
    synthese = texte.split("## Par split")[0]
    print(synthese)
    print(f"rapport complet : {dossier / 'rapport.md'}")


def cmd_noter(a) -> None:
    for d in a.dossiers:
        _noter_et_ecrire(d)


def cmd_comparer(a) -> None:
    texte = rapport.rapport_comparatif(a.dossiers)
    if a.sortie:
        a.sortie.write_text(texte, encoding="utf-8")
        print(f"ecrit : {a.sortie}")
    else:
        print(texte)


def cmd_figer(a) -> None:
    base = Base(DSN)
    empreintes = references.calculer(jeu.charger(), base)
    references.FICHIER.write_text(json.dumps(empreintes, ensure_ascii=False, indent=1) + "\n",
                                  encoding="utf-8")
    print(f"{len(empreintes)} references figees dans {references.FICHIER}")


def cmd_lot(a) -> None:
    questions = jeu.filtrer(jeu.charger(), a.split)
    random.Random(a.graine).shuffle(questions)
    print(prompt.construire_lot(Base(DSN), a.variante, questions))


def cmd_empreinte(a) -> None:
    print(arbitrages.empreinte_sql(a.requete))


def cmd_prompt(a) -> None:
    print(prompt.construire(Base(DSN), a.variante, a.mode))


def cmd_sql(a) -> None:
    r = Base(DSN).executer(garde.verifier(a.requete))
    print(" | ".join(r.colonnes))
    for ligne in r.apercu(50):
        print(" | ".join(str(v) for v in ligne))
    print(f"({len(r.lignes)} lignes)")


def main(argv=None) -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(prog="askdata")
    sous = p.add_subparsers(dest="commande", required=True)

    s = sous.add_parser("ask", help="pose une question")
    s.add_argument("question")
    _options_modele(s)
    s.set_defaults(f=cmd_ask)

    s = sous.add_parser("eval", help="lance un run sur le jeu d'evaluation")
    _options_modele(s)
    s.add_argument("--split", default="dev", choices=["dev", "test", "tout"])
    s.add_argument("--questions", help="identifiants separes par des virgules")
    s.add_argument("--repetitions", type=int, default=1)
    s.add_argument("--paralleles", type=int, default=4)
    s.add_argument("--reprendre", type=Path, help="dossier d'un run interrompu")
    s.set_defaults(f=cmd_eval)

    s = sous.add_parser("noter", help="renote des runs existants")
    s.add_argument("dossiers", nargs="+", type=Path)
    s.set_defaults(f=cmd_noter)

    s = sous.add_parser("comparer", help="compare plusieurs runs")
    s.add_argument("dossiers", nargs="+", type=Path)
    s.add_argument("--sortie", type=Path)
    s.set_defaults(f=cmd_comparer)

    s = sous.add_parser("figer", help="enregistre les resultats des references")
    s.set_defaults(f=cmd_figer)

    s = sous.add_parser("lot", help="prompt pour evaluer un modele hors harnais")
    s.add_argument("--variante", default="documente", choices=VARIANTES)
    s.add_argument("--split", default="dev", choices=["dev", "test", "tout"])
    s.add_argument("--graine", type=int, default=0, help="graine du melange des questions")
    s.set_defaults(f=cmd_lot)

    s = sous.add_parser("empreinte", help="empreinte d'une requete, pour un arbitrage")
    s.add_argument("requete")
    s.set_defaults(f=cmd_empreinte)

    s = sous.add_parser("prompt", help="affiche le prompt systeme")
    s.add_argument("--variante", default="documente", choices=VARIANTES)
    s.add_argument("--mode", default="agent", choices=prompt.MODES)
    s.set_defaults(f=cmd_prompt)

    s = sous.add_parser("sql", help="execute une requete en lecture seule")
    s.add_argument("requete")
    s.set_defaults(f=cmd_sql)

    a = p.parse_args(argv)
    try:
        a.f(a)
    except ErreurConnexion as e:
        message = str(e)[:300]
        print(f"arret : connexion a la base impossible. {message}", file=sys.stderr)
        print(f"Connexion utilisee : {dsn_affichable(DSN)} (variable WC_DSN, sinon "
              "valeur par defaut). Le role wc_lecteur existe-t-il, et son mot de passe "
              "est-il dans le fichier pgpass ? Voir le README.", file=sys.stderr)
        raise SystemExit(2) from None
    except Exception as e:
        if not agent.est_fatale(e):
            raise
        message = str(e).splitlines()[0][:300]
        print(f"arret : le fournisseur refuse l'acces ({type(e).__name__}). {message}",
              file=sys.stderr)
        print("Verifier la cle (ANTHROPIC_API_KEY ou OPENAI_API_KEY) et le nom du modele.",
              file=sys.stderr)
        raise SystemExit(2) from None


if __name__ == "__main__":
    main()
