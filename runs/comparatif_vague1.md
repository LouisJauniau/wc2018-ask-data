# Comparaison de runs

| Run | Exactitude | Faux silencieux | Erreurs | Ambiguïtés signalées | Faux signalements | Hors périmètre refusé | Coût |
|---|---|---|---|---|---|---|---|
| `vague1_haiku_brut` (haiku-sous-agent, brut, direct) | 20/52 (38 %) [26-52] | 25/52 (48 %) | 2/52 (4 %) | 2/8 (25 %) | 6/52 (12 %) | 5/6 (83 %) | n/a |
| `vague1_haiku_valeurs` (haiku-sous-agent, valeurs, direct) | 29/52 (56 %) [42-68] | 17/52 (33 %) | 2/52 (4 %) | 3/8 (38 %) | 7/52 (13 %) | 6/6 (100 %) | n/a |
| `vague1_haiku_documente` (haiku-sous-agent, documente, direct) | 44/52 (85 %) [72-92] | 7/52 (13 %) | 1/52 (2 %) | 2/8 (25 %) | 1/52 (2 %) | 6/6 (100 %) | n/a |
| `vague1_sonnet_brut` (sonnet-sous-agent, brut, direct) | 52/52 (100 %) [93-100] | 0/52 (0 %) | 0/52 (0 %) | 7/8 (88 %) | 2/52 (4 %) | 6/6 (100 %) | n/a |
| `vague1_sonnet_valeurs` (sonnet-sous-agent, valeurs, direct) | 52/52 (100 %) [93-100] | 0/52 (0 %) | 0/52 (0 %) | 7/8 (88 %) | 3/52 (6 %) | 6/6 (100 %) | n/a |
| `vague1_sonnet_documente` (sonnet-sous-agent, documente, direct) | 52/52 (100 %) [93-100] | 0/52 (0 %) | 0/52 (0 %) | 7/8 (88 %) | 2/52 (4 %) | 6/6 (100 %) | n/a |

## Question par question

ok juste, FAUX faux silencieux, err erreur d'exécution, abst abstention à tort, sig ambiguïté signalée, - ambiguïté non signalée, HALL réponse inventée hors périmètre. Plusieurs répétitions : une issue par répétition.

| Question | Cat. | vague1_haiku_brut | vague1_haiku_valeurs | vague1_haiku_documente | vague1_sonnet_brut | vague1_sonnet_valeurs | vague1_sonnet_documente |
|---|---|---|---|---|---|---|---|
| affluence_finale | hors_ | ok | ok | ok | ok | ok | ok |
| age_buteurs | hors_ | ok | ok | ok | ok | ok | ok |
| arbitre_plus_matchs | class | ok | ok | ok | ok | ok | ok |
| but_plus_rapide | class | FAUX | ok | ok | ok | ok | ok |
| but_xg_min | class | ok | ok | ok | ok | ok | ok |
| buteurs_distincts | compt | FAUX | FAUX | ok | ok | ok | ok |
| buts_coup_franc | compt | abst | FAUX | FAUX | ok | ok | ok |
| buts_france | compt | FAUX | FAUX | FAUX | ok | ok | ok |
| buts_prolongation | compt | FAUX | abst | ok | ok | ok | ok |
| buts_temps_additionnel | compt | FAUX | FAUX | FAUX | ok | ok | ok |
| buts_tete | compt | ok | ok | ok | ok | ok | ok |
| buts_total | compt | FAUX | FAUX | ok | ok | ok | ok |
| cartons_jaunes | ambig | - | - | - | sig | sig | sig |
| centres_angleterre | compt | ok | ok | ok | ok | ok | ok |
| classement_xg_top5 | class | FAUX | FAUX | ok | ok | ok | ok |
| club_kane | hors_ | ok | ok | ok | ok | ok | ok |
| corners_equipe | class | ok | ok | ok | ok | ok | ok |
| dernier_tiers_proportion | class | ok | ok | ok | ok | ok | ok |
| distance_parcourue | hors_ | HALL | ok | ok | ok | ok | ok |
| dribbles_reussis | class | abst | ok | FAUX | ok | ok | ok |
| duree_possession | ratio | FAUX | FAUX | ok | ok | ok | ok |
| equipe_plus_xg | class | FAUX | FAUX | ok | ok | ok | ok |
| fautes_par_match | class | abst | err | ok | ok | ok | ok |
| fautes_uruguay | compt | ok | ok | ok | ok | ok | ok |
| france_2022 | hors_ | ok | ok | ok | ok | ok | ok |
| joueurs_expulses | liste | abst | FAUX | ok | ok | ok | ok |
| match_plus_buts | class | FAUX | ok | ok | ok | ok | ok |
| matchs_croatie | compt | ok | ok | ok | ok | ok | ok |
| matchs_nuls | ambig | - | - | - | - | sig | sig |
| meilleur_buteur | class | FAUX | FAUX | ok | ok | ok | ok |
| meilleur_joueur | ambig | - | sig | sig | sig | - | - |
| meilleur_passeur | ambig | sig | - | - | sig | sig | sig |
| meilleur_taux_passes | class | ok | err | ok | ok | ok | ok |
| meilleure_defense | ambig | sig | sig | - | sig | sig | sig |
| nb_csc | compt | FAUX | FAUX | ok | ok | ok | ok |
| nb_matchs | compt | ok | ok | ok | ok | ok | ok |
| nb_remplacements | compt | ok | ok | ok | ok | ok | ok |
| nb_seances_tab | compt | abst | abst | ok | ok | ok | ok |
| part_buts_premiere_periode | ratio | FAUX | FAUX | FAUX | ok | ok | ok |
| passes_dec_eden_hazard | compt | ok | ok | ok | ok | ok | ok |
| passes_dec_hazard | ambig | - | sig | - | sig | sig | sig |
| passes_modric | compt | FAUX | FAUX | FAUX | ok | ok | ok |
| passes_profondeur | compt | FAUX | ok | ok | ok | ok | ok |
| passes_reussies_joueur | class | err | ok | ok | ok | ok | ok |
| pays_plus_buteurs | class | FAUX | ok | ok | ok | ok | ok |
| penalties_jeu | compt | FAUX | abst | ok | ok | ok | ok |
| penalties_transformes | compt | FAUX | FAUX | ok | ok | ok | ok |
| plus_encaisse | class | ok | ok | ok | ok | ok | ok |
| possession_dominante | ambig | - | - | sig | sig | sig | sig |
| possessions_tir_belgique | compt | FAUX | ok | ok | ok | ok | ok |
| sans_victoire_groupes | compt | ok | ok | ok | ok | ok | ok |
| stade_finale | liste | ok | ok | ok | ok | ok | ok |
| taux_cadres_france | ratio | ok | ok | ok | ok | ok | ok |
| taux_passes_espagne | ratio | err | ok | ok | ok | ok | ok |
| tirs_cadres_joueur | class | ok | ok | ok | ok | ok | ok |
| tirs_concedes | class | ok | ok | ok | ok | ok | ok |
| tirs_croatie | compt | FAUX | FAUX | ok | ok | ok | ok |
| tirs_finale | compt | ok | ok | ok | ok | ok | ok |
| tirs_hors_surface | class | ok | ok | ok | ok | ok | ok |
| tirs_mbappe | compt | FAUX | ok | FAUX | ok | ok | ok |
| tirs_par_match | ratio | FAUX | FAUX | ok | ok | ok | ok |
| titulaires_france | compt | FAUX | FAUX | err | ok | ok | ok |
| vainqueur | liste | FAUX | ok | ok | ok | ok | ok |
| vainqueurs_tab | liste | FAUX | abst | ok | ok | ok | ok |
| victoires_russie | ambig | - | - | - | sig | sig | sig |
| vitesse_tir | hors_ | ok | ok | ok | ok | ok | ok |
