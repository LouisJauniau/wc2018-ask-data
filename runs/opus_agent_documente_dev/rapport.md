# Run opus_agent_documente_dev

| Paramètre | Valeur |
|---|---|
| fournisseur / modèle | anthropic / claude-opus-5-5 |
| variante du prompt | documente |
| mode | agent |
| répétitions | 1 |
| jeu / prompt | 7a8956439f6a / 14eea6b06925 |
| date | 2026-10-06T16:12:36 |

## Synthèse

| Mesure | Effectif (IC 95 %) |
|---|---|
| **Exactitude**, questions répondables | 27/27 (100 %) [88-100] |
| Exactitude du comparateur seul, avant arbitrage humain | 26/27 (96 %) [82-99] |
| **Faux silencieux** : s'exécute, renvoie un faux résultat | 0/27 (0 %) [0-12] |
| Part de faux parmi les réponses qui s'exécutent | 0/27 (0 %) [0-12] |
| Erreurs d'exécution (requête finale) | 0/27 (0 %) [0-12] |
| Abstentions à tort | 0/27 (0 %) [0-12] |
| Ambiguïtés signalées | 4/4 (100 %) [51-100] |
| Réponse conforme à une interprétation (ambiguës) | 4/4 (100 %) [51-100] |
| Faux signalements : question claire jugée ambiguë | 2/27 (7 %) [2-23] |
| Hors périmètre : abstention juste | 3/3 (100 %) [44-100] |
| Hors périmètre : réponse inventée | 0/3 (0 %) [0-56] |
| Incidents (pas de réponse, refus, exception) | 0 |

Requêtes par question : 1.0. Questions répondables passées par une erreur : 0, dont 0 finies justes.

Jetons : 18129 en entrée, 670067 lus en cache, 22201 en sortie, 67 appels. Coût estimé : 0.651 $. Durée moyenne par question : 8.2 s.

## Par split

| Split | Exactitude | Faux silencieux | Ambiguïtés signalées | Hors périmètre refusé |
|---|---|---|---|---|
| dev | 27/27 (100 %) [88-100] | 0/27 (0 %) | 4/4 (100 %) | 3/3 (100 %) |
| test | n/a | n/a | n/a | n/a |

## Par catégorie

| Catégorie | Justes | Faux silencieux | Erreurs |
|---|---|---|---|
| classement | 9/9 (100 %) | 0 | 0 |
| comptage | 13/13 (100 %) | 0 | 0 |
| liste | 2/2 (100 %) | 0 | 0 |
| ratio | 3/3 (100 %) | 0 | 0 |

## Par piège

Taux d'échec des questions répondables qui portent le piège. Une question porte souvent plusieurs pièges : ces lignes ne s'additionnent pas.

| Piège | Questions | Échecs |
|---|---|---|
| seance_tab | 7 | 0/7 (0 %) |
| noms_en_anglais | 6 | 0/6 (0 %) |
| csc | 3 | 0/3 (0 %) |
| ratio | 3 | 0/3 (0 %) |
| periode_ou_minute | 2 | 0/2 (0 %) |
| table_derivee | 2 | 0/2 (0 %) |
| passe_reussie_null | 2 | 0/2 (0 %) |
| libelle_stage | 2 | 0/2 (0 %) |
| buts_par_le_score | 1 | 0/1 (0 %) |
| domicile_exterieur | 1 | 0/1 (0 %) |
| convention_corner | 1 | 0/1 (0 %) |
| jsonb | 1 | 0/1 (0 %) |
| faute_commise_ou_subie | 1 | 0/1 (0 %) |
| egalite | 1 | 0/1 (0 %) |
| accents | 1 | 0/1 (0 %) |
| convention_cadre | 1 | 0/1 (0 %) |
| geometrie_surface | 1 | 0/1 (0 %) |

## Verdicts corrigés à la main

Voir evals/arbitrages.toml. Le verdict du comparateur est donné entre parenthèses.

### tirs_finale : juste (comparateur : faux_silencieux, cardinalite)

La requete renvoie le detail par equipe (Croatie 15, France 8) et une ligne de total a 23, la bonne reponse. Le comparateur attend une seule ligne et la refuse pour cardinalite.

```sql
SELECT COALESCE(t.team_name, 'Total') AS equipe, count(*) AS tirs
FROM sb.shots s JOIN sb.events e ON e.event_id = s.event_id
JOIN sb.matches m ON m.match_id = e.match_id
JOIN sb.teams t ON t.team_id = e.team_id
WHERE m.stage = 'Final' AND e.period <> 5
GROUP BY ROLLUP(t.team_name) ORDER BY t.team_name NULLS LAST
```

