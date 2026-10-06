# Ce projet en termes simples

## L'idée

On pose une question en français sur la Coupe du monde 2018, par exemple
« Quelle équipe a tenté le plus de tirs hors de la surface ? ». Un assistant
d'intelligence artificielle va chercher la réponse dans une base de données
qui contient tout ce qui s'est passé pendant les 64 matchs : chaque passe,
chaque tir, chaque faute, près de 230 000 actions. Il répond par une phrase :
« C'est la Croatie, avec 54 tirs, devant le Brésil (39) et la France (35). »

## À quoi ça sert

Dans une entreprise, beaucoup de gens ont des questions sur leurs données
(« combien de clients ont commandé deux fois ce mois-ci ? ») mais ne savent
pas interroger une base de données. Ils doivent demander à quelqu'un qui
sait, et attendre. Un assistant qui comprend la question et va chercher la
réponse lui-même leur fait gagner ce temps.

Le football sert ici de terrain d'essai : les données sont publiques, et
les bonnes réponses peuvent être vérifiées contre les chiffres officiels du
tournoi.

## Le vrai sujet : savoir quand l'assistant se trompe

Un assistant de ce genre peut se tromper de deux façons.

- **De façon visible** : il n'arrive pas à répondre et le dit. C'est gênant,
  mais l'utilisateur le sait.
- **De façon invisible** : il répond un chiffre faux, avec la même assurance
  qu'un chiffre juste. C'est la panne dangereuse, parce que personne ne s'en
  aperçoit.

Un exemple réel, observé pendant les essais. À la question « Combien de buts
la France a-t-elle marqués ? », l'assistant le moins puissant a répondu 12.
La bonne réponse est 14 : il avait oublié les deux buts que des adversaires
ont marqués contre leur propre camp. Sa réponse avait l'air parfaitement
normale.

C'est pour cela que ce projet est d'abord un **banc d'essai** : un moyen de
mesurer combien de fois l'assistant se trompe, de quelle façon, et pourquoi.

## Comment l'assistant fonctionne

1. **Il lit la question.**
2. **Il lit la description de la base**, un peu comme on consulte le plan
   d'une bibliothèque avant d'y chercher un livre. Cette description dit ce
   que contient chaque rayon, et quelques règles utiles : par exemple que les
   séances de tirs au but sont rangées à part et ne comptent pas dans les
   statistiques de match.
3. **Il cherche et vérifie.** Il peut interroger la base plusieurs fois avant
   de répondre. Quand on lui demande les passes de « Modric », il cherche ce
   nom, ne trouve rien, essaie autrement, et découvre que le joueur est
   enregistré sous le nom « Luka Modrić », avec un accent.
4. **Il répond par une phrase.** Si la question peut se comprendre de
   plusieurs façons, il le signale et dit laquelle il a choisie. Si la base
   ne contient pas l'information, il le dit au lieu d'inventer.

L'assistant a un accès en lecture seule : il peut consulter la base, pas la
modifier.

## Comment on le contrôle

On lui fait passer un **examen de 66 questions**, avec un corrigé.

- **52 questions ont une réponse nette.** Pour chacune, la bonne réponse a
  été établie à la main, puis recoupée avec les chiffres officiels du
  tournoi : 169 buts, 12 buts contre son camp, Harry Kane meilleur buteur
  avec 6 buts.
- **8 questions sont ambiguës.** « Combien de matchs la Russie a-t-elle
  gagnés ? » : le huitième de finale remporté aux tirs au but compte-t-il
  comme une victoire ? On attend de l'assistant qu'il remarque l'ambiguïté et
  la signale.
- **6 questions n'ont pas de réponse dans la base.** « Combien de spectateurs
  ont assisté à la finale ? » : l'information n'y est pas. On attend de
  l'assistant qu'il le dise, et non qu'il fabrique un chiffre.

Les questions contiennent des **pièges volontaires**, ceux qui produisent
les erreurs invisibles : les buts contre son camp, les tirs au but, les noms
d'équipes enregistrés en anglais, les accents, les égalités en tête d'un
classement.

On corrige la réponse, pas la façon d'y arriver : deux chemins différents qui
mènent au bon résultat sont tous les deux justes. Le correcteur automatique
est lui-même testé sur des réponses dont on connaît le verdict. Quand il se
trompe, la correction est faite à la main, écrite et justifiée, et la note
d'origine reste affichée à côté.

## Ce qu'on a appris

- **Le modèle le plus puissant testé (Claude Opus) a répondu juste aux 52
  questions**, a signalé les 8 ambiguïtés et a refusé les 6 questions sans
  réponse, pour environ 2 centimes par question.
- **Un modèle plus petit (Claude Haiku) montre l'intérêt de la description
  de la base.** Sans les règles écrites à la main, il répond juste à environ
  4 questions sur 10. Avec elles, à environ 9 sur 10.
- **Presque toutes les erreurs sont invisibles.** L'assistant n'échoue
  presque jamais de façon visible ; quand il se trompe, il donne un chiffre
  faux qui a l'air juste.
- **Laisser l'assistant vérifier dans la base corrige certaines erreurs, pas
  toutes.** Il retrouve seul l'orthographe exacte d'un nom. Il n'est pas
  averti quand il oublie une règle, comme les buts contre son camp, et
  continue à l'oublier.
- **L'examen a révélé un défaut dans les données d'origine** : dans la
  composition d'équipe de la finale, le nom de N'Golo Kanté est écrit d'une
  autre façon qu'ailleurs, ce qui fait compter un joueur de trop si l'on
  compte par nom.
- **Limite** : ces questions sont devenues trop faciles pour les modèles les
  plus puissants. Pour les départager, il faudrait des questions plus
  difficiles, ou des données que ces modèles n'ont jamais vues.

## En une phrase

Un assistant qui répond en français à des questions sur des données, et
surtout une méthode pour vérifier qu'il dit vrai, et repérer ses erreurs
quand elles ne se voient pas.
