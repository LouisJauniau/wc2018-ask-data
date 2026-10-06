# Run vague1_sonnet_valeurs

| Paramètre | Valeur |
|---|---|
| fournisseur / modèle | rejeu / sonnet-sous-agent |
| variante du prompt | valeurs |
| mode | direct |
| répétitions | 1 |
| jeu / prompt | 7a8956439f6a / 3ec955e03233 |
| date | 2026-10-06T15:25:40 |

Réponses rejouées depuis un fichier. Lignes illisibles : 0. Corrections de format : statut 'ok' -> reponse (59).

## Synthèse

| Mesure | Effectif (IC 95 %) |
|---|---|
| **Exactitude**, questions répondables | 52/52 (100 %) [93-100] |
| **Faux silencieux** : s'exécute, renvoie un faux résultat | 0/52 (0 %) [0-7] |
| Part de faux parmi les réponses qui s'exécutent | 0/52 (0 %) [0-7] |
| Erreurs d'exécution (requête finale) | 0/52 (0 %) [0-7] |
| Abstentions à tort | 0/52 (0 %) [0-7] |
| Ambiguïtés signalées | 7/8 (88 %) [53-98] |
| Réponse conforme à une interprétation (ambiguës) | 7/7 (100 %) [65-100] |
| Faux signalements : question claire jugée ambiguë | 3/52 (6 %) [2-16] |
| Hors périmètre : abstention juste | 6/6 (100 %) [61-100] |
| Hors périmètre : réponse inventée | 0/6 (0 %) [0-39] |
| Incidents (pas de réponse, refus, exception) | 0 |

Jetons : 0 en entrée, 0 lus en cache, 0 en sortie, 0 appels. Durée moyenne par question : 0.0 s.

## Par split

| Split | Exactitude | Faux silencieux | Ambiguïtés signalées | Hors périmètre refusé |
|---|---|---|---|---|
| dev | 27/27 (100 %) [88-100] | 0/27 (0 %) | 4/4 (100 %) | 3/3 (100 %) |
| test | 25/25 (100 %) [87-100] | 0/25 (0 %) | 3/4 (75 %) | 3/3 (100 %) |

## Par catégorie

| Catégorie | Justes | Faux silencieux | Erreurs |
|---|---|---|---|
| classement | 18/18 (100 %) | 0 | 0 |
| comptage | 25/25 (100 %) | 0 | 0 |
| liste | 4/4 (100 %) | 0 | 0 |
| ratio | 5/5 (100 %) | 0 | 0 |

## Par piège

Taux d'échec des questions répondables qui portent le piège. Une question porte souvent plusieurs pièges : ces lignes ne s'additionnent pas.

| Piège | Questions | Échecs |
|---|---|---|
| seance_tab | 17 | 0/17 (0 %) |
| noms_en_anglais | 9 | 0/9 (0 %) |
| csc | 6 | 0/6 (0 %) |
| domicile_exterieur | 5 | 0/5 (0 %) |
| ratio | 5 | 0/5 (0 %) |
| passe_reussie_null | 5 | 0/5 (0 %) |
| periode_ou_minute | 3 | 0/3 (0 %) |
| buts_par_le_score | 3 | 0/3 (0 %) |
| table_derivee | 3 | 0/3 (0 %) |
| libelle_stage | 3 | 0/3 (0 %) |
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
| jsonb_tableau | 1 | 0/1 (0 %) |

## Détail des échecs

### meilleur_joueur (rép. 0) : non_signalee

