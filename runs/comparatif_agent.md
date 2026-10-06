# Comparaison de runs

| Run | Exactitude | Faux silencieux | Erreurs | Ambiguïtés signalées | Faux signalements | Hors périmètre refusé | Coût |
|---|---|---|---|---|---|---|---|
| `vague1_haiku_documente` (haiku-sous-agent, documente, direct) | 44/52 (85 %) [72-92] | 7/52 (13 %) | 1/52 (2 %) | 2/8 (25 %) | 1/52 (2 %) | 6/6 (100 %) | n/a |
| `vague2_haiku_documente` (haiku-sous-agent, documente, direct) | 47/52 (90 %) [79-96] | 4/52 (8 %) | 1/52 (2 %) | 1/8 (12 %) | 2/52 (4 %) | 6/6 (100 %) | n/a |
| `haiku_agent_documente` (claude-haiku-4-5, documente, agent) | 48/52 (92 %) [82-97] | 4/52 (8 %) | 0/52 (0 %) | 2/8 (25 %) | 0/52 (0 %) | 5/6 (83 %) | 0.50 $ |
| `opus_agent_documente_dev` (claude-opus-5-5, documente, agent) | 27/27 (100 %) [88-100] | 0/27 (0 %) | 0/27 (0 %) | 4/4 (100 %) | 2/27 (7 %) | 3/3 (100 %) | 0.65 $ |
| `opus_agent_documente_test` (claude-opus-5-5, documente, agent) | 25/25 (100 %) [87-100] | 0/25 (0 %) | 0/25 (0 %) | 4/4 (100 %) | 1/25 (4 %) | 3/3 (100 %) | 0.69 $ |

## Question par question

ok juste, FAUX faux silencieux, err erreur d'exécution, abst abstention à tort, sig ambiguïté signalée, - ambiguïté non signalée, HALL réponse inventée hors périmètre. Plusieurs répétitions : une issue par répétition.

| Question | Cat. | vague1_haiku_documente | vague2_haiku_documente | haiku_agent_documente | opus_agent_documente_dev | opus_agent_documente_test |
|---|---|---|---|---|---|---|
| affluence_finale | hors_ | ok | ok | ok | ok |  |
| age_buteurs | hors_ | ok | ok | ok | ok |  |
| arbitre_plus_matchs | class | ok | ok | ok | ok |  |
| but_plus_rapide | class | ok | ok | ok | ok |  |
| but_xg_min | class | ok | ok | ok |  | ok |
| buteurs_distincts | compt | ok | ok | ok | ok |  |
| buts_coup_franc | compt | FAUX | FAUX | ok |  | ok |
| buts_france | compt | FAUX | ok | ok | ok |  |
| buts_prolongation | compt | ok | ok | ok |  | ok |
| buts_temps_additionnel | compt | FAUX | FAUX | FAUX | ok |  |
| buts_tete | compt | ok | ok | ok |  | ok |
| buts_total | compt | ok | ok | ok |  | ok |
| cartons_jaunes | ambig | - | - | - | sig |  |
| centres_angleterre | compt | ok | ok | ok | ok |  |
| classement_xg_top5 | class | ok | ok | ok |  | ok |
| club_kane | hors_ | ok | ok | ok | ok |  |
| corners_equipe | class | ok | ok | ok | ok |  |
| dernier_tiers_proportion | class | ok | ok | ok | ok |  |
| distance_parcourue | hors_ | ok | ok | HALL |  | ok |
| dribbles_reussis | class | FAUX | ok | ok | ok |  |
| duree_possession | ratio | ok | ok | ok | ok |  |
| equipe_plus_xg | class | ok | ok | ok | ok |  |
| fautes_par_match | class | ok | ok | ok |  | ok |
| fautes_uruguay | compt | ok | ok | ok | ok |  |
| france_2022 | hors_ | ok | ok | ok |  | ok |
| joueurs_expulses | liste | ok | ok | ok |  | ok |
| match_plus_buts | class | ok | ok | ok | ok |  |
| matchs_croatie | compt | ok | ok | ok |  | ok |
| matchs_nuls | ambig | - | - | - | sig |  |
| meilleur_buteur | class | ok | ok | ok |  | ok |
| meilleur_joueur | ambig | sig | - | sig |  | sig |
| meilleur_passeur | ambig | - | - | - | sig |  |
| meilleur_taux_passes | class | ok | ok | ok |  | ok |
| meilleure_defense | ambig | - | - | sig |  | sig |
| nb_csc | compt | ok | ok | ok | ok |  |
| nb_matchs | compt | ok | ok | ok | ok |  |
| nb_remplacements | compt | ok | ok | ok | ok |  |
| nb_seances_tab | compt | ok | ok | ok |  | ok |
| part_buts_premiere_periode | ratio | FAUX | FAUX | FAUX |  | ok |
| passes_dec_eden_hazard | compt | ok | ok | ok | ok |  |
| passes_dec_hazard | ambig | - | - | - |  | sig |
| passes_modric | compt | FAUX | FAUX | ok | ok |  |
| passes_profondeur | compt | ok | ok | ok |  | ok |
| passes_reussies_joueur | class | ok | ok | ok |  | ok |
| pays_plus_buteurs | class | ok | ok | ok | ok |  |
| penalties_jeu | compt | ok | ok | ok |  | ok |
| penalties_transformes | compt | ok | ok | ok | ok |  |
| plus_encaisse | class | ok | ok | ok |  | ok |
| possession_dominante | ambig | sig | sig | - | sig |  |
| possessions_tir_belgique | compt | ok | ok | ok |  | ok |
| sans_victoire_groupes | compt | ok | ok | ok |  | ok |
| stade_finale | liste | ok | ok | ok | ok |  |
| taux_cadres_france | ratio | ok | ok | ok | ok |  |
| taux_passes_espagne | ratio | ok | ok | ok | ok |  |
| tirs_cadres_joueur | class | ok | ok | ok |  | ok |
| tirs_concedes | class | ok | ok | ok |  | ok |
| tirs_croatie | compt | ok | ok | ok | ok |  |
| tirs_finale | compt | ok | ok | FAUX | ok |  |
| tirs_hors_surface | class | ok | ok | ok | ok |  |
| tirs_mbappe | compt | FAUX | ok | ok |  | ok |
| tirs_par_match | ratio | ok | ok | ok |  | ok |
| titulaires_france | compt | err | err | FAUX |  | ok |
| vainqueur | liste | ok | ok | ok |  | ok |
| vainqueurs_tab | liste | ok | ok | ok | ok |  |
| victoires_russie | ambig | - | - | - |  | sig |
| vitesse_tir | hors_ | ok | ok | ok |  | ok |
