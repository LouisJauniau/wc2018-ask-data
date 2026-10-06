# Comparaison de runs

| Run | Exactitude | Faux silencieux | Erreurs | Ambiguïtés signalées | Faux signalements | Hors périmètre refusé | Coût |
|---|---|---|---|---|---|---|---|
| `vague1_haiku_brut` (haiku-sous-agent, brut, direct) | 20/52 (38 %) [26-52] | 25/52 (48 %) | 2/52 (4 %) | 2/8 (25 %) | 6/52 (12 %) | 5/6 (83 %) | n/a |
| `vague2_haiku_brut` (haiku-sous-agent, brut, direct) | 23/52 (44 %) [32-58] | 24/52 (46 %) | 1/52 (2 %) | 1/8 (12 %) | 5/52 (10 %) | 6/6 (100 %) | n/a |
| `vague1_haiku_valeurs` (haiku-sous-agent, valeurs, direct) | 29/52 (56 %) [42-68] | 17/52 (33 %) | 2/52 (4 %) | 3/8 (38 %) | 7/52 (13 %) | 6/6 (100 %) | n/a |
| `vague2_haiku_valeurs` (haiku-sous-agent, valeurs, direct) | 30/52 (58 %) [44-70] | 20/52 (38 %) | 1/52 (2 %) | 0/8 (0 %) | 10/52 (19 %) | 5/6 (83 %) | n/a |
| `vague1_haiku_documente` (haiku-sous-agent, documente, direct) | 44/52 (85 %) [72-92] | 7/52 (13 %) | 1/52 (2 %) | 2/8 (25 %) | 1/52 (2 %) | 6/6 (100 %) | n/a |
| `vague2_haiku_documente` (haiku-sous-agent, documente, direct) | 47/52 (90 %) [79-96] | 4/52 (8 %) | 1/52 (2 %) | 1/8 (12 %) | 2/52 (4 %) | 6/6 (100 %) | n/a |

## Question par question

ok juste, FAUX faux silencieux, err erreur d'exécution, abst abstention à tort, sig ambiguïté signalée, - ambiguïté non signalée, HALL réponse inventée hors périmètre. Plusieurs répétitions : une issue par répétition.

| Question | Cat. | vague1_haiku_brut | vague2_haiku_brut | vague1_haiku_valeurs | vague2_haiku_valeurs | vague1_haiku_documente | vague2_haiku_documente |
|---|---|---|---|---|---|---|---|
| affluence_finale | hors_ | ok | ok | ok | ok | ok | ok |
| age_buteurs | hors_ | ok | ok | ok | ok | ok | ok |
| arbitre_plus_matchs | class | ok | ok | ok | ok | ok | ok |
| but_plus_rapide | class | FAUX | ok | ok | FAUX | ok | ok |
| but_xg_min | class | ok | ok | ok | ok | ok | ok |
| buteurs_distincts | compt | FAUX | FAUX | FAUX | FAUX | ok | ok |
| buts_coup_franc | compt | abst | abst | FAUX | FAUX | FAUX | FAUX |
| buts_france | compt | FAUX | FAUX | FAUX | FAUX | FAUX | ok |
| buts_prolongation | compt | FAUX | FAUX | abst | ok | ok | ok |
| buts_temps_additionnel | compt | FAUX | FAUX | FAUX | FAUX | FAUX | FAUX |
| buts_tete | compt | ok | ok | ok | ok | ok | ok |
| buts_total | compt | FAUX | FAUX | FAUX | FAUX | ok | ok |
| cartons_jaunes | ambig | - | sig | - | - | - | - |
| centres_angleterre | compt | ok | ok | ok | ok | ok | ok |
| classement_xg_top5 | class | FAUX | FAUX | FAUX | FAUX | ok | ok |
| club_kane | hors_ | ok | ok | ok | ok | ok | ok |
| corners_equipe | class | ok | FAUX | ok | ok | ok | ok |
| dernier_tiers_proportion | class | ok | ok | ok | ok | ok | ok |
| distance_parcourue | hors_ | HALL | ok | ok | HALL | ok | ok |
| dribbles_reussis | class | abst | FAUX | ok | ok | FAUX | ok |
| duree_possession | ratio | FAUX | FAUX | FAUX | FAUX | ok | ok |
| equipe_plus_xg | class | FAUX | FAUX | FAUX | FAUX | ok | ok |
| fautes_par_match | class | abst | ok | err | ok | ok | ok |
| fautes_uruguay | compt | ok | ok | ok | ok | ok | ok |
| france_2022 | hors_ | ok | ok | ok | ok | ok | ok |
| joueurs_expulses | liste | abst | abst | FAUX | FAUX | ok | ok |
| match_plus_buts | class | FAUX | ok | ok | ok | ok | ok |
| matchs_croatie | compt | ok | ok | ok | ok | ok | ok |
| matchs_nuls | ambig | - | - | - | - | - | - |
| meilleur_buteur | class | FAUX | FAUX | FAUX | FAUX | ok | ok |
| meilleur_joueur | ambig | - | - | sig | - | sig | - |
| meilleur_passeur | ambig | sig | - | - | - | - | - |
| meilleur_taux_passes | class | ok | FAUX | err | ok | ok | ok |
| meilleure_defense | ambig | sig | - | sig | - | - | - |
| nb_csc | compt | FAUX | abst | FAUX | FAUX | ok | ok |
| nb_matchs | compt | ok | ok | ok | ok | ok | ok |
| nb_remplacements | compt | ok | ok | ok | ok | ok | ok |
| nb_seances_tab | compt | abst | abst | abst | ok | ok | ok |
| part_buts_premiere_periode | ratio | FAUX | FAUX | FAUX | FAUX | FAUX | FAUX |
| passes_dec_eden_hazard | compt | ok | ok | ok | ok | ok | ok |
| passes_dec_hazard | ambig | - | - | sig | - | - | - |
| passes_modric | compt | FAUX | FAUX | FAUX | FAUX | FAUX | FAUX |
| passes_profondeur | compt | FAUX | FAUX | ok | ok | ok | ok |
| passes_reussies_joueur | class | err | FAUX | ok | ok | ok | ok |
| pays_plus_buteurs | class | FAUX | ok | ok | ok | ok | ok |
| penalties_jeu | compt | FAUX | FAUX | abst | ok | ok | ok |
| penalties_transformes | compt | FAUX | FAUX | FAUX | FAUX | ok | ok |
| plus_encaisse | class | ok | ok | ok | ok | ok | ok |
| possession_dominante | ambig | - | - | - | - | sig | sig |
| possessions_tir_belgique | compt | FAUX | ok | ok | ok | ok | ok |
| sans_victoire_groupes | compt | ok | ok | ok | ok | ok | ok |
| stade_finale | liste | ok | ok | ok | ok | ok | ok |
| taux_cadres_france | ratio | ok | ok | ok | ok | ok | ok |
| taux_passes_espagne | ratio | err | FAUX | ok | FAUX | ok | ok |
| tirs_cadres_joueur | class | ok | ok | ok | ok | ok | ok |
| tirs_concedes | class | ok | ok | ok | ok | ok | ok |
| tirs_croatie | compt | FAUX | FAUX | FAUX | FAUX | ok | ok |
| tirs_finale | compt | ok | ok | ok | ok | ok | ok |
| tirs_hors_surface | class | ok | err | ok | FAUX | ok | ok |
| tirs_mbappe | compt | FAUX | FAUX | ok | FAUX | FAUX | ok |
| tirs_par_match | ratio | FAUX | FAUX | FAUX | err | ok | ok |
| titulaires_france | compt | FAUX | FAUX | FAUX | FAUX | err | err |
| vainqueur | liste | FAUX | ok | ok | ok | ok | ok |
| vainqueurs_tab | liste | FAUX | FAUX | abst | abst | ok | ok |
| victoires_russie | ambig | - | - | - | - | - | - |
| vitesse_tir | hors_ | ok | ok | ok | ok | ok | ok |
