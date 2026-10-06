# Run opus_agent_documente_test

| Paramètre | Valeur |
|---|---|
| fournisseur / modèle | anthropic / claude-opus-5-5 |
| variante du prompt | documente |
| mode | agent |
| répétitions | 1 |
| jeu / prompt | 7a8956439f6a / 14eea6b06925 |
| date | 2026-10-06T16:15:30 |

## Synthèse

| Mesure | Effectif (IC 95 %) |
|---|---|
| **Exactitude**, questions répondables | 25/25 (100 %) [87-100] |
| Exactitude du comparateur seul, avant arbitrage humain | 24/25 (96 %) [80-99] |
| **Faux silencieux** : s'exécute, renvoie un faux résultat | 0/25 (0 %) [0-13] |
| Part de faux parmi les réponses qui s'exécutent | 0/25 (0 %) [0-13] |
| Erreurs d'exécution (requête finale) | 0/25 (0 %) [0-13] |
| Abstentions à tort | 0/25 (0 %) [0-13] |
| Ambiguïtés signalées | 4/4 (100 %) [51-100] |
| Réponse conforme à une interprétation (ambiguës) | 3/3 (100 %) [44-100] |
| Faux signalements : question claire jugée ambiguë | 1/25 (4 %) [1-20] |
| Hors périmètre : abstention juste | 3/3 (100 %) [44-100] |
| Hors périmètre : réponse inventée | 0/3 (0 %) [0-56] |
| Incidents (pas de réponse, refus, exception) | 0 |

Requêtes par question : 1.0. Questions répondables passées par une erreur : 0, dont 0 finies justes.

Jetons : 21366 en entrée, 640064 lus en cache, 23607 en sortie, 64 appels. Coût estimé : 0.686 $. Durée moyenne par question : 8.5 s.

## Par split

| Split | Exactitude | Faux silencieux | Ambiguïtés signalées | Hors périmètre refusé |
|---|---|---|---|---|
| dev | n/a | n/a | n/a | n/a |
| test | 25/25 (100 %) [87-100] | 0/25 (0 %) | 4/4 (100 %) | 3/3 (100 %) |

## Par catégorie

| Catégorie | Justes | Faux silencieux | Erreurs |
|---|---|---|---|
| classement | 9/9 (100 %) | 0 | 0 |
| comptage | 12/12 (100 %) | 0 | 0 |
| liste | 2/2 (100 %) | 0 | 0 |
| ratio | 2/2 (100 %) | 0 | 0 |

## Par piège

Taux d'échec des questions répondables qui portent le piège. Une question porte souvent plusieurs pièges : ces lignes ne s'additionnent pas.

| Piège | Questions | Échecs |
|---|---|---|
| seance_tab | 10 | 0/10 (0 %) |
| domicile_exterieur | 4 | 0/4 (0 %) |
| csc | 3 | 0/3 (0 %) |
| noms_en_anglais | 3 | 0/3 (0 %) |
| passe_reussie_null | 3 | 0/3 (0 %) |
| buts_par_le_score | 2 | 0/2 (0 %) |
| ratio | 2 | 0/2 (0 %) |
| periode_ou_minute | 1 | 0/1 (0 %) |
| normalisation_par_match | 1 | 0/1 (0 %) |
| faute_commise_ou_subie | 1 | 0/1 (0 %) |
| jsonb | 1 | 0/1 (0 %) |
| cartons_deux_types | 1 | 0/1 (0 %) |
| table_derivee | 1 | 0/1 (0 %) |
| convention_cadre | 1 | 0/1 (0 %) |
| adversaire | 1 | 0/1 (0 %) |
| accents | 1 | 0/1 (0 %) |
| nom_complet | 1 | 0/1 (0 %) |
| jsonb_tableau | 1 | 0/1 (0 %) |
| libelle_stage | 1 | 0/1 (0 %) |

## Verdicts corrigés à la main

Voir evals/arbitrages.toml. Le verdict du comparateur est donné entre parenthèses.

### sans_victoire_groupes : juste (comparateur : faux_silencieux, cardinalite)

La question demande un nombre, la requete renvoie la liste des equipes concernees. Verifie : ce sont exactement les six equipes sans victoire (Australie, Costa Rica, Egypte, Islande, Maroc, Panama), et la reponse donnee a l'utilisateur dit « six equipes ». Le comparateur refuse pour cardinalite (six lignes au lieu d'une).

```sql
WITH r AS (
  SELECT home_team_id team_id, (home_score>away_score)::int w FROM sb.matches WHERE stage='Group Stage'
  UNION ALL
  SELECT away_team_id, (away_score>home_score)::int FROM sb.matches WHERE stage='Group Stage'
)
SELECT t.team_name, count(*) matchs, sum(w) victoires
FROM r JOIN sb.teams t USING(team_id)
GROUP BY t.team_name HAVING sum(w)=0 ORDER BY t.team_name
```

