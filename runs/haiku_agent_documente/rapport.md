# Run haiku_agent_documente

| Paramètre | Valeur |
|---|---|
| fournisseur / modèle | anthropic / claude-haiku-4-5 |
| variante du prompt | documente |
| mode | agent |
| répétitions | 1 |
| jeu / prompt | 7a8956439f6a / 14eea6b06925 |
| date | 2026-10-06T16:17:24 |

## Synthèse

| Mesure | Effectif (IC 95 %) |
|---|---|
| **Exactitude**, questions répondables | 48/52 (92 %) [82-97] |
| **Faux silencieux** : s'exécute, renvoie un faux résultat | 4/52 (8 %) [3-18] |
| Part de faux parmi les réponses qui s'exécutent | 4/52 (8 %) [3-18] |
| Erreurs d'exécution (requête finale) | 0/52 (0 %) [0-7] |
| Abstentions à tort | 0/52 (0 %) [0-7] |
| Ambiguïtés signalées | 2/8 (25 %) [7-59] |
| Réponse conforme à une interprétation (ambiguës) | 6/6 (100 %) [61-100] |
| Faux signalements : question claire jugée ambiguë | 0/52 (0 %) [0-7] |
| Hors périmètre : abstention juste | 5/6 (83 %) [44-97] |
| Hors périmètre : réponse inventée | 1/6 (17 %) [3-56] |
| Incidents (pas de réponse, refus, exception) | 0 |

Requêtes par question : 1.6. Questions répondables passées par une erreur : 5, dont 2 finies justes.

Jetons : 117756 en entrée, 1287812 lus en cache, 42727 en sortie, 177 appels. Coût estimé : 0.497 $. Durée moyenne par question : 7.6 s.

## Par split

| Split | Exactitude | Faux silencieux | Ambiguïtés signalées | Hors périmètre refusé |
|---|---|---|---|---|
| dev | 25/27 (93 %) [77-98] | 2/27 (7 %) | 0/4 (0 %) | 3/3 (100 %) |
| test | 23/25 (92 %) [75-98] | 2/25 (8 %) | 2/4 (50 %) | 2/3 (67 %) |

## Par catégorie

| Catégorie | Justes | Faux silencieux | Erreurs |
|---|---|---|---|
| classement | 18/18 (100 %) | 0 | 0 |
| comptage | 22/25 (88 %) | 3 | 0 |
| liste | 4/4 (100 %) | 0 | 0 |
| ratio | 4/5 (80 %) | 1 | 0 |

## Par piège

Taux d'échec des questions répondables qui portent le piège. Une question porte souvent plusieurs pièges : ces lignes ne s'additionnent pas.

| Piège | Questions | Échecs |
|---|---|---|
| jsonb_tableau | 1 | 1/1 (100 %) |
| csc | 6 | 2/6 (33 %) |
| periode_ou_minute | 3 | 1/3 (33 %) |
| libelle_stage | 3 | 1/3 (33 %) |
| ratio | 5 | 1/5 (20 %) |
| noms_en_anglais | 9 | 1/9 (11 %) |
| seance_tab | 17 | 1/17 (6 %) |
| domicile_exterieur | 5 | 0/5 (0 %) |
| passe_reussie_null | 5 | 0/5 (0 %) |
| buts_par_le_score | 3 | 0/3 (0 %) |
| table_derivee | 3 | 0/3 (0 %) |
| jsonb | 2 | 0/2 (0 %) |
| faute_commise_ou_subie | 2 | 0/2 (0 %) |
| accents | 2 | 0/2 (0 %) |
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
| valeurs | 3 |
| cardinalite | 1 |

## Détail des échecs

### buts_temps_additionnel (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('n_buts',) [[19]] \| obtenu ('nombre_buts',) [[17]]

```sql
SELECT 
  COUNT(*) as nombre_buts
FROM sb.shots s
JOIN sb.events e ON s.event_id = e.event_id
WHERE s.outcome = 'Goal'
  AND e.period = 2
  AND e.minute >= 90
```

### cartons_jaunes (rép. 0) : non_signalee

```sql
SELECT 
  (SELECT COUNT(*) FROM sb.events 
   WHERE type = 'Foul Committed' 
   AND details -> 'foul_committed' -> 'card' ->> 'name' = 'Yellow Card') +
  (SELECT COUNT(*) FROM sb.events 
   WHERE type = 'Bad Behaviour' 
   AND details -> 'bad_behaviour' -> 'card' ->> 'name' = 'Yellow Card') 
as total_cartons_jaunes
```

### distance_parcourue (rép. 0) : hallucination

```sql
SELECT 
  p.player_name,
  ROUND(SUM(SQRT(POWER(c.end_x - e.loc_x, 2) + POWER(c.end_y - e.loc_y, 2)))::numeric, 2) as total_distance
FROM sb.carries c
JOIN sb.events e ON c.event_id = e.event_id
JOIN sb.players p ON e.player_id = p.player_id
WHERE e.period < 5
  AND e.player_id IS NOT NULL
GROUP BY p.player_id, p.player_name
ORDER BY total_distance DESC
LIMIT 1;
```

### matchs_nuls (rép. 0) : non_signalee

```sql
SELECT COUNT(*) as nombre_matchs_nuls
FROM sb.matches
WHERE home_score = away_score
```

### meilleur_passeur (rép. 0) : non_signalee

```sql
SELECT 
  p.player_name,
  COUNT(*) as nb_passes_decisives
FROM sb.passes pa
JOIN sb.events e ON pa.event_id = e.event_id
JOIN sb.players p ON e.player_id = p.player_id
WHERE pa.goal_assist = true
  AND e.period < 5
GROUP BY p.player_id, p.player_name
HAVING COUNT(*) = (
  SELECT COUNT(*)
  FROM sb.passes pa2
  JOIN sb.events e2 ON pa2.event_id = e2.event_id
  WHERE pa2.goal_assist = true AND e2.period < 5
  GROUP BY e2.player_id
  ORDER BY COUNT(*) DESC
  LIMIT 1
)
ORDER BY p.player_name;
```

### part_buts_premiere_periode (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : part \| attendu ('part',) [[0.38461538461538464]] \| obtenu ('buts_p1', 'buts_total', 'pourcentage_p1') [[58, 157, 36.9]]

```sql
SELECT 
  COUNT(*) FILTER (WHERE e.period = 1) as buts_p1,
  COUNT(*) as buts_total,
  ROUND(100.0 * COUNT(*) FILTER (WHERE e.period = 1) / COUNT(*), 1) as pourcentage_p1
FROM sb.shots s
JOIN sb.events e ON s.event_id = e.event_id
WHERE s.outcome = 'Goal' AND e.period != 5
```

### passes_dec_hazard (rép. 0) : non_signalee

```sql
SELECT 
  p.player_name,
  COUNT(*) as passes_decisives
FROM sb.passes
INNER JOIN sb.events e ON e.event_id = sb.passes.event_id
INNER JOIN sb.players p ON p.player_id = e.player_id
WHERE e.player_id = 3621
  AND sb.passes.goal_assist = true
  AND e.period IN (1, 2, 3, 4)
GROUP BY p.player_name
```

### possession_dominante (rép. 0) : non_signalee

```sql
SELECT 
  t.team_name,
  SUM(p.duration_seconds) AS total_possession_seconds
FROM sb.possessions p
JOIN sb.teams t ON p.team_id = t.team_id
WHERE p.period < 5
GROUP BY t.team_name
ORDER BY total_possession_seconds DESC
```

### tirs_finale (rép. 0) : faux_silencieux, cardinalite

2 lignes obtenues, 1 attendues \| attendu ('n_tirs',) [[23]] \| obtenu ('team_name', 'shots_count') [['Croatia', 15], ['France', 8]]

```sql
SELECT 
  t.team_name,
  COUNT(s.event_id) AS shots_count
FROM sb.shots s
JOIN sb.events e ON s.event_id = e.event_id
JOIN sb.matches m ON e.match_id = m.match_id
JOIN sb.teams t ON e.team_id = t.team_id
WHERE m.stage = 'Final'
  AND e.period != 5
GROUP BY t.team_id, t.team_name
ORDER BY t.team_name;
```

### titulaires_france (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_joueurs \| attendu ('n_joueurs',) [[18]] \| obtenu ('nombre_de_joueurs',) [[19]]

```sql
WITH france_lineups AS (
  SELECT DISTINCT 
    jsonb_array_elements(e.details -> 'tactics' -> 'lineup') -> 'player' ->> 'name' AS player_name
  FROM sb.events e
  JOIN sb.matches m ON e.match_id = m.match_id
  WHERE e.type = 'Starting XI'
    AND (m.home_team_id = (SELECT team_id FROM sb.teams WHERE team_name = 'France')
         OR m.away_team_id = (SELECT team_id FROM sb.teams WHERE team_name = 'France'))
    AND e.team_id = (SELECT team_id FROM sb.teams WHERE team_name = 'France')
)
SELECT COUNT(*) AS nombre_de_joueurs
FROM france_lineups
```

### victoires_russie (rép. 0) : non_signalee

```sql
SELECT COUNT(*) as matchs_gagnes
FROM sb.matches m
WHERE (
  (m.home_team_id = (SELECT team_id FROM sb.teams WHERE team_name = 'Russia') AND m.home_score > m.away_score)
  OR
  (m.away_team_id = (SELECT team_id FROM sb.teams WHERE team_name = 'Russia') AND m.away_score > m.home_score)
)
```

