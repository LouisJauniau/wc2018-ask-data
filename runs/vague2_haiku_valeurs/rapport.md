# Run vague2_haiku_valeurs

| Paramètre | Valeur |
|---|---|
| fournisseur / modèle | rejeu / haiku-sous-agent |
| variante du prompt | valeurs |
| mode | direct |
| répétitions | 1 |
| jeu / prompt | 7a8956439f6a / 3ec955e03233 |
| date | 2026-10-06T15:32:12 |

Réponses rejouées depuis un fichier. Lignes illisibles : 0. Corrections de format : aucune.

## Synthèse

| Mesure | Effectif (IC 95 %) |
|---|---|
| **Exactitude**, questions répondables | 30/52 (58 %) [44-70] |
| **Faux silencieux** : s'exécute, renvoie un faux résultat | 20/52 (38 %) [26-52] |
| Part de faux parmi les réponses qui s'exécutent | 20/50 (40 %) [28-54] |
| Erreurs d'exécution (requête finale) | 1/52 (2 %) [0-10] |
| Abstentions à tort | 1/52 (2 %) [0-10] |
| Ambiguïtés signalées | 0/8 (0 %) [0-32] |
| Réponse conforme à une interprétation (ambiguës) | 6/7 (86 %) [49-97] |
| Faux signalements : question claire jugée ambiguë | 10/52 (19 %) [11-32] |
| Hors périmètre : abstention juste | 5/6 (83 %) [44-97] |
| Hors périmètre : réponse inventée | 1/6 (17 %) [3-56] |
| Incidents (pas de réponse, refus, exception) | 0 |

Jetons : 0 en entrée, 0 lus en cache, 0 en sortie, 0 appels. Durée moyenne par question : 0.0 s.

## Par split

| Split | Exactitude | Faux silencieux | Ambiguïtés signalées | Hors périmètre refusé |
|---|---|---|---|---|
| dev | 14/27 (52 %) [34-69] | 12/27 (44 %) | 0/4 (0 %) | 3/3 (100 %) |
| test | 16/25 (64 %) [45-80] | 8/25 (32 %) | 0/4 (0 %) | 2/3 (67 %) |

## Par catégorie

| Catégorie | Justes | Faux silencieux | Erreurs |
|---|---|---|---|
| classement | 13/18 (72 %) | 5 | 0 |
| comptage | 14/25 (56 %) | 11 | 0 |
| liste | 2/4 (50 %) | 1 | 0 |
| ratio | 1/5 (20 %) | 3 | 1 |

## Par piège

Taux d'échec des questions répondables qui portent le piège. Une question porte souvent plusieurs pièges : ces lignes ne s'additionnent pas.

| Piège | Questions | Échecs |
|---|---|---|
| accents | 2 | 2/2 (100 %) |
| cartons_deux_types | 1 | 1/1 (100 %) |
| geometrie_surface | 1 | 1/1 (100 %) |
| nom_complet | 1 | 1/1 (100 %) |
| jsonb_tableau | 1 | 1/1 (100 %) |
| csc | 6 | 5/6 (83 %) |
| periode_ou_minute | 3 | 2/3 (67 %) |
| buts_par_le_score | 3 | 2/3 (67 %) |
| seance_tab | 17 | 11/17 (65 %) |
| jsonb | 2 | 1/2 (50 %) |
| noms_en_anglais | 9 | 4/9 (44 %) |
| ratio | 5 | 2/5 (40 %) |
| passe_reussie_null | 5 | 2/5 (40 %) |
| table_derivee | 3 | 1/3 (33 %) |
| domicile_exterieur | 5 | 1/5 (20 %) |
| libelle_stage | 3 | 0/3 (0 %) |
| faute_commise_ou_subie | 2 | 0/2 (0 %) |
| convention_cadre | 2 | 0/2 (0 %) |
| convention_corner | 1 | 0/1 (0 %) |
| normalisation_par_match | 1 | 0/1 (0 %) |
| egalite | 1 | 0/1 (0 %) |
| adversaire | 1 | 0/1 (0 %) |

## Forme des faux silencieux

| Diagnostic | Nombre |
|---|---|
| valeurs | 15 |
| vide | 2 |
| entites | 2 |
| cardinalite | 1 |

## Détail des échecs

### but_plus_rapide (rép. 0) : faux_silencieux, vide

aucune ligne obtenue \| attendu ('joueur', 'match_seconds') [['Mathias Jørgensen Jatta', 57]] \| obtenu ('player_name',) []

```sql
WITH earliest_goal AS (SELECT MIN(e.minute) as min_minute, MIN(e.second) as min_second FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id WHERE s.outcome = 'Goal') SELECT DISTINCT p.player_name FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id JOIN sb.players p ON e.player_id = p.player_id, earliest_goal eg WHERE s.outcome = 'Goal' AND e.minute = eg.min_minute AND e.second = eg.min_second
```

### buteurs_distincts (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buteurs \| attendu ('n_buteurs',) [[110]] \| obtenu ('nb_buteurs',) [[123]]

```sql
SELECT COUNT(DISTINCT e.player_id) as nb_buteurs FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id WHERE s.outcome = 'Goal'
```

### buts_coup_franc (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('n_buts',) [[6]] \| obtenu ('direct_free_kick_goals',) [[8]]

```sql
SELECT COUNT(*) as direct_free_kick_goals FROM sb.passes WHERE pass_type = 'Free Kick' AND goal_assist = true
```

### buts_france (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('n_buts',) [[14]] \| obtenu ('nb_buts',) [[12]]

```sql
SELECT COUNT(*) as nb_buts FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id JOIN sb.teams t ON e.team_id = t.team_id WHERE t.team_name = 'France' AND s.outcome = 'Goal'
```

### buts_temps_additionnel (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('n_buts',) [[19]] \| obtenu ('nb_buts',) [[96]]

```sql
SELECT COUNT(*) as nb_buts FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id WHERE s.outcome = 'Goal' AND e.period = 2 AND e.minute >= 45
```

### buts_total (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('n_buts',) [[169]] \| obtenu ('total_goals',) [[183]]

```sql
SELECT COUNT(*) as total_goals FROM sb.shots WHERE outcome = 'Goal'
```

### cartons_jaunes (rép. 0) : non_signalee

```sql
SELECT COUNT(*) as nb_cartons FROM sb.events WHERE (type = 'Bad Behaviour' AND (details #>> '{bad_behaviour,card,name}') = 'Yellow Card') OR (type = 'Foul Committed' AND (details #>> '{foul_committed,card,name}') = 'Yellow Card')
```

### classement_xg_top5 (rép. 0) : faux_silencieux, entites

introuvable dans le resultat : joueur \| attendu ('joueur', 'xg') [['Neymar da Silva Santos Junior', 4.178492526], ['Harry Kane', 4.027905531], ['Antoine Griezmann', 3.556915921]] \| obtenu ('player_name', 'total_xg') [['Harry Kane', 4.811405531], ['Neymar da Silva Santos Junior', 4.178492526], ['Antoine Griezmann', 3.556915921]]

```sql
SELECT pl.player_name, SUM(sh.statsbomb_xg) as total_xg FROM sb.shots sh JOIN sb.events e ON sh.event_id = e.event_id JOIN sb.players pl ON e.player_id = pl.player_id GROUP BY pl.player_id, pl.player_name ORDER BY total_xg DESC LIMIT 5
```

### distance_parcourue (rép. 0) : hallucination

```sql
WITH distances AS (SELECT pl.player_id, pl.player_name, SUM(sqrt(power(c.end_x - e.loc_x, 2) + power(c.end_y - e.loc_y, 2))) as total_distance FROM sb.carries c JOIN sb.events e ON c.event_id = e.event_id JOIN sb.players pl ON e.player_id = pl.player_id WHERE e.loc_x IS NOT NULL AND e.loc_y IS NOT NULL GROUP BY pl.player_id, pl.player_name) SELECT player_name, total_distance FROM distances WHERE total_distance = (SELECT MAX(total_distance) FROM distances)
```

### duree_possession (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : duree_moyenne \| attendu ('duree_moyenne',) [[21.08106169296987]] \| obtenu ('duree_moyenne',) [[20.995981784087864]]

```sql
SELECT AVG(p.duration_seconds) as duree_moyenne FROM sb.possessions p
```

### equipe_plus_xg (rép. 0) : faux_silencieux, entites

introuvable dans le resultat : equipe \| attendu ('equipe', 'xg') [['Belgium', 12.7244262895]] \| obtenu ('team_name', 'total_xg') [['Croatia', 19.0870290802], ['England', 15.7975037083], ['Belgium', 12.7039656315]]

```sql
SELECT t.team_name, SUM(p.sum_xg) as total_xg FROM sb.possessions p JOIN sb.teams t ON p.team_id = t.team_id GROUP BY t.team_name ORDER BY total_xg DESC
```

### joueurs_expulses (rép. 0) : faux_silencieux, cardinalite

2 lignes obtenues, 4 attendues \| attendu ('joueur',) [['Carlos Alberto Sánchez Moreno'], ['Igor Smolnikov'], ['Jérôme Boateng']] \| obtenu ('player_name',) [['Carlos Alberto Sánchez Moreno'], ['Michael Lang']]

```sql
SELECT DISTINCT pl.player_name FROM sb.events e JOIN sb.players pl ON e.player_id = pl.player_id WHERE e.type = 'Foul Committed' AND e.details -> 'foul_committed' -> 'card' ->> 'name' = 'Red Card' ORDER BY pl.player_name
```

### matchs_nuls (rép. 0) : non_signalee

```sql
SELECT COUNT(*) as nb_nuls FROM sb.matches WHERE home_score = away_score
```

### meilleur_buteur (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('joueur', 'n_buts') [['Harry Kane', 6]] \| obtenu ('player_name', 'goals') [['Harry Kane', 7]]

```sql
WITH goals AS (SELECT pl.player_id, pl.player_name, COUNT(*) as goals FROM sb.shots sh JOIN sb.events e ON sh.event_id = e.event_id JOIN sb.players pl ON e.player_id = pl.player_id WHERE sh.outcome = 'Goal' GROUP BY pl.player_id, pl.player_name) SELECT player_name, goals FROM goals WHERE goals = (SELECT MAX(goals) FROM goals)
```

### meilleur_joueur (rép. 0) : non_signalee

### meilleur_passeur (rép. 0) : non_signalee

```sql
SELECT p.player_name, COUNT(*) as nb_passes_decisives FROM sb.passes pa JOIN sb.events e ON pa.event_id = e.event_id JOIN sb.players p ON e.player_id = p.player_id WHERE pa.goal_assist = true GROUP BY p.player_name ORDER BY nb_passes_decisives DESC
```

### meilleure_defense (rép. 0) : non_signalee

```sql
WITH goals_conceded AS ((SELECT home_team_id as team_id, SUM(away_score) as goals_conceded FROM sb.matches GROUP BY home_team_id) UNION ALL (SELECT away_team_id as team_id, SUM(home_score) as goals_conceded FROM sb.matches GROUP BY away_team_id)), team_defense AS (SELECT t.team_id, t.team_name, SUM(gc.goals_conceded) as total_conceded FROM goals_conceded gc JOIN sb.teams t ON gc.team_id = t.team_id GROUP BY t.team_id, t.team_name) SELECT team_name, total_conceded FROM team_defense WHERE total_conceded = (SELECT MIN(total_conceded) FROM team_defense)
```

### nb_csc (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_csc \| attendu ('n_csc',) [[12]] \| obtenu ('nb_own_goals',) [[24]]

```sql
SELECT COUNT(*) as nb_own_goals FROM sb.events WHERE type IN ('Own Goal For', 'Own Goal Against')
```

### part_buts_premiere_periode (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : part \| attendu ('part',) [[0.38461538461538464]] \| obtenu ('first_half_goal_ratio',) [[0.31693989071038253]]

```sql
SELECT COUNT(CASE WHEN e.period = 1 THEN 1 END)::float / COUNT(*) as first_half_goal_ratio FROM sb.shots sh JOIN sb.events e ON sh.event_id = e.event_id WHERE sh.outcome = 'Goal'
```

### passes_dec_hazard (rép. 0) : non_signalee

```sql
SELECT pl.player_name, COUNT(*) as assists FROM sb.passes p JOIN sb.events e ON p.event_id = e.event_id JOIN sb.players pl ON e.player_id = pl.player_id WHERE pl.player_name = 'Hazard' AND p.goal_assist = true GROUP BY pl.player_id, pl.player_name
```

### passes_modric (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_passes \| attendu ('n_passes',) [[430]] \| obtenu ('nb_passes',) [[0]]

```sql
SELECT COUNT(*) as nb_passes FROM sb.passes p JOIN sb.events e ON p.event_id = e.event_id JOIN sb.players pl ON e.player_id = pl.player_id WHERE pl.player_name = 'Luka Modric' AND (p.outcome IS NULL OR p.outcome NOT IN ('Incomplete', 'Out', 'Unknown', 'Pass Offside', 'Injury Clearance'))
```

### penalties_transformes (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_penalties_marques \| attendu ('n_penalties_marques',) [[22]] \| obtenu ('nb_penalties',) [[48]]

```sql
SELECT COUNT(*) as nb_penalties FROM sb.shots s WHERE s.shot_type = 'Penalty' AND s.outcome = 'Goal'
```

### possession_dominante (rép. 0) : non_signalee

```sql
SELECT t.team_name, SUM(p.duration_seconds) as total_possession FROM sb.possessions p JOIN sb.teams t ON p.team_id = t.team_id GROUP BY t.team_name ORDER BY total_possession DESC
```

### taux_passes_espagne (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : taux \| attendu ('taux',) [[0.8938961779806047]] \| obtenu ('taux',) [[0.9125]]

```sql
SELECT ROUND(SUM(p.n_passes_reussies)::numeric / SUM(p.n_passes_tentees), 4) as taux FROM sb.possessions p JOIN sb.teams t ON p.team_id = t.team_id WHERE t.team_name = 'Spain'
```

### tirs_croatie (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_tirs \| attendu ('n_tirs',) [[114]] \| obtenu ('nb_tirs',) [[124]]

```sql
SELECT COUNT(*) as nb_tirs FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id JOIN sb.teams t ON e.team_id = t.team_id WHERE t.team_name = 'Croatia'
```

### tirs_hors_surface (rép. 0) : faux_silencieux, vide

aucune ligne obtenue \| attendu ('equipe', 'n_tirs') [['Croatia', 54]] \| obtenu ('team_name', 'nb_tirs') []

```sql
SELECT t.team_name, COUNT(*) as nb_tirs FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id JOIN sb.teams t ON e.team_id = t.team_id WHERE s.end_x < 83 GROUP BY t.team_name ORDER BY nb_tirs DESC
```

### tirs_mbappe (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_tirs \| attendu ('n_tirs',) [[8]] \| obtenu ('shots',) [[0]]

```sql
SELECT COUNT(*) as shots FROM sb.shots sh JOIN sb.events e ON sh.event_id = e.event_id JOIN sb.players pl ON e.player_id = pl.player_id WHERE pl.player_name LIKE '%Mbappe%'
```

### tirs_par_match (rép. 0) : erreur_execution, 42703: ERROR:  column "match_id" does not exist

```sql
SELECT COUNT(*)::float / (SELECT COUNT(DISTINCT match_id) FROM sb.shots) as avg_shots_per_match FROM sb.shots
```

### titulaires_france (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_joueurs \| attendu ('n_joueurs',) [[18]] \| obtenu ('unique_starting_players',) [[23]]

```sql
SELECT COUNT(DISTINCT player_id) as unique_starting_players FROM sb.lineups WHERE team_id = (SELECT team_id FROM sb.teams WHERE team_name = 'France')
```

### vainqueurs_tab (rép. 0) : abstention_a_tort, hors_perimetre

### victoires_russie (rép. 0) : non_signalee

```sql
SELECT COUNT(*) as wins FROM sb.matches WHERE (home_team_id = (SELECT team_id FROM sb.teams WHERE team_name = 'Russia') AND home_score > away_score) OR (away_team_id = (SELECT team_id FROM sb.teams WHERE team_name = 'Russia') AND away_score > home_score)
```

