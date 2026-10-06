# Ask Data sur la Coupe du monde 2018

Un agent qui répond en français à des questions sur la base
[wc2018-event-pipeline](https://github.com/LouisJauniau/wc2018-event-pipeline) en écrivant du SQL, et
surtout le banc d'essai qui mesure quand il se trompe.

```
$ python -m askdata ask "Quelle équipe a tenté le plus de tirs hors de la surface ?"
```

Pour une présentation sans jargon : [EXPLICATION.md](EXPLICATION.md).

Le chiffre habituel d'un système text-to-SQL, le taux de bonnes réponses,
cache la panne qui compte. Une requête qui plante se voit : l'utilisateur
reçoit une erreur. Une requête qui s'exécute et renvoie un chiffre faux ne
se voit pas : l'utilisateur reçoit un chiffre. Ce projet sépare donc les
issues au lieu de les fondre dans un score, et regarde à part ce qu'un taux
global mélange : les questions ambiguës, et celles auxquelles la base ne
peut pas répondre.

## Ce qui est mesuré

| Issue | Ce que voit l'utilisateur |
|---|---|
| **juste** | le bon résultat |
| **faux silencieux** | un résultat, faux, sans aucun signal |
| erreur d'exécution | une erreur PostgreSQL |
| abstention à tort | « je ne peux pas répondre » à une question qui avait une réponse |
| ambiguïté signalée / non signalée | la lecture retenue, dite ou tue |
| hors périmètre : abstention / réponse inventée | « la base ne le contient pas », ou un chiffre approché |

Sur les questions ambiguës, la mesure a deux faces, comme toute détection :
le taux de questions ambiguës signalées ne vaut rien sans le taux de
questions claires signalées à tort. Un agent qui déclarerait tout ambigu
aurait 100 % au premier.

## Résultats

### L'agent complet

Mode agent (le modèle explore la base avec un outil d'exécution avant de
répondre), description documentée, appels par l'API Anthropic. Opus a tourné
une fois sur le split dev, puis une seule fois sur le split test ; Haiku sur
l'ensemble du jeu. Entre crochets, l'intervalle de Wilson à 95 %.

| Run | Exactitude | Comparateur seul | Faux silencieux | Ambiguïtés signalées | Hors périmètre refusé | Coût |
|---|---|---|---|---|---|---|
| Opus 5.5, dev | 27/27 [88-100] | 26/27 | 0 | 4/4 | 3/3 | 0,65 $ |
| Opus 5.5, test | 25/25 [87-100] | 24/25 | 0 | 4/4 | 3/3 | 0,69 $ |
| Haiku 4.5, tout | 48/52 [82-97] | 48/52 | 4 | 2/8 | 5/6 | 0,50 $ |

« Comparateur seul » est le score avant arbitrage humain
([evals/arbitrages.toml](evals/arbitrages.toml)) ; les deux corrections
portent sur des réponses d'Opus plus détaillées que la référence (un total
accompagné du détail par équipe, la liste vérifiée des six équipes quand on
demandait leur nombre). Comparaison : [runs/comparatif_agent.md](runs/comparatif_agent.md).

**Opus ne se trompe sur aucune des 52 questions**, signale les 8
ambiguïtés et refuse les 6 questions hors périmètre, pour 2 centimes par
question grâce au cache du prompt système. Le split test, lu une seule fois
et sans réglage préalable, confirme le split dev. Mais comme Sonnet en
génération directe (plus bas), Opus sature le jeu : ce chiffre dit que
l'agent est fiable sur ce type de questions, pas jusqu'où.

**L'exploration corrige ce qu'elle doit corriger.** En génération directe,
Haiku cherchait « Modric » sans accent et trouvait zéro passe, dans les deux
vagues. En mode agent, il cherche `ILIKE '%Modric%'`, obtient zéro ligne,
change d'approche (`ILIKE '%Luka%'`), trouve « Luka Modrić » et répond juste.
Même parcours pour Mbappé. Aucune requête finale ne plante plus.

**Elle ne corrige pas ce qui ne fait pas d'erreur.** Les buts contre son
camp oubliés restent oubliés (temps additionnel, part des buts de première
période) : la requête s'exécute, le chiffre est plausible, rien ne signale le
problème. Haiku agent ne fait pas mieux que Haiku en un coup (92 % contre 85
à 90 %, dans le bruit, et dans des conditions qui ne sont pas identiques :
appels par l'API d'un côté, sous-agents et lots de l'autre) ; la boucle
change la nature des erreurs restantes plus que leur nombre.

**Un défaut des données source, repéré par l'agent, qui se trompe quand
même.** Dans les compositions de départ de la finale, StatsBomb écrit
« N''Golo Kanté » avec une apostrophe doublée, et « N'Golo Kanté » partout
ailleurs. Compter les titulaires par nom donne 19 au lieu de 18. Haiku
remarque l'anomalie, l'écrit dans sa réponse (« N'Golo Kanté compté deux
fois »), puis répond 19. La référence compte par identifiant et n'est pas
touchée.

### Génération en un coup

Vague 1 : génération en un coup (mode `direct`), trois descriptions de la
base de plus en plus riches, deux modèles. 52 questions répondables, 8
ambiguës, 6 hors périmètre. Entre crochets, l'intervalle de Wilson à 95 %.

| Modèle / description | Exactitude | Faux silencieux | Erreurs | Ambiguïtés signalées | Hors périmètre refusé |
|---|---|---|---|---|---|
| Haiku / brut | 38 % [26-52] | 48 % | 4 % | 2/8 | 5/6 |
| Haiku / valeurs | 56 % [42-68] | 33 % | 4 % | 3/8 | 6/6 |
| Haiku / documenté | 85 % [72-92] | 13 % | 2 % | 2/8 | 6/6 |
| Sonnet / brut | 100 % [93-100] | 0 % | 0 % | 7/8 | 6/6 |
| Sonnet / valeurs | 100 % [93-100] | 0 % | 0 % | 7/8 | 6/6 |
| Sonnet / documenté | 100 % [93-100] | 0 % | 0 % | 7/8 | 6/6 |

`brut` : tables, colonnes, types et clés, lus dans le catalogue. `valeurs` :
plus les valeurs des colonnes texte peu variées et l'arborescence des champs
jsonb, extraites automatiquement. `documenté` : plus un dictionnaire de
données écrit à la main ([askdata/dictionnaire.md](askdata/dictionnaire.md)).
Comparaison question par question : [runs/comparatif_vague1.md](runs/comparatif_vague1.md).

Vague 2 : les trois configurations de Haiku relancées, questions dans un
autre ordre, pour mesurer ce qui change d'un run à l'autre à prompt égal
([runs/comparatif_haiku_vagues.md](runs/comparatif_haiku_vagues.md)).

| Haiku | Vague 1 | Vague 2 | Même issue dans les deux vagues |
|---|---|---|---|
| brut | 38 % | 44 % | 39/52 |
| valeurs | 56 % | 58 % | 42/52 |
| documenté | 85 % | 90 % | 49/52 |

L'ordre des trois configurations tient, avec des écarts de 2 à 6 points
entre vagues. Sans documentation, 9 questions sur 52 changent d'issue d'un
run à l'autre : un run unique y est en bonne partie du bruit. Avec, 3
seulement, et les 5 échecs communs aux deux vagues sont des erreurs
systématiques, pas du hasard (voir plus bas).

### Ce qu'on en tire

**Presque toutes les erreurs sont silencieuses.** Sur les neuf runs, les
requêtes finales qui plantent ne dépassent jamais 4 % des questions. Sans
documentation, Haiku produit 47 requêtes : 45 s'exécutent, 20 sont justes.
Un banc qui compterait les requêtes qui s'exécutent lui donnerait 96 % ; il
en mérite 38.

**La documentation agit sur les faux silencieux, pas sur les erreurs.** De
la description brute à la description documentée, les faux silencieux de
Haiku passent de 25 à 7, les erreurs d'exécution de 2 à 1. Ce que le
dictionnaire apporte, ce sont des conventions qu'aucune introspection ne
retrouve : une passe réussie a un `outcome` NULL, la séance de tirs au but
est une période 5, un but contre son camp n'est pas un tir.

**Ce qui résiste à la documentation.** Les cinq questions que Haiku
documenté manque dans les deux vagues se rangent en trois familles.
- *Une règle écrite mais pas appliquée* : les buts contre son camp, oubliés
  dans le temps additionnel et dans la part des buts de première période
  (et une fois sur deux pour les buts de la France, 12 au lieu de 14), alors
  que le dictionnaire le dit en toutes lettres.
- *Une valeur que le modèle ne peut pas vérifier* : « Modric » cherché sans
  accent, zéro passe trouvée, alors que le dictionnaire prévient que les noms
  portent des accents. Un modèle qui écrit sa requête en un coup ne peut pas
  regarder la base. C'est ce que le mode agent apporte, avec un outil
  d'exécution pour explorer avant de répondre.
- *Une question mal lue* : « directement sur coup franc » compris comme
  « après un coup franc », par deux chemins différents selon la vague (les
  tirs qui suivent une passe sur coup franc, 8 buts, puis le motif de jeu
  'From Free Kick', 23 buts, au lieu de 6). C'est la lecture qui est
  systématique, pas la requête.
- *Une syntaxe mal maîtrisée* : le dépliage d'un tableau jsonb placé à
  l'intérieur d'un agrégat, ce que PostgreSQL refuse, dans les deux vagues.

**Sonnet sature le jeu.** 52 sur 52 dans les trois configurations, y compris
sans aucune documentation. Ses requêtes montrent pourquoi : il connaît le
format StatsBomb, qui est public (`outcome IS NULL`, `period < 5`, les types
`Own Goal`), et se couvre là où il doute (`ILIKE 'Luka Modri%'`,
`details::text ILIKE '%Red Card%'`). Deux conséquences. Ce jeu ne mesure plus
rien sur Sonnet : il faudrait des questions plus dures, ou un schéma privé
que le modèle n'a jamais vu. Et ce que Sonnet tire de son entraînement
ressemble à ce que le dictionnaire apporte à Haiku. Hypothèse, non mesurée
ici : sur des données d'entreprise qu'aucun modèle n'a lues, Sonnet sans
documentation perdrait une partie de cet avantage, et la documentation
redeviendrait le levier principal.

**Ambiguïté.** Sonnet en signale 7 sur 8. Haiku entre 0 et 3 selon la
configuration et la vague, avec jusqu'à 10 questions claires signalées à
tort : chez lui, le drapeau d'ambiguïté ne porte pas d'information. Sur
« Combien de passes décisives Hazard a-t-il délivrées ? », Haiku additionne Eden et
Thorgan sans rien signaler, et tombe juste par chance : Thorgan n'en a
délivré aucune. Les signalements de Sonnet sur des questions classées
claires portent sur des lectures réellement discutables (« tirs par match » :
des deux équipes ou d'une seule ?), et il répond chaque fois selon la
convention attendue. Signaler et répondre quand même est le comportement
voulu ; la frontière entre question claire et ambiguë est elle-même un choix
de l'auteur du jeu.

**Hors périmètre.** Deux réponses inventées sur 54 occasions, toutes deux de
Haiku sans dictionnaire, toutes deux sur la même question : la « distance
parcourue » reconstruite à partir de la longueur des conduites de balle. La
donnée voisine qui tente l'approximation est exactement le piège prévu.

## Comment l'évaluation est construite

**Le jeu** ([evals/questions.toml](evals/questions.toml)) : 66 questions
formulées comme un utilisateur les poserait. 52 ont une réponse (comptages,
classements, ratios, listes), 8 sont ambiguës, 6 portent sur ce que la base
ne contient pas. Chaque question répondable porte une requête de référence
écrite à la main ; chaque question ambiguë porte une requête par
interprétation raisonnable.

**Les pièges** ([evals/PIEGES.md](evals/PIEGES.md)). Chaque question déclare
ce qu'elle met à l'épreuve : la séance de tirs au but stockée en période 5,
les buts contre son camp absents des tirs, `outcome` NULL pour une passe
réussie, les noms d'équipes en anglais, les accents, les égalités en tête de
classement. Le rapport donne le taux d'échec par piège, ce qui dit pourquoi
un modèle se trompe et pas seulement combien de fois.

**La vérité terrain est du code, elle se teste.**
- Les références recoupent les chiffres officiels du tournoi : 169 buts,
  12 contre son camp, 29 penalties en cours de jeu, Kane meilleur buteur
  avec 6 buts.
- Trois références sont écrites deux fois, par des chemins indépendants
  (le score des matchs, puis les tirs et les buts contre son camp ; ou les
  deux événements qui enregistrent un même but contre son camp), et les deux
  écritures doivent concorder.
- Le résultat de chaque référence est figé dans
  [evals/references.json](evals/references.json) : un test échoue si l'un
  d'eux change.
- Les classements gardent les ex aequo. « Quel match a été le plus riche en
  buts ? » a trois réponses (7 buts chacun) ; un `LIMIT 1` en donne une au
  hasard, et le comparateur le diagnostique comme égalité tronquée.

**On compare des résultats, pas des requêtes**
([askdata/comparaison.py](askdata/comparaison.py)). Deux SQL différents qui
renvoient la même réponse sont justes tous les deux. L'ordre et le nom des
colonnes ne comptent pas, les colonnes en plus sont tolérées, un nombre
arrondi est accepté s'il est exactement l'arrondi de la référence au nombre
de décimales qu'il affiche (66,5 pour 66,5079, pas 67), une proportion est
acceptée en fraction ou en pourcentage. Un échec reçoit un diagnostic :
résultat vide, égalité tronquée, mauvais nombre de lignes, mauvaise entité,
mauvaise valeur, mauvais ordre.

**On évalue l'évaluateur** ([evals/meta.toml](evals/meta.toml)). 29
requêtes dont on connaît le verdict : des réécritures justes qui doivent
passer, des erreurs typiques qui doivent échouer avec le bon diagnostic.
Ce test a trouvé un défaut dès sa première exécution : avec des colonnes
clés alternatives, le diagnostic venait de la première alternative essayée
au lieu de la plus proche de la bonne réponse.

Deux autres défauts du banc lui-même ont été trouvés en lisant les sorties
plutôt que les scores. Sous le rôle en lecture seule, la description de la
base perdait toutes ses clés primaires et étrangères, parce
qu'`information_schema` ne montre les contraintes qu'aux rôles qui ont un
droit autre que `SELECT` : la variante « brut » aurait été mesurée affaiblie,
sans erreur. Et le prompt hors API ne montrait pas les valeurs permises du
statut ; tous les modèles ont écrit `"ok"` ou `"success"`, ce qui, noté tel
quel, aurait classé de 55 à 59 réponses sur 66 par run en abstentions.

**Dev et test.** Les questions sont réparties en deux moitiés équilibrées
par catégorie. Les consignes du prompt ne se règlent que sur le split dev ;
le split test sert à vérifier qu'un gain ne vient pas d'un réglage sur les
questions elles-mêmes. Aucun réglage n'a encore eu lieu : les deux vagues
utilisent les mêmes consignes, le split test est donc encore vierge.

**Le run et la notation sont séparés.** Un run écrit des traces ; la
notation les relit, réexécute chaque requête finale et la compare à la
référence. On ne croit pas l'agent sur parole quant à ce que sa requête
renvoie, et on peut corriger le comparateur puis renoter sans rappeler le
modèle.

## L'agent

[askdata/agent.py](askdata/agent.py). Deux outils : `executer_sql`, pour
explorer et tester (vérifier un nom, une valeur, la forme d'un résultat), et
`repondre`, qui porte la requête finale, le statut (réponse, clarification,
hors périmètre), le drapeau d'ambiguïté et la lecture retenue. Les schémas
d'outils sont stricts. Une erreur PostgreSQL est renvoyée au modèle, qui
peut corriger ; le nombre de tours est borné.

- **Base protégée par le rôle, pas par le filtre.** L'agent se connecte avec
  un rôle qui n'a que `SELECT` sur le schéma ([sql/role_lecteur.sql](sql/role_lecteur.sql)),
  ses transactions sont en lecture seule et coupées après 10 secondes. Le
  filtre de [askdata/garde.py](askdata/garde.py) ne vient qu'en plus, pour
  refuser tôt avec un message clair.
- **Deux fournisseurs** derrière une interface commune : Anthropic et OpenAI,
  par leurs SDK officiels. L'historique n'est jamais réécrit, seulement
  allongé, et le prompt système, identique pour toutes les questions, est
  mis en cache.
- **Pas de modèle de repli.** Un repli automatique vers un autre modèle en
  cas de refus changerait le modèle évalué en cours de run ; un refus est
  compté comme incident.
- Un troisième fournisseur, `rejeu`, relit des réponses produites ailleurs.
  `python -m askdata lot` produit le prompt pour un modèle qu'on n'appelle
  pas par API ; c'est ainsi qu'ont été produites les vagues ci-dessus.

## Ce que ces chiffres ne disent pas

- **Le jeu est saturé pour les grands modèles.** Opus en agent et Sonnet en
  génération directe font le plein. Ces questions mesurent bien les modèles
  plus petits et les variantes de prompt ; pour départager les grands, il
  faudrait des questions plus difficiles ou un schéma que le modèle n'a pas
  pu lire pendant son entraînement.
- **Un run par configuration pour l'agent.** La variance d'un run à l'autre
  n'est mesurée qu'en génération directe, sur Haiku (deux vagues).
- **Deux verdicts corrigés à la main**, sur 52 réponses d'Opus, selon un
  critère écrit en tête de [evals/arbitrages.toml](evals/arbitrages.toml).
  Le score avant correction est toujours affiché à côté.
- **Génération en un coup : questions par lots.** Les vagues 1 et 2 ont été
  produites par des sous-agents, chacun recevant 32 ou 34 questions dans le
  même prompt, pas une par appel ([runs/README.md](runs/README.md)). Les
  paires de questions qui se renseignent l'une l'autre ont été séparées,
  mais l'indépendance n'est pas celle d'appels distincts.
- **Une copie de la base.** Les runs ont tourné sur une base rechargée par
  la même chaîne d'ingestion (227 825 événements, 11 199 possessions). Les
  183 tests passent aussi sur la base d'origine : chaque référence y donne
  exactement le même résultat.
- **Petits effectifs.** 52 questions répondables : un écart de quelques
  points n'est pas un résultat. Les intervalles sont donnés pour cette
  raison.
- **Le dictionnaire et les questions ont le même auteur.** Le dictionnaire
  décrit les données et non les questions (une première version qui listait
  les cas hors périmètre a été retirée pour cette raison), mais l'effet de
  la documentation mesuré ici est sans doute un majorant.
- **Les tolérances du comparateur sont des choix.** Un pourcentage arrondi à
  l'entier est refusé ; une colonne en plus qui contiendrait par hasard la
  bonne valeur ferait passer une réponse fausse. La méta-évaluation borne ce
  risque, elle ne l'annule pas.

## Utilisation

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
```

La base est celle de `wc2018-event-pipeline` (`python run.py ingest`).
L'agent s'y connecte avec un rôle en lecture seule. Le créer une fois, en
superutilisateur, et relancer le script après chaque ingestion, qui recrée
le schéma et efface les droits :

```bash
psql -h localhost -U postgres -d wc2018 -f sql/role_lecteur.sql
```

Lui donner un mot de passe : ouvrir `psql -h localhost -U postgres -d wc2018`,
taper `\password wc_lecteur`, puis ranger ce mot de passe dans le fichier
`pgpass` de PostgreSQL (sous Windows, `%APPDATA%\postgresql\pgpass.conf`),
sur une ligne :

```
localhost:5432:wc2018:wc_lecteur:<mot de passe>
```

Ainsi le mot de passe ne figure ni dans une commande, ni dans l'historique
du terminal, ni dans un fichier du dépôt.

La clé d'API se range dans les variables d'environnement de l'utilisateur
(sous Windows : `setx ANTHROPIC_API_KEY "sk-ant-..."`). Elle est lue même
depuis un terminal ouvert avant son enregistrement.

Sans autre réglage, la connexion utilisée est
`host=localhost dbname=wc2018 user=wc_lecteur`. Pour viser une autre base,
définir `WC_DSN` (en PowerShell : `$env:WC_DSN = "host=... dbname=... user=..."`).

```bash
python -m askdata ask "Combien de buts la France a-t-elle marqués ?"
```

```bash
python -m askdata eval --modele claude-opus-5-5 --variante documente --mode agent --split dev
```

```bash
python -m askdata comparer runs/<run1> runs/<run2> --sortie runs/comparatif.md
```

Autres commandes : `noter` (renoter un run), `figer` (après une modification
voulue d'une référence), `prompt` (afficher le prompt système), `lot`
(prompt pour un modèle hors API), `sql` (requête en lecture seule).
Fournisseur OpenAI : `--fournisseur openai --modele <modèle>`.

```bash
python -m pytest
```

Les tests qui ont besoin de la base sont sautés, avec un message, si la
connexion échoue.

## Organisation

```
askdata/
  agent.py          la boucle : question, requêtes, réponse, trace
  llm.py            fournisseurs Anthropic, OpenAI, rejeu
  prompt.py         consignes et schémas des outils
  schema.py         description de la base en trois niveaux
  dictionnaire.md   conventions écrites à la main
  garde.py          filtre des requêtes avant exécution
  db.py             accès en lecture seule
  comparaison.py    résultat obtenu contre résultat de référence
  evaluation.py     lancement d'un run, notation des traces
  rapport.py        synthèse, intervalles, comparaison de runs
  references.py     empreintes des résultats de référence
evals/
  questions.toml    le jeu
  PIEGES.md         le catalogue des pièges
  meta.toml         les cas de la méta-évaluation
  references.json   résultats de référence figés
runs/               runs enregistrés, rapports, comparatifs
sql/role_lecteur.sql
tests/
```

Données : [StatsBomb Open Data](https://github.com/statsbomb/open-data),
soumises à leur accord de licence, qui impose l'attribution.
