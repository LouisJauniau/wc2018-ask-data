# Run vague2_haiku_documente

| Paramètre | Valeur |
|---|---|
| fournisseur / modèle | rejeu / haiku-sous-agent |
| variante du prompt | documente |
| mode | direct |
| répétitions | 1 |
| jeu / prompt | 7a8956439f6a / 4564226ef08c |
| date | 2026-10-06T15:32:15 |

Réponses rejouées depuis un fichier. Lignes illisibles : 0. Corrections de format : aucune.

## Synthèse

| Mesure | Effectif (IC 95 %) |
|---|---|
| **Exactitude**, questions répondables | 47/52 (90 %) [79-96] |
| **Faux silencieux** : s'exécute, renvoie un faux résultat | 4/52 (8 %) [3-18] |
| Part de faux parmi les réponses qui s'exécutent | 4/51 (8 %) [3-19] |
| Erreurs d'exécution (requête finale) | 1/52 (2 %) [0-10] |
| Abstentions à tort | 0/52 (0 %) [0-7] |
| Ambiguïtés signalées | 1/8 (12 %) [2-47] |
| Réponse conforme à une interprétation (ambiguës) | 7/7 (100 %) [65-100] |
| Faux signalements : question claire jugée ambiguë | 2/52 (4 %) [1-13] |
| Hors périmètre : abstention juste | 6/6 (100 %) [61-100] |
| Hors périmètre : réponse inventée | 0/6 (0 %) [0-39] |
| Incidents (pas de réponse, refus, exception) | 0 |

Jetons : 0 en entrée, 0 lus en cache, 0 en sortie, 0 appels. Durée moyenne par question : 0.0 s.

## Par split

| Split | Exactitude | Faux silencieux | Ambiguïtés signalées | Hors périmètre refusé |
|---|---|---|---|---|
| dev | 25/27 (93 %) [77-98] | 2/27 (7 %) | 1/4 (25 %) | 3/3 (100 %) |
| test | 22/25 (88 %) [70-96] | 2/25 (8 %) | 0/4 (0 %) | 3/3 (100 %) |

## Par catégorie

| Catégorie | Justes | Faux silencieux | Erreurs |
|---|---|---|---|
| classement | 18/18 (100 %) | 0 | 0 |
| comptage | 21/25 (84 %) | 3 | 1 |
| liste | 4/4 (100 %) | 0 | 0 |
| ratio | 4/5 (80 %) | 1 | 0 |

## Par piège

Taux d'échec des questions répondables qui portent le piège. Une question porte souvent plusieurs pièges : ces lignes ne s'additionnent pas.

| Piège | Questions | Échecs |
|---|---|---|
| jsonb_tableau | 1 | 1/1 (100 %) |
| accents | 2 | 1/2 (50 %) |
| csc | 6 | 2/6 (33 %) |
| periode_ou_minute | 3 | 1/3 (33 %) |
| ratio | 5 | 1/5 (20 %) |
| passe_reussie_null | 5 | 1/5 (20 %) |
| noms_en_anglais | 9 | 1/9 (11 %) |
| seance_tab | 17 | 1/17 (6 %) |
| domicile_exterieur | 5 | 0/5 (0 %) |
| buts_par_le_score | 3 | 0/3 (0 %) |
| table_derivee | 3 | 0/3 (0 %) |
| libelle_stage | 3 | 0/3 (0 %) |
| jsonb | 2 | 0/2 (0 %) |
| faute_commise_ou_subie | 2 | 0/2 (0 %) |
| convention_cadre | 2 | 0/2 (0 %) |
| convention_corner | 1 | 0/1 (0 %) |
| normalisation_par_match | 1 | 0/1 (0 %) |
| cartons_deux_types | 1 | 0/1 (0 %) |
| egalite | 1 | 0/1 (0 %) |
| adversaire | 1 | 0/1 (0 %) |
| geometrie_surface | 1 | 0/1 (0 %) |
| nom_complet | 1 | 0/1 (0 %) |

## Forme des faux silencieux

| Diagnostic | Nombre |
|---|---|
| valeurs | 4 |

## Détail des échecs

### buts_coup_franc (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('n_buts',) [[6]] \| obtenu ('goals_from_free_kick',) [[23]]

```sql
SELECT COUNT(*) as goals_from_free_kick FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id WHERE s.outcome = 'Goal' AND e.play_pattern = 'From Free Kick' AND e.period < 5
```

### buts_temps_additionnel (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('n_buts',) [[19]] \| obtenu ('goals_in_extra_time',) [[17]]

```sql
SELECT COUNT(*) as goals_in_extra_time FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id WHERE s.outcome = 'Goal' AND e.period = 2 AND e.minute >= 90;
```

### cartons_jaunes (rép. 0) : non_signalee

```sql
SELECT COUNT(*) as cartons_jaunes FROM sb.events WHERE ((type = 'Foul Committed' AND details -> 'foul_committed' -> 'card' ->> 'name' = 'Yellow Card') OR (type = 'Bad Behaviour' AND details -> 'bad_behaviour' -> 'card' ->> 'name' = 'Yellow Card')) AND period != 5;
```

### matchs_nuls (rép. 0) : non_signalee

```sql
SELECT COUNT(*) as matchs_nuls FROM sb.matches WHERE home_score = away_score;
```

### meilleur_joueur (rép. 0) : non_signalee

### meilleur_passeur (rép. 0) : non_signalee

```sql
WITH assists_par_joueur AS (SELECT e.player_id, pl.player_name, COUNT(*) as n_assists FROM sb.passes p JOIN sb.events e ON p.event_id = e.event_id JOIN sb.players pl ON e.player_id = pl.player_id WHERE p.goal_assist = true AND e.period != 5 GROUP BY e.player_id, pl.player_name) SELECT player_name, n_assists FROM assists_par_joueur WHERE n_assists = (SELECT MAX(n_assists) FROM assists_par_joueur);
```

### meilleure_defense (rép. 0) : non_signalee

```sql
WITH team_goals_conceded AS (SELECT m.home_team_id as team_id, SUM(m.away_score) as goals_conceded FROM sb.matches m GROUP BY m.home_team_id UNION ALL SELECT m.away_team_id as team_id, SUM(m.home_score) as goals_conceded FROM sb.matches m GROUP BY m.away_team_id), total_goals_conceded AS (SELECT team_id, SUM(goals_conceded) as total_conceded FROM team_goals_conceded GROUP BY team_id) SELECT t.team_name, tgc.total_conceded FROM total_goals_conceded tgc JOIN sb.teams t ON tgc.team_id = t.team_id WHERE tgc.total_conceded = (SELECT MIN(total_conceded) FROM total_goals_conceded)
```

### part_buts_premiere_periode (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : part \| attendu ('part',) [[0.38461538461538464]] \| obtenu ('first_half_ratio',) [[0.36942675159235666]]

```sql
WITH goals_by_period AS (SELECT e.period, COUNT(*) as goals FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id WHERE s.outcome = 'Goal' AND e.period < 5 GROUP BY e.period), total_goals AS (SELECT SUM(goals) as total FROM goals_by_period) SELECT (SELECT goals FROM goals_by_period WHERE period = 1)::numeric / (SELECT total FROM total_goals) as first_half_ratio
```

### passes_dec_hazard (rép. 0) : non_signalee

```sql
SELECT p.player_name, COUNT(*) as goal_assists FROM sb.passes pa JOIN sb.events e ON pa.event_id = e.event_id JOIN sb.players p ON e.player_id = p.player_id WHERE p.player_name ILIKE '%Hazard%' AND pa.goal_assist = true AND e.period < 5 GROUP BY p.player_id, p.player_name ORDER BY goal_assists DESC
```

### passes_modric (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_passes \| attendu ('n_passes',) [[430]] \| obtenu ('passes_reussies',) [[0]]

```sql
SELECT COUNT(*) as passes_reussies FROM sb.passes p JOIN sb.events e ON p.event_id = e.event_id JOIN sb.players pl ON e.player_id = pl.player_id WHERE pl.player_name ILIKE '%Modric%' AND p.outcome IS NULL AND e.period != 5;
```

### titulaires_france (rép. 0) : erreur_execution, 0A000: ERROR:  aggregate function calls cannot contain set-returning function calls

```sql
SELECT COUNT(DISTINCT ((jsonb_array_elements(e.details -> 'tactics' -> 'lineup')->'player'->>'id')::integer)) as unique_starters FROM sb.events e WHERE e.type = 'Starting XI' AND e.team_id = (SELECT team_id FROM sb.teams WHERE team_name = 'France')
```

### victoires_russie (rép. 0) : non_signalee

```sql
SELECT COUNT(*) as matches_won FROM sb.matches m WHERE (m.home_team_id = (SELECT team_id FROM sb.teams WHERE team_name = 'Russia') AND m.home_score > m.away_score) OR (m.away_team_id = (SELECT team_id FROM sb.teams WHERE team_name = 'Russia') AND m.away_score > m.home_score)
```

