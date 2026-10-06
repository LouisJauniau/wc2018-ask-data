# Run vague1_haiku_brut

| Paramètre | Valeur |
|---|---|
| fournisseur / modèle | rejeu / haiku-sous-agent |
| variante du prompt | brut |
| mode | direct |
| répétitions | 1 |
| jeu / prompt | 7a8956439f6a / e1eccf5679a5 |
| date | 2026-10-06T15:25:29 |

Réponses rejouées depuis un fichier. Lignes illisibles : 0. Corrections de format : statut 'ok' -> reponse (30), statut 'success' -> reponse (25).

## Synthèse

| Mesure | Effectif (IC 95 %) |
|---|---|
| **Exactitude**, questions répondables | 20/52 (38 %) [26-52] |
| **Faux silencieux** : s'exécute, renvoie un faux résultat | 25/52 (48 %) [35-61] |
| Part de faux parmi les réponses qui s'exécutent | 25/45 (56 %) [41-69] |
| Erreurs d'exécution (requête finale) | 2/52 (4 %) [1-13] |
| Abstentions à tort | 5/52 (10 %) [4-21] |
| Ambiguïtés signalées | 2/8 (25 %) [7-59] |
| Réponse conforme à une interprétation (ambiguës) | 4/7 (57 %) [25-84] |
| Faux signalements : question claire jugée ambiguë | 6/52 (12 %) [5-23] |
| Hors périmètre : abstention juste | 5/6 (83 %) [44-97] |
| Hors périmètre : réponse inventée | 1/6 (17 %) [3-56] |
| Incidents (pas de réponse, refus, exception) | 0 |

Jetons : 0 en entrée, 0 lus en cache, 0 en sortie, 0 appels. Durée moyenne par question : 0.0 s.

## Par split

| Split | Exactitude | Faux silencieux | Ambiguïtés signalées | Hors périmètre refusé |
|---|---|---|---|---|
| dev | 12/27 (44 %) [28-63] | 13/27 (48 %) | 1/4 (25 %) | 3/3 (100 %) |
| test | 8/25 (32 %) [17-52] | 12/25 (48 %) | 1/4 (25 %) | 2/3 (67 %) |

## Par catégorie

| Catégorie | Justes | Faux silencieux | Erreurs |
|---|---|---|---|
| classement | 9/18 (50 %) | 6 | 1 |
| comptage | 9/25 (36 %) | 14 | 0 |
| liste | 1/4 (25 %) | 2 | 0 |
| ratio | 1/5 (20 %) | 3 | 1 |

## Par piège

Taux d'échec des questions répondables qui portent le piège. Une question porte souvent plusieurs pièges : ces lignes ne s'additionnent pas.

| Piège | Questions | Échecs |
|---|---|---|
| csc | 6 | 6/6 (100 %) |
| periode_ou_minute | 3 | 3/3 (100 %) |
| jsonb | 2 | 2/2 (100 %) |
| accents | 2 | 2/2 (100 %) |
| normalisation_par_match | 1 | 1/1 (100 %) |
| cartons_deux_types | 1 | 1/1 (100 %) |
| egalite | 1 | 1/1 (100 %) |
| nom_complet | 1 | 1/1 (100 %) |
| jsonb_tableau | 1 | 1/1 (100 %) |
| passe_reussie_null | 5 | 4/5 (80 %) |
| seance_tab | 17 | 13/17 (76 %) |
| buts_par_le_score | 3 | 2/3 (67 %) |
| table_derivee | 3 | 2/3 (67 %) |
| noms_en_anglais | 9 | 5/9 (56 %) |
| faute_commise_ou_subie | 2 | 1/2 (50 %) |
| domicile_exterieur | 5 | 2/5 (40 %) |
| ratio | 5 | 2/5 (40 %) |
| libelle_stage | 3 | 1/3 (33 %) |
| convention_cadre | 2 | 0/2 (0 %) |
| convention_corner | 1 | 0/1 (0 %) |
| adversaire | 1 | 0/1 (0 %) |
| geometrie_surface | 1 | 0/1 (0 %) |

## Forme des faux silencieux

| Diagnostic | Nombre |
|---|---|
| valeurs | 19 |
| vide | 3 |
| entites | 2 |
| cardinalite | 1 |

## Détail des échecs

### but_plus_rapide (rép. 0) : faux_silencieux, vide

aucune ligne obtenue \| attendu ('joueur', 'match_seconds') [['Mathias Jørgensen Jatta', 57]] \| obtenu ('player_name',) []

```sql
WITH goal_times AS (SELECT p.player_name, COALESCE(e.minute, 0) * 60 + COALESCE(e.second, 0) as total_seconds FROM sb.events e JOIN sb.players p ON e.player_id = p.player_id WHERE e.type = 'Shot' AND e.details->>'outcome' = 'Goal') SELECT player_name FROM goal_times WHERE total_seconds = (SELECT MIN(total_seconds) FROM goal_times);
```

### buteurs_distincts (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buteurs \| attendu ('n_buteurs',) [[110]] \| obtenu ('nb_scorers',) [[0]]

```sql
SELECT COUNT(DISTINCT e.player_id) as nb_scorers FROM sb.events e WHERE e.type = 'Shot' AND e.details->>'outcome' = 'Goal';
```

### buts_coup_franc (rép. 0) : abstention_a_tort, hors_perimetre

### buts_france (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('n_buts',) [[14]] \| obtenu ('buts',) [[0]]

```sql
SELECT COUNT(*) as buts FROM sb.events e JOIN sb.teams t ON e.team_id = t.team_id WHERE t.team_name = 'France' AND e.type = 'Shot' AND e.details->>'outcome' = 'Goal';
```

### buts_prolongation (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('n_buts',) [[3]] \| obtenu ('extra_time_goals',) [[29]]

```sql
SELECT COUNT(*) as extra_time_goals FROM sb.shots WHERE (outcome = 'Goal') AND (SELECT e.period FROM sb.events e WHERE e.event_id = sb.shots.event_id) > 2
```

### buts_temps_additionnel (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('n_buts',) [[19]] \| obtenu ('buts_additionnel_p2',) [[0]]

```sql
SELECT COUNT(*) as buts_additionnel_p2 FROM sb.events e WHERE e.type = 'Shot' AND e.details->>'outcome' = 'Goal' AND e.period = 2 AND EXTRACT(EPOCH FROM e.timestamp_in_period) > 2700;
```

### buts_total (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('n_buts',) [[169]] \| obtenu ('total_goals',) [[183]]

```sql
SELECT COUNT(*) as total_goals FROM sb.shots WHERE outcome = 'Goal'
```

### cartons_jaunes (rép. 0) : non_signalee

```sql
SELECT COUNT(*) as cartons_jaunes FROM sb.events WHERE type = 'Card' AND (details->>'card_type' = 'Yellow Card' OR details->>'card_type' = 'yellow card');
```

### classement_xg_top5 (rép. 0) : faux_silencieux, entites

introuvable dans le resultat : joueur \| attendu ('joueur', 'xg') [['Neymar da Silva Santos Junior', 4.178492526], ['Harry Kane', 4.027905531], ['Antoine Griezmann', 3.556915921]] \| obtenu ('player_name', 'total_xg') [['Harry Kane', 4.811405531], ['Neymar da Silva Santos Junior', 4.178492526], ['Antoine Griezmann', 3.556915921]]

```sql
SELECT p.player_name, SUM(s.statsbomb_xg) as total_xg FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id JOIN sb.players p ON e.player_id = p.player_id GROUP BY p.player_id, p.player_name ORDER BY total_xg DESC LIMIT 5
```

### distance_parcourue (rép. 0) : hallucination

```sql
SELECT p.player_name, COALESCE(SUM(ps.length), 0) + COALESCE(SUM(SQRT(POWER(c.end_x - e.loc_x, 2) + POWER(c.end_y - e.loc_y, 2))), 0) as total_distance FROM sb.players p LEFT JOIN sb.passes ps ON p.player_id = ps.recipient_id OR ps.recipient_id IS NULL LEFT JOIN sb.events e ON e.player_id = p.player_id LEFT JOIN sb.carries c ON c.event_id = e.event_id GROUP BY p.player_id, p.player_name ORDER BY total_distance DESC LIMIT (SELECT COUNT(*) FROM sb.players WHERE player_id IN (SELECT player_id FROM sb.events WHERE type = 'Pass' OR type = 'Carry') ORDER BY 1 LIMIT 1)
```

### dribbles_reussis (rép. 0) : abstention_a_tort, hors_perimetre

### duree_possession (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : duree_moyenne \| attendu ('duree_moyenne',) [[21.08106169296987]] \| obtenu ('duration_moyenne',) [[20.995981784087864]]

```sql
SELECT AVG(p.duration_seconds) as duration_moyenne FROM sb.possessions p WHERE p.play_pattern != 'Penalty Shootout' OR p.period < 5;
```

### equipe_plus_xg (rép. 0) : faux_silencieux, entites

introuvable dans le resultat : equipe \| attendu ('equipe', 'xg') [['Belgium', 12.7244262895]] \| obtenu ('team_name', 'total_xg') [['Croatia', 19.4774227802]]

```sql
WITH xg_by_team AS (SELECT t.team_name, SUM(s.statsbomb_xg) as total_xg FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id JOIN sb.teams t ON e.team_id = t.team_id GROUP BY t.team_name) SELECT team_name, total_xg FROM xg_by_team WHERE total_xg = (SELECT MAX(total_xg) FROM xg_by_team);
```

### fautes_par_match (rép. 0) : abstention_a_tort, hors_perimetre

### joueurs_expulses (rép. 0) : abstention_a_tort, hors_perimetre

### match_plus_buts (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : match_id \| attendu ('match_id', 'equipe_domicile', 'equipe_exterieur', 'n_buts') [[7554, 'England', 'Panama', 7], [7580, 'France', 'Argentina', 7], [7552, 'Belgium', 'Tunisia', 7]] \| obtenu ('match_desc', 'total_buts') [['England 6-1 Panama', 7], ['France 4-3 Argentina', 7], ['Belgium 5-2 Tunisia', 7]]

```sql
WITH match_totals AS (SELECT m.match_id, (m.home_score + m.away_score) as total_buts, CONCAT(t1.team_name, ' ', m.home_score, '-', m.away_score, ' ', t2.team_name) as match_desc FROM sb.matches m JOIN sb.teams t1 ON m.home_team_id = t1.team_id JOIN sb.teams t2 ON m.away_team_id = t2.team_id) SELECT match_desc, total_buts FROM match_totals WHERE total_buts = (SELECT MAX(total_buts) FROM match_totals);
```

### matchs_nuls (rép. 0) : non_signalee

```sql
SELECT COUNT(*) as nb_nuls FROM sb.matches WHERE home_score = away_score;
```

### meilleur_buteur (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('joueur', 'n_buts') [['Harry Kane', 6]] \| obtenu ('player_name', 'goals') [['Harry Kane', 7]]

```sql
SELECT p.player_name, COUNT(*) as goals FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id JOIN sb.players p ON e.player_id = p.player_id WHERE s.outcome = 'Goal' GROUP BY p.player_id, p.player_name ORDER BY goals DESC LIMIT 1
```

### meilleur_joueur (rép. 0) : non_signalee

### nb_csc (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_csc \| attendu ('n_csc',) [[12]] \| obtenu ('buts_contre_camp',) [[0]]

```sql
SELECT COUNT(*) as buts_contre_camp FROM sb.events e WHERE e.type = 'Shot' AND (e.details->>'own_goal' = 'true' OR e.details->>'own_goal' = 'True');
```

### nb_seances_tab (rép. 0) : abstention_a_tort, hors_perimetre

### part_buts_premiere_periode (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : part \| attendu ('part',) [[0.38461538461538464]] \| obtenu ('pct_goals_period_1',) [[31.69]]

```sql
SELECT ROUND(100.0 * COUNT(CASE WHEN e.period = 1 THEN 1 END) / COUNT(*), 2) as pct_goals_period_1 FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id WHERE s.outcome = 'Goal'
```

### passes_dec_hazard (rép. 0) : non_signalee, 42703: ERROR:  column "player_id" does not exist

```sql
SELECT COUNT(*) as hazard_assists FROM sb.passes WHERE player_id IN (SELECT player_id FROM sb.players WHERE player_name ILIKE '%Hazard%') AND goal_assist = true
```

### passes_modric (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_passes \| attendu ('n_passes',) [[430]] \| obtenu ('passes_reussies',) [[0]]

```sql
SELECT COUNT(*) as passes_reussies FROM sb.passes p JOIN sb.events e ON p.event_id = e.event_id JOIN sb.players pl ON e.player_id = pl.player_id WHERE pl.player_name = 'Luka Modric' AND p.outcome = 'Successful';
```

### passes_profondeur (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_passes \| attendu ('n_passes',) [[42]] \| obtenu ('through_balls_successful',) [[0]]

```sql
SELECT COUNT(*) as through_balls_successful FROM sb.passes WHERE is_through_ball = true AND outcome = 'Successful'
```

### passes_reussies_joueur (rép. 0) : erreur_execution, 42P01: ERROR:  missing FROM-clause entry for table "p"

```sql
SELECT p.player_name, COUNT(*) as passes_completed FROM sb.passes WHERE outcome = 'Successful' GROUP BY (SELECT player_id FROM sb.events WHERE event_id = sb.passes.event_id), p.player_name ORDER BY passes_completed DESC LIMIT 1
```

### pays_plus_buteurs (rép. 0) : faux_silencieux, vide

aucune ligne obtenue \| attendu ('equipe', 'n_buteurs') [['Belgium', 10]] \| obtenu ('team_name', 'nb_scorers') []

```sql
WITH scorers_by_team AS (SELECT t.team_name, COUNT(DISTINCT e.player_id) as nb_scorers FROM sb.events e JOIN sb.teams t ON e.team_id = t.team_id WHERE e.type = 'Shot' AND e.details->>'outcome' = 'Goal' GROUP BY t.team_name) SELECT team_name, nb_scorers FROM scorers_by_team WHERE nb_scorers = (SELECT MAX(nb_scorers) FROM scorers_by_team);
```

### penalties_jeu (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_penalties \| attendu ('n_penalties',) [[29]] \| obtenu ('penalty_attempts',) [[68]]

```sql
SELECT COUNT(*) as penalty_attempts FROM sb.passes WHERE pass_type = 'Penalty' UNION ALL SELECT COUNT(*) FROM sb.shots WHERE (shot_type = 'Penalty' OR shot_type ILIKE '%Penalty%') ORDER BY 1 DESC LIMIT 1
```

### penalties_transformes (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_penalties_marques \| attendu ('n_penalties_marques',) [[22]] \| obtenu ('penalties_scores',) [[0]]

```sql
SELECT COUNT(*) as penalties_scores FROM sb.events e WHERE e.type = 'Shot' AND e.details->>'penalty' = 'true' AND e.details->>'outcome' = 'Goal' AND e.period IN (1, 2);
```

### possession_dominante (rép. 0) : non_signalee

```sql
WITH possession_by_team AS (SELECT t.team_name, SUM(p.duration_seconds) as total_possession_seconds FROM sb.possessions p JOIN sb.teams t ON p.team_id = t.team_id GROUP BY t.team_name) SELECT team_name, total_possession_seconds FROM possession_by_team WHERE total_possession_seconds = (SELECT MAX(total_possession_seconds) FROM possession_by_team);
```

### possessions_tir_belgique (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_possessions \| attendu ('n_possessions',) [[95]] \| obtenu ('belgium_possessions_with_shot',) [[74]]

```sql
SELECT COUNT(DISTINCT pos.possession) as belgium_possessions_with_shot FROM sb.possessions pos WHERE pos.team_id = (SELECT team_id FROM sb.teams WHERE team_name = 'Belgium') AND pos.produced_shot = true
```

### taux_passes_espagne (rép. 0) : erreur_execution, 42883: ERROR:  function round(double precision, integer) does not exist

```sql
WITH spain_passes AS (SELECT COUNT(CASE WHEN p.outcome = 'Successful' THEN 1 END) as successful, COUNT(*) as total FROM sb.passes p JOIN sb.events e ON p.event_id = e.event_id JOIN sb.teams t ON e.team_id = t.team_id WHERE t.team_name = 'Spain') SELECT ROUND((successful::float / NULLIF(total, 0)) * 100, 2) as completion_rate FROM spain_passes;
```

### tirs_croatie (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_tirs \| attendu ('n_tirs',) [[114]] \| obtenu ('nb_tirs',) [[124]]

```sql
SELECT COUNT(*) as nb_tirs FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id JOIN sb.teams t ON e.team_id = t.team_id WHERE t.team_name = 'Croatia';
```

### tirs_mbappe (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_tirs \| attendu ('n_tirs',) [[8]] \| obtenu ('mbappe_shots',) [[0]]

```sql
SELECT COUNT(*) as mbappe_shots FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id JOIN sb.players p ON e.player_id = p.player_id WHERE p.player_name ILIKE '%Mbappe%'
```

### tirs_par_match (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : tirs_par_match \| attendu ('tirs_par_match',) [[26.046875]] \| obtenu ('avg_shots_per_match',) [[26.66]]

```sql
SELECT ROUND(COUNT(*)::numeric / 64, 2) as avg_shots_per_match FROM sb.shots
```

### titulaires_france (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_joueurs \| attendu ('n_joueurs',) [[18]] \| obtenu ('france_distinct_starters',) [[23]]

```sql
SELECT COUNT(DISTINCT l.player_id) as france_distinct_starters FROM sb.lineups l WHERE l.team_id = (SELECT team_id FROM sb.teams WHERE team_name = 'France')
```

### vainqueur (rép. 0) : faux_silencieux, cardinalite

8 lignes obtenues, 1 attendues \| attendu ('equipe',) [['France']] \| obtenu ('team_name',) [['Belgium'], ['Croatia'], ['France']]

```sql
SELECT t.team_name FROM sb.matches m JOIN sb.teams t ON (CASE WHEN m.home_score > m.away_score THEN m.home_team_id ELSE m.away_team_id END) = t.team_id WHERE m.stage ILIKE '%Final%'
```

### vainqueurs_tab (rép. 0) : faux_silencieux, vide

aucune ligne obtenue \| attendu ('equipe', 'n_seances_gagnees') [['Croatia', 2], ['England', 1], ['Russia', 1]] \| obtenu ('team_name', 'goals_in_shootout') []

```sql
WITH shootout_goals AS (SELECT t.team_name, COUNT(*) as goals_in_shootout FROM sb.events e JOIN sb.teams t ON e.team_id = t.team_id WHERE e.period = 5 AND e.type = 'Shot' AND e.details->>'outcome' = 'Goal' GROUP BY t.team_name) SELECT team_name, goals_in_shootout FROM shootout_goals ORDER BY goals_in_shootout DESC;
```

### victoires_russie (rép. 0) : non_signalee

```sql
SELECT COUNT(*) as russia_wins FROM sb.matches WHERE (home_team_id = (SELECT team_id FROM sb.teams WHERE team_name = 'Russia') AND home_score > away_score) OR (away_team_id = (SELECT team_id FROM sb.teams WHERE team_name = 'Russia') AND away_score > home_score)
```

