# Run vague1_haiku_valeurs

| Paramètre | Valeur |
|---|---|
| fournisseur / modèle | rejeu / haiku-sous-agent |
| variante du prompt | valeurs |
| mode | direct |
| répétitions | 1 |
| jeu / prompt | 7a8956439f6a / 3ec955e03233 |
| date | 2026-10-06T15:25:32 |

Réponses rejouées depuis un fichier. Lignes illisibles : 0. Corrections de format : statut 'ok' -> reponse (55).

## Synthèse

| Mesure | Effectif (IC 95 %) |
|---|---|
| **Exactitude**, questions répondables | 29/52 (56 %) [42-68] |
| **Faux silencieux** : s'exécute, renvoie un faux résultat | 17/52 (33 %) [22-46] |
| Part de faux parmi les réponses qui s'exécutent | 17/46 (37 %) [25-51] |
| Erreurs d'exécution (requête finale) | 2/52 (4 %) [1-13] |
| Abstentions à tort | 4/52 (8 %) [3-18] |
| Ambiguïtés signalées | 3/8 (38 %) [14-69] |
| Réponse conforme à une interprétation (ambiguës) | 5/7 (71 %) [36-92] |
| Faux signalements : question claire jugée ambiguë | 7/52 (13 %) [7-25] |
| Hors périmètre : abstention juste | 6/6 (100 %) [61-100] |
| Hors périmètre : réponse inventée | 0/6 (0 %) [0-39] |
| Incidents (pas de réponse, refus, exception) | 0 |

Jetons : 0 en entrée, 0 lus en cache, 0 en sortie, 0 appels. Durée moyenne par question : 0.0 s.

## Par split

| Split | Exactitude | Faux silencieux | Ambiguïtés signalées | Hors périmètre refusé |
|---|---|---|---|---|
| dev | 17/27 (63 %) [44-78] | 9/27 (33 %) | 0/4 (0 %) | 3/3 (100 %) |
| test | 12/25 (48 %) [30-67] | 8/25 (32 %) | 3/4 (75 %) | 3/3 (100 %) |

## Par catégorie

| Catégorie | Justes | Faux silencieux | Erreurs |
|---|---|---|---|
| classement | 13/18 (72 %) | 3 | 2 |
| comptage | 12/25 (48 %) | 10 | 0 |
| liste | 2/4 (50 %) | 1 | 0 |
| ratio | 2/5 (40 %) | 3 | 0 |

## Par piège

Taux d'échec des questions répondables qui portent le piège. Une question porte souvent plusieurs pièges : ces lignes ne s'additionnent pas.

| Piège | Questions | Échecs |
|---|---|---|
| csc | 6 | 6/6 (100 %) |
| normalisation_par_match | 1 | 1/1 (100 %) |
| cartons_deux_types | 1 | 1/1 (100 %) |
| jsonb_tableau | 1 | 1/1 (100 %) |
| seance_tab | 17 | 12/17 (71 %) |
| periode_ou_minute | 3 | 2/3 (67 %) |
| buts_par_le_score | 3 | 2/3 (67 %) |
| jsonb | 2 | 1/2 (50 %) |
| faute_commise_ou_subie | 2 | 1/2 (50 %) |
| accents | 2 | 1/2 (50 %) |
| ratio | 5 | 2/5 (40 %) |
| passe_reussie_null | 5 | 2/5 (40 %) |
| noms_en_anglais | 9 | 3/9 (33 %) |
| table_derivee | 3 | 1/3 (33 %) |
| domicile_exterieur | 5 | 1/5 (20 %) |
| libelle_stage | 3 | 0/3 (0 %) |
| convention_cadre | 2 | 0/2 (0 %) |
| convention_corner | 1 | 0/1 (0 %) |
| egalite | 1 | 0/1 (0 %) |
| adversaire | 1 | 0/1 (0 %) |
| geometrie_surface | 1 | 0/1 (0 %) |
| nom_complet | 1 | 0/1 (0 %) |

## Forme des faux silencieux

| Diagnostic | Nombre |
|---|---|
| valeurs | 14 |
| entites | 2 |
| cardinalite | 1 |

## Détail des échecs

### buteurs_distincts (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buteurs \| attendu ('n_buteurs',) [[110]] \| obtenu ('count',) [[123]]

```sql
SELECT COUNT(DISTINCT e.player_id) FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id WHERE s.outcome = 'Goal'
```

### buts_coup_franc (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('n_buts',) [[6]] \| obtenu ('count',) [[8]]

```sql
SELECT COUNT(*) FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id WHERE s.outcome = 'Goal' AND s.key_pass_id IN (SELECT event_id FROM sb.passes WHERE pass_type = 'Free Kick')
```

### buts_france (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('n_buts',) [[14]] \| obtenu ('count',) [[12]]

```sql
SELECT COUNT(*) FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id JOIN sb.teams t ON e.team_id = t.team_id WHERE s.outcome = 'Goal' AND t.team_name = 'France'
```

### buts_prolongation (rép. 0) : abstention_a_tort, clarification

### buts_temps_additionnel (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('n_buts',) [[19]] \| obtenu ('count',) [[96]]

```sql
SELECT COUNT(*) FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id WHERE s.outcome = 'Goal' AND e.period = 2 AND e.minute >= 45
```

### buts_total (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('n_buts',) [[169]] \| obtenu ('count',) [[183]]

```sql
SELECT COUNT(*) FROM sb.shots WHERE outcome = 'Goal'
```

### cartons_jaunes (rép. 0) : non_signalee

```sql
SELECT COUNT(*) FROM sb.events WHERE (type = 'Bad Behaviour' AND details -> 'bad_behaviour' -> 'card' -> 'name' = '"Yellow Card"') OR (type = 'Foul Committed' AND (details -> 'foul_committed' -> 'card' -> 'name' = '"Yellow Card"' OR details -> 'foul_committed' -> 'card' -> 'name' = '"Second Yellow"'))
```

### classement_xg_top5 (rép. 0) : faux_silencieux, entites

introuvable dans le resultat : joueur \| attendu ('joueur', 'xg') [['Neymar da Silva Santos Junior', 4.178492526], ['Harry Kane', 4.027905531], ['Antoine Griezmann', 3.556915921]] \| obtenu ('player_name', 'total_xg') [['Harry Kane', 4.811405531], ['Neymar da Silva Santos Junior', 4.178492526], ['Antoine Griezmann', 3.556915921]]

```sql
SELECT p.player_name, SUM(s.statsbomb_xg) as total_xg FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id JOIN sb.players p ON e.player_id = p.player_id GROUP BY p.player_id, p.player_name ORDER BY total_xg DESC LIMIT 5
```

### duree_possession (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : duree_moyenne \| attendu ('duree_moyenne',) [[21.08106169296987]] \| obtenu ('round',) [[21.0]]

```sql
SELECT ROUND(AVG(p.duration_seconds), 2) FROM sb.possessions p
```

### equipe_plus_xg (rép. 0) : faux_silencieux, entites

introuvable dans le resultat : equipe \| attendu ('equipe', 'xg') [['Belgium', 12.7244262895]] \| obtenu ('team_name', 'total_xg') [['Croatia', 19.4774227802]]

```sql
WITH xg_by_team AS (SELECT t.team_name, SUM(s.statsbomb_xg) as total_xg FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id JOIN sb.teams t ON e.team_id = t.team_id GROUP BY t.team_id, t.team_name) SELECT team_name, total_xg FROM xg_by_team WHERE total_xg = (SELECT MAX(total_xg) FROM xg_by_team)
```

### fautes_par_match (rép. 0) : erreur_execution, 42883: ERROR:  function round(double precision, integer) does not exist

```sql
SELECT t.team_name, ROUND(CAST(COUNT(*) AS FLOAT) / COUNT(DISTINCT m.match_id), 2) as fouls_per_match FROM sb.events e JOIN sb.matches m ON e.match_id = m.match_id JOIN sb.teams t ON e.team_id = t.team_id WHERE e.type = 'Foul Committed' GROUP BY t.team_id, t.team_name ORDER BY fouls_per_match DESC LIMIT 1
```

### joueurs_expulses (rép. 0) : faux_silencieux, cardinalite

2 lignes obtenues, 4 attendues \| attendu ('joueur',) [['Carlos Alberto Sánchez Moreno'], ['Igor Smolnikov'], ['Jérôme Boateng']] \| obtenu ('player_name',) [['Carlos Alberto Sánchez Moreno'], ['Michael Lang']]

```sql
SELECT DISTINCT p.player_name FROM sb.events e JOIN sb.players p ON e.player_id = p.player_id WHERE (e.type = 'Bad Behaviour' AND e.details -> 'bad_behaviour' -> 'card' ->> 'name' = 'Red Card') OR (e.type = 'Foul Committed' AND e.details -> 'foul_committed' -> 'card' ->> 'name' = 'Red Card')
```

### matchs_nuls (rép. 0) : non_signalee

```sql
SELECT COUNT(*) FROM sb.matches WHERE home_score = away_score
```

### meilleur_buteur (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('joueur', 'n_buts') [['Harry Kane', 6]] \| obtenu ('player_name', 'goals') [['Harry Kane', 7]]

```sql
WITH goal_scorers AS (SELECT p.player_id, p.player_name, COUNT(*) as goals FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id JOIN sb.players p ON e.player_id = p.player_id WHERE s.outcome = 'Goal' GROUP BY p.player_id, p.player_name) SELECT player_name, goals FROM goal_scorers WHERE goals = (SELECT MAX(goals) FROM goal_scorers)
```

### meilleur_passeur (rép. 0) : non_signalee

```sql
WITH assists_by_player AS (SELECT p.player_name, COUNT(*) as assist_count FROM sb.passes pas JOIN sb.events e ON pas.event_id = e.event_id JOIN sb.players p ON e.player_id = p.player_id WHERE pas.goal_assist = true GROUP BY p.player_id, p.player_name) SELECT player_name, assist_count FROM assists_by_player WHERE assist_count = (SELECT MAX(assist_count) FROM assists_by_player)
```

### meilleur_taux_passes (rép. 0) : erreur_execution, 42883: ERROR:  function round(double precision, integer) does not exist

```sql
WITH pass_stats AS (SELECT t.team_id, t.team_name, CAST(SUM(CASE WHEN pa.outcome IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) as success_rate FROM sb.passes pa JOIN sb.events e ON pa.event_id = e.event_id JOIN sb.teams t ON e.team_id = t.team_id GROUP BY t.team_id, t.team_name) SELECT team_name, ROUND(success_rate * 100, 2) as success_percentage FROM pass_stats WHERE success_rate = (SELECT MAX(success_rate) FROM pass_stats)
```

### nb_csc (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_csc \| attendu ('n_csc',) [[12]] \| obtenu ('count',) [[24]]

```sql
SELECT COUNT(*) FROM sb.events WHERE type = 'Own Goal For' OR type = 'Own Goal Against'
```

### nb_seances_tab (rép. 0) : abstention_a_tort, hors_perimetre

### part_buts_premiere_periode (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : part \| attendu ('part',) [[0.38461538461538464]] \| obtenu ('percentage',) [[31.69]]

```sql
SELECT ROUND(100.0 * SUM(CASE WHEN e.period = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) as percentage FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id WHERE s.outcome = 'Goal'
```

### passes_modric (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_passes \| attendu ('n_passes',) [[430]] \| obtenu ('count',) [[0]]

```sql
SELECT COUNT(*) FROM sb.passes p JOIN sb.events e ON p.event_id = e.event_id JOIN sb.players pl ON e.player_id = pl.player_id WHERE pl.player_name = 'Luka Modric' AND p.outcome IS NULL
```

### penalties_jeu (rép. 0) : abstention_a_tort, clarification

### penalties_transformes (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_penalties_marques \| attendu ('n_penalties_marques',) [[22]] \| obtenu ('count',) [[48]]

```sql
SELECT COUNT(*) FROM sb.shots WHERE shot_type = 'Penalty' AND outcome = 'Goal'
```

### possession_dominante (rép. 0) : non_signalee

```sql
WITH possession_by_team AS (SELECT t.team_name, SUM(p.duration_seconds) as total_possession_seconds FROM sb.possessions p JOIN sb.teams t ON p.team_id = t.team_id GROUP BY t.team_id, t.team_name) SELECT team_name, total_possession_seconds FROM possession_by_team WHERE total_possession_seconds = (SELECT MAX(total_possession_seconds) FROM possession_by_team)
```

### tirs_croatie (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_tirs \| attendu ('n_tirs',) [[114]] \| obtenu ('count',) [[124]]

```sql
SELECT COUNT(*) FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id JOIN sb.teams t ON e.team_id = t.team_id WHERE t.team_name = 'Croatia'
```

### tirs_par_match (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : tirs_par_match \| attendu ('tirs_par_match',) [[26.046875]] \| obtenu ('avg',) [[26.65625]]

```sql
SELECT AVG(shot_count) FROM (SELECT m.match_id, COUNT(*) as shot_count FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id JOIN sb.matches m ON e.match_id = m.match_id GROUP BY m.match_id) sub
```

### titulaires_france (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_joueurs \| attendu ('n_joueurs',) [[18]] \| obtenu ('count',) [[23]]

```sql
SELECT COUNT(DISTINCT l.player_id) FROM sb.lineups l JOIN sb.events e ON l.match_id = e.match_id AND l.team_id = e.team_id WHERE l.team_id = (SELECT team_id FROM sb.teams WHERE team_name = 'France') AND e.type = 'Starting XI'
```

### vainqueurs_tab (rép. 0) : abstention_a_tort, clarification

### victoires_russie (rép. 0) : non_signalee

```sql
SELECT COUNT(*) FROM sb.matches WHERE (home_team_id = (SELECT team_id FROM sb.teams WHERE team_name = 'Russia') AND home_score > away_score) OR (away_team_id = (SELECT team_id FROM sb.teams WHERE team_name = 'Russia') AND away_score > home_score)
```

