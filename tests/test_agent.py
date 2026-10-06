"""La boucle de l'agent, avec un faux modele qui suit un script."""

import pytest

from askdata.agent import MAX_TOURS, repondre
from askdata.db import ErreurSQL, Resultat
from askdata.llm import Appel, Tour, Usage


class FausseBase:
    def __init__(self):
        self.requetes = []

    def executer(self, sql):
        self.requetes.append(sql)
        if "colonne_inconnue" in sql:
            raise ErreurSQL('column "colonne_inconnue" does not exist', "42703")
        return Resultat(("n",), ((14,),))


class ModeleScripte:
    """Rejoue une liste de tours, et garde ce qu'on lui renvoie."""

    nom, modele = "faux", "faux"

    def __init__(self, tours):
        self.tours = list(tours)
        self.recus = []

    def ouvrir(self, systeme, outils, etiquette):
        self.outils = [o.nom for o in outils]
        return self

    def _suivant(self):
        return self.tours.pop(0) if self.tours else Tour("", [], "fin", Usage())

    def envoyer(self, texte):
        self.recus.append(texte)
        return self._suivant()

    def renvoyer(self, resultats):
        self.recus.append(resultats)
        return self._suivant()


def sql(id_, requete):
    return Tour("", [Appel(id_, "executer_sql", {"sql": requete})], "outil", Usage(10, 5, 0, 0, 1))


def final(requete="SELECT 14", statut="reponse"):
    return Tour("", [Appel("f", "repondre", {"statut": statut, "sql": requete, "ambiguite": False,
                                             "interpretation": "", "reponse": "14 buts"})],
                "outil", Usage(10, 5, 0, 0, 1))


def test_erreur_renvoyee_au_modele_puis_rattrapee():
    modele = ModeleScripte([sql("a", "SELECT colonne_inconnue"), sql("b", "SELECT 14"), final()])
    t = repondre("q", modele, FausseBase(), "systeme", "agent")
    assert t.final["sql"] == "SELECT 14"
    assert [e.erreur is not None for e in t.etapes] == [True, False]
    assert t.etapes[0].erreur.startswith("42703")
    erreur_vue = modele.recus[1][0]
    assert erreur_vue.erreur and "does not exist" in erreur_vue.contenu
    assert erreur_vue.id == "a"
    assert t.usage.appels == 3 and t.incident is None


def test_garde_avant_la_base():
    base = FausseBase()
    modele = ModeleScripte([sql("a", "DELETE FROM sb.teams"), final()])
    t = repondre("q", modele, base, "systeme", "agent")
    assert base.requetes == []
    assert t.etapes[0].erreur.startswith("garde")


def test_relance_unique_si_reponse_en_texte_libre():
    modele = ModeleScripte([Tour("La France a marqué 14 buts.", [], "fin", Usage()), final()])
    t = repondre("q", modele, FausseBase(), "systeme", "agent")
    assert t.final is not None and "repondre" in modele.recus[1]

    modele = ModeleScripte([Tour("bla", [], "fin", Usage()), Tour("bla", [], "fin", Usage())])
    t = repondre("q", modele, FausseBase(), "systeme", "agent")
    assert t.final is None and t.incident == "pas_de_reponse"


def test_refus_du_modele():
    t = repondre("q", ModeleScripte([Tour("", [], "refus", Usage())]), FausseBase(), "s", "agent")
    assert t.incident == "arret_refus"


def test_nombre_de_tours_borne_et_reponse_au_dernier_tour_gardee():
    boucle = [sql(str(i), "SELECT 1") for i in range(MAX_TOURS - 1)]
    t = repondre("q", ModeleScripte(boucle + [final()]), FausseBase(), "s", "agent")
    assert t.final is not None and t.tours == MAX_TOURS

    t = repondre("q", ModeleScripte([sql(str(i), "SELECT 1") for i in range(20)]),
                 FausseBase(), "s", "agent")
    assert t.final is None and t.incident == "max_tours" and t.tours == MAX_TOURS


def test_mode_direct_sans_outil_sql():
    modele = ModeleScripte([sql("a", "SELECT 1"), final()])
    base = FausseBase()
    t = repondre("q", modele, base, "s", "direct")
    assert modele.outils == ["repondre"]
    assert base.requetes == [] and t.final is not None


def test_exception_isolee_mais_erreur_d_authentification_fatale():
    class Panne(ModeleScripte):
        def envoyer(self, texte):
            raise RuntimeError("connexion perdue")

    t = repondre("q", Panne([]), FausseBase(), "s", "agent")
    assert t.incident.startswith("exception: RuntimeError")

    class AuthenticationError(Exception):
        pass

    class CleRefusee(ModeleScripte):
        def envoyer(self, texte):
            raise AuthenticationError("cle invalide")

    with pytest.raises(AuthenticationError):
        repondre("q", CleRefusee([]), FausseBase(), "s", "agent")

    class SansCle(ModeleScripte):
        def envoyer(self, texte):
            # Ce que leve le SDK Anthropic quand aucune cle n'est configuree.
            raise TypeError('"Could not resolve authentication method. Expected one of ..."')

    with pytest.raises(TypeError):
        repondre("q", SansCle([]), FausseBase(), "s", "agent")
