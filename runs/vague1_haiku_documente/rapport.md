# Run vague1_haiku_documente

| Paramètre | Valeur |
|---|---|
| fournisseur / modèle | rejeu / haiku-sous-agent |
| variante du prompt | documente |
| mode | direct |
| répétitions | 1 |
| jeu / prompt | 7a8956439f6a / 4564226ef08c |
| date | 2026-10-06T15:25:35 |

Réponses rejouées depuis un fichier. Lignes illisibles : 0. Corrections de format : statut 'ok' -> reponse (59).

## Synthèse

| Mesure | Effectif (IC 95 %) |
|---|---|
| **Exactitude**, questions répondables | 44/52 (85 %) [72-92] |
| **Faux silencieux** : s'exécute, renvoie un faux résultat | 7/52 (13 %) [7-25] |
| Part de faux parmi les réponses qui s'exécutent | 7/51 (14 %) [7-26] |
| Erreurs d'exécution (requête finale) | 1/52 (2 %) [0-10] |
| Abstentions à tort | 0/52 (0 %) [0-7] |
| Ambiguïtés signalées | 2/8 (25 %) [7-59] |
| Réponse conforme à une interprétation (ambiguës) | 6/7 (86 %) [49-97] |
| Faux signalements : question claire jugée ambiguë | 1/52 (2 %) [0-10] |
| Hors périmètre : abstention juste | 6/6 (100 %) [61-100] |
| Hors périmètre : réponse inventée | 0/6 (0 %) [0-39] |
| Incidents (pas de réponse, refus, exception) | 0 |

Jetons : 0 en entrée, 0 lus en cache, 0 en sortie, 0 appels. Durée moyenne par question : 0.0 s.

## Par split

| Split | Exactitude | Faux silencieux | Ambiguïtés signalées | Hors périmètre refusé |
|---|---|---|---|---|
| dev | 23/27 (85 %) [68-94] | 4/27 (15 %) | 1/4 (25 %) | 3/3 (100 %) |
| test | 21/25 (84 %) [65-94] | 3/25 (12 %) | 1/4 (25 %) | 3/3 (100 %) |

## Par catégorie

| Catégorie | Justes | Faux silencieux | Erreurs |
|---|---|---|---|
| classement | 17/18 (94 %) | 1 | 0 |
| comptage | 19/25 (76 %) | 5 | 1 |
| liste | 4/4 (100 %) | 0 | 0 |
| ratio | 4/5 (80 %) | 1 | 0 |

## Par piège

Taux d'échec des questions répondables qui portent le piège. Une question porte souvent plusieurs pièges : ces lignes ne s'additionnent pas.

| Piège | Questions | Échecs |
|---|---|---|
| accents | 2 | 2/2 (100 %) |
| nom_complet | 1 | 1/1 (100 %) |
| jsonb_tableau | 1 | 1/1 (100 %) |
| csc | 6 | 3/6 (50 %) |
| jsonb | 2 | 1/2 (50 %) |
| periode_ou_minute | 3 | 1/3 (33 %) |
| buts_par_le_score | 3 | 1/3 (33 %) |
| noms_en_anglais | 9 | 2/9 (22 %) |
| domicile_exterieur | 5 | 1/5 (20 %) |
| ratio | 5 | 1/5 (20 %) |
| passe_reussie_null | 5 | 1/5 (20 %) |
| seance_tab | 17 | 1/17 (6 %) |
| table_derivee | 3 | 0/3 (0 %) |
| libelle_stage | 3 | 0/3 (0 %) |
| faute_commise_ou_subie | 2 | 0/2 (0 %) |
| convention_cadre | 2 | 0/2 (0 %) |
| convention_corner | 1 | 0/1 (0 %) |
| normalisation_par_match | 1 | 0/1 (0 %) |
| cartons_deux_types | 1 | 0/1 (0 %) |
| egalite | 1 | 0/1 (0 %) |
| adversaire | 1 | 0/1 (0 %) |
| geometrie_surface | 1 | 0/1 (0 %) |

## Forme des faux silencieux

| Diagnostic | Nombre |
|---|---|
| valeurs | 6 |
| entites | 1 |

## Détail des échecs

### buts_coup_franc (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('n_buts',) [[6]] \| obtenu ('count',) [[8]]

```sql
SELECT COUNT(*) FROM sb.shots sh WHERE sh.outcome = 'Goal' AND sh.event_id IN (SELECT sp.assisted_shot_id FROM sb.passes sp WHERE sp.pass_type = 'Free Kick' AND sp.outcome IS NULL) AND sh.event_id IN (SELECT event_id FROM sb.events WHERE period != 5)
```

### buts_france (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('n_buts',) [[14]] \| obtenu ('n_goals',) [[12]]

```sql
SELECT COUNT(*) as n_goals FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id WHERE s.outcome = 'Goal' AND e.team_id = (SELECT team_id FROM sb.teams WHERE team_name = 'France') AND e.period < 5
```

### buts_temps_additionnel (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('n_buts',) [[19]] \| obtenu ('n_goals',) [[17]]

```sql
SELECT COUNT(*) as n_goals FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id WHERE s.outcome = 'Goal' AND e.period = 2 AND e.minute >= 90
```

### cartons_jaunes (rép. 0) : non_signalee

```sql
SELECT COUNT(*) as n_yellow_cards FROM sb.events WHERE (type = 'Foul Committed' AND details -> 'foul_committed' -> 'card' ->> 'name' = 'Yellow Card') OR (type = 'Bad Behaviour' AND details -> 'bad_behaviour' -> 'card' ->> 'name' = 'Yellow Card')
```

### dribbles_reussis (rép. 0) : faux_silencieux, entites

introuvable dans le resultat : joueur \| attendu ('joueur', 'n_dribbles') [['Francisco Román Alarcón Suárez', 30]] \| obtenu ('player_name', 'n_dribbles') [['Kylian Mbappé Lottin', 52]]

```sql
WITH stats AS (SELECT pl.player_name, COUNT(*) as n_dribbles FROM sb.events e JOIN sb.players pl ON e.player_id = pl.player_id WHERE e.type = 'Dribble' AND e.period < 5 GROUP BY e.player_id, pl.player_name) SELECT player_name, n_dribbles FROM stats WHERE n_dribbles = (SELECT MAX(n_dribbles) FROM stats)
```

### matchs_nuls (rép. 0) : non_signalee

```sql
SELECT COUNT(*) as n_draws FROM sb.matches WHERE home_score = away_score
```

### meilleur_passeur (rép. 0) : non_signalee

```sql
WITH stats AS (SELECT pl.player_name, COUNT(*) as n_assists FROM sb.passes p JOIN sb.events e ON p.event_id = e.event_id JOIN sb.players pl ON e.player_id = pl.player_id WHERE p.goal_assist AND e.period < 5 GROUP BY pl.player_id, pl.player_name) SELECT player_name, n_assists FROM stats WHERE n_assists = (SELECT MAX(n_assists) FROM stats)
```

### meilleure_defense (rép. 0) : non_signalee

```sql
SELECT t.team_name, SUM(CASE WHEN m.home_team_id = t.team_id THEN m.away_score WHEN m.away_team_id = t.team_id THEN m.home_score END) as goals_against FROM sb.teams t JOIN sb.matches m ON (m.home_team_id = t.team_id OR m.away_team_id = t.team_id) GROUP BY t.team_id, t.team_name ORDER BY goals_against ASC LIMIT 1
```

### part_buts_premiere_periode (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : part \| attendu ('part',) [[0.38461538461538464]] \| obtenu ('?column?',) [[0.36942675159235666]]

```sql
SELECT (SELECT COUNT(*) FROM sb.shots WHERE outcome = 'Goal' AND event_id IN (SELECT event_id FROM sb.events WHERE period = 1))::numeric / (SELECT COUNT(*) FROM sb.shots WHERE outcome = 'Goal' AND event_id IN (SELECT event_id FROM sb.events WHERE period != 5))
```

### passes_dec_hazard (rép. 0) : non_signalee

```sql
SELECT COUNT(*) FROM sb.passes p JOIN sb.events e ON p.event_id = e.event_id WHERE p.goal_assist = true AND e.player_id IN (SELECT player_id FROM sb.players WHERE player_name ILIKE '%Hazard%')
```

### passes_modric (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_passes \| attendu ('n_passes',) [[430]] \| obtenu ('n_passes',) [[0]]

```sql
SELECT COUNT(*) as n_passes FROM sb.passes p JOIN sb.events e ON p.event_id = e.event_id JOIN sb.players pl ON e.player_id = pl.player_id WHERE pl.player_name ILIKE '%Luka Modric%' AND p.outcome IS NULL AND e.period < 5
```

### tirs_mbappe (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_tirs \| attendu ('n_tirs',) [[8]] \| obtenu ('count',) [[0]]

```sql
SELECT COUNT(*) FROM sb.shots sh JOIN sb.events e ON sh.event_id = e.event_id WHERE e.player_id IN (SELECT player_id FROM sb.players WHERE player_name ILIKE '%Mbappe%') AND e.period != 5
```

### titulaires_france (rép. 0) : erreur_execution, 42883: ERROR:  operator does not exist: text ->> unknown

```sql
SELECT COUNT(DISTINCT jsonb_array_elements(details -> 'tactics' -> 'lineup')->>'player'->>'id') FROM sb.events WHERE type = 'Starting XI' AND team_id = (SELECT team_id FROM sb.teams WHERE team_name = 'France')
```

### victoires_russie (rép. 0) : non_signalee

```sql
SELECT COUNT(*) FROM (SELECT match_id FROM sb.matches WHERE home_team_id = (SELECT team_id FROM sb.teams WHERE team_name = 'Russia') AND home_score > away_score UNION ALL SELECT match_id FROM sb.matches WHERE away_team_id = (SELECT team_id FROM sb.teams WHERE team_name = 'Russia') AND away_score > home_score) wins
```

