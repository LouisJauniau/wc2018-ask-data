# Catalogue des pièges

Chaque question du jeu porte la liste des pièges qu'elle met à l'épreuve. Le
rapport d'un run donne le taux d'échec par piège : c'est ce qui permet de
dire *pourquoi* un modèle se trompe, et pas seulement combien de fois.

Un piège est une raison identifiée pour laquelle une requête plausible,
syntaxiquement juste, renvoie un résultat faux. La plupart ne produisent
aucune erreur : ce sont eux qui fabriquent les faux silencieux.

## Conventions du format StatsBomb

**`seance_tab`** : la séance de tirs au but est stockée comme une période 5,
et ses tirs au but comme des tirs ordinaires (`shot_type = 'Penalty'`).
Oublier `period < 5` gonfle les tirs, les penalties, l'xG et les buts des
joueurs. Kane passe de 6 à 7 buts ; la Croatie, deux séances, passe de 11,6
à 19,5 xG et devient « l'équipe qui a cumulé le plus d'xG » à la place de la
Belgique.

**`csc`** : un but contre son camp n'est pas un tir. Il apparaît deux fois
dans les événements, `Own Goal Against` et `Own Goal For`. Compter les buts à
partir des tirs les oublie (12 sur 169) ; compter les deux types d'événement
les compte double.

**`buts_par_le_score`** : le score d'un match est dans `matches`. Le
recalculer depuis les tirs oublie les csc et ajoute les tirs au but.

**`passe_reussie_null`** : une passe réussie a `outcome` NULL. Il n'existe pas
de valeur 'Complete'. `WHERE outcome = 'Complete'` renvoie zéro passe, sans
erreur.

**`periode_ou_minute`** : `minute` est cumulée depuis le coup d'envoi.
`minute >= 90` capte le temps additionnel de la seconde période et toutes les
prolongations à la fois. Il faut la période et la minute.

**`convention_cadre`** : un tir cadré est 'Goal' ou 'Saved'. Un poteau n'est
pas cadré, un tir contré non plus.

**`convention_corner`** : un corner est une passe avec `pass_type = 'Corner'`,
pas un `play_pattern = 'From Corner'`, qui marque toutes les actions qui
suivent un corner.

**`jsonb`** : les cartons, l'issue des dribbles et les détails des gardiens
sont dans `events.details`. Il faut connaître le chemin.

**`jsonb_tableau`** : les onze de départ sont un tableau jsonb à déplier avec
`jsonb_array_elements`.

**`cartons_deux_types`** : un carton peut suivre une faute (`Foul Committed`)
ou un comportement (`Bad Behaviour`). Ne regarder que les fautes perd 40
cartons jaunes sur 205.

**`table_derivee`** : `sb.possessions` est dérivée des événements. Elle
contient les possessions de la séance de tirs au but, et ses booléens
(`reached_final_third`, `produced_shot`) dispensent de refaire la géométrie.

## Structure des données

**`domicile_exterieur`** : une équipe joue comme `home_team_id` ou comme
`away_team_id`. Filtrer sur une seule colonne divise les matchs par deux,
sans erreur.

**`adversaire`** : « concédé » demande les événements de l'autre équipe dans
les matchs de l'équipe visée, donc une jointure sur le match et une
condition d'inégalité.

**`faute_commise_ou_subie`** : `Foul Committed` et `Foul Won` existent tous
les deux, avec des volumes proches.

**`normalisation_par_match`** : « par match » demande le nombre de matchs de
chaque équipe, qui va de 3 à 7.

**`libelle_stage`** : la finale est `stage = 'Final'`. `LIKE '%Final%'` attrape
aussi les quarts, les demies et le match pour la troisième place.

**`geometrie_surface`** : la surface de réparation se définit par des
coordonnées (x >= 102, y entre 18 et 62). Les bornes exactes changent
quelques tirs ; les questions de ce type ne vérifient que l'équipe, pas le
compte.

**`ratio`** : division entière (`count(*) / 64` vaut 26, pas 26,05), part
ou pourcentage, dénominateur.

**`egalite`** : plusieurs lignes ex aequo en tête. Trois matchs finissent
avec 7 buts ; un `LIMIT 1` en montre un, au hasard du plan d'exécution.

## Noms

**`noms_en_anglais`** : 'Germany', pas 'Allemagne'. Un nom français filtre
tout, et `count(*)` renvoie 0 ou `sum()` renvoie NULL : un résultat, pas une
erreur.

**`accents`** : 'Luka Modrić', 'Kylian Mbappé Lottin'. `ILIKE '%modric%'` ne
trouve rien.

**`nom_complet`** : StatsBomb stocke les noms complets ('Neymar da Silva Santos
Junior'). Une égalité stricte sur le nom d'usage échoue.

**`homonymes`** : Eden et Thorgan Hazard. `ILIKE '%Hazard%'` les additionne.

## Questions ambiguës et hors périmètre

**`subjectif`** : aucune colonne ne mesure « le meilleur ». Un choix de
critère est nécessaire, et doit être dit.

**`donnee_approchante`** : la base contient une donnée voisine qui tente
l'approximation : la longueur des conduites pour la distance parcourue,
l'édition 2018 pour une question sur 2022, le xG pour la puissance d'un tir.
Répondre avec elle, c'est inventer.
