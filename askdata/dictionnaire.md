## Dictionnaire de données : conventions à connaître

Source : données ouvertes StatsBomb, Coupe du monde masculine 2018, 64 matchs.
Les noms de colonnes et les valeurs textuelles sont ceux de StatsBomb, en
anglais.

### Équipes, joueurs, matchs
- Les noms d'équipes sont en anglais : 'Germany', 'Spain', 'South Korea'.
- Les noms de joueurs sont des noms complets, avec accents et parfois noms
  de famille multiples : un joueur connu sous un nom court peut être stocké
  sous un nom plus long. Pour retrouver un joueur, chercher d'abord avec
  ILIKE sur une partie du nom et vérifier le nom exact. Les accents comptent
  pour ILIKE ('é' ne correspond pas à 'e').
- Une équipe joue un match soit comme home_team_id, soit comme away_team_id.
  « Domicile » et « extérieur » n'ont pas de sens sportif ici (tournoi en
  terrain neutre), mais il faut toujours regarder les deux colonnes.
- matches.stage vaut exactement 'Final' pour la finale ; '3rd Place Final'
  est le match pour la troisième place.

### Temps de jeu
- period : 1 et 2 pour les mi-temps, 3 et 4 pour les prolongations,
  5 pour la séance de tirs au but.
- **Sauf mention contraire, une statistique de jeu exclut la séance de tirs
  au but (period = 5)** : tirs, xG, buts d'un joueur, penalties, arrêts.
  C'est la convention des statistiques officielles. Les tirs au but sont
  stockés comme des tirs (sb.shots, shot_type = 'Penalty').
- Aucune colonne ne dit qu'un match est allé aux tirs au but : un match a
  eu une séance si et seulement s'il a des événements en period = 5. Le
  vainqueur est l'équipe qui y marque le plus.
- minute est cumulée depuis le coup d'envoi : la 47e minute est en seconde
  période. Le temps additionnel d'une période se repère par la période ET la
  minute (period = 2 et minute >= 90), jamais par la minute seule, car les
  prolongations ont aussi des minutes supérieures à 90.
- match_seconds = minute * 60 + second, utile pour ordonner un match.

### Buts
- Score d'un match, buts marqués ou encaissés par une équipe : utiliser
  matches.home_score et matches.away_score. Ils comptent les prolongations
  et les buts contre son camp, et ne comptent pas la séance de tirs au but.
- Buts d'un joueur : sb.shots avec outcome = 'Goal', hors period = 5.
- Un but contre son camp n'est pas un tir. Il apparaît deux fois dans
  sb.events : type 'Own Goal Against' (équipe et joueur qui marquent contre
  leur camp) et type 'Own Goal For' (équipe qui en bénéficie). Pour compter
  les buts à partir des événements : tirs marqués + 'Own Goal Against'.

### Tirs
- sb.shots.outcome : 'Goal', 'Saved' (arrêté), 'Off T' (à côté), 'Post'
  (poteau), 'Blocked' (contré), 'Wayward' (raté).
- Un tir cadré a outcome IN ('Goal', 'Saved'). Un poteau n'est pas cadré.
- statsbomb_xg est la probabilité de but estimée par StatsBomb, entre 0 et 1.

### Terrain et coordonnées
- Terrain de 120 x 80. Chaque événement est décrit du point de vue de
  l'équipe qui le réalise, qui attaque vers x = 120.
- Surface de réparation adverse : loc_x >= 102 et loc_y entre 18 et 62,
  lignes comprises. « Hors de la surface » est la négation de cette condition.
- Dernier tiers adverse : loc_x >= 80.

### Passes
- **sb.passes.outcome NULL signifie passe réussie.** Les valeurs non nulles
  ('Incomplete', 'Out', 'Pass Offside', 'Unknown', 'Injury Clearance') sont
  des échecs ou des cas particuliers.
- goal_assist : passe décisive. shot_assist : passe qui amène un tir.
- Un corner est une passe avec pass_type = 'Corner'.

### Actions de l'équipe
- events.team_id est l'équipe qui réalise l'action. possession_team_id est
  l'équipe en possession du ballon au même moment ; ce n'est pas la même
  chose (un tacle est réalisé par l'équipe qui n'a pas le ballon).
- Fautes : type 'Foul Committed' pour la faute commise, 'Foul Won' pour la
  faute subie.

### Cartons
- Ils sont dans le jsonb, sous deux types d'événements :
  details -> 'foul_committed' -> 'card' ->> 'name' (type 'Foul Committed')
  et details -> 'bad_behaviour' -> 'card' ->> 'name' (type 'Bad Behaviour',
  carton sans faute, par exemple pour contestation).
- Valeurs : 'Yellow Card', 'Second Yellow' (second avertissement, qui vaut
  expulsion), 'Red Card' (rouge direct).

### Compositions
- sb.lineups liste tous les joueurs de la feuille de match, remplaçants non
  entrés compris : ce n'est pas la liste des joueurs qui ont joué.
- Les onze de départ sont dans les événements de type 'Starting XI' :
  details -> 'tactics' -> 'lineup' est un tableau jsonb d'objets
  {player: {id, name}, position: {id, name}, jersey_number}.
- Remplacements : type 'Substitution', le joueur entrant est dans
  details -> 'substitution' -> 'replacement'.

### Table dérivée sb.possessions
Une ligne par possession (numérotation StatsBomb), dérivée des événements.
- team_id : équipe en possession. duration_seconds : durée.
- reached_final_third, reached_box, produced_shot, produced_goal : la
  possession a-t-elle atteint le dernier tiers, la surface, produit un tir,
  un but. funnel_stage résume : 0 rien, 1 dernier tiers, 2 surface, 3 tir,
  4 but.
- Les possessions de la séance de tirs au but sont en period = 5.
