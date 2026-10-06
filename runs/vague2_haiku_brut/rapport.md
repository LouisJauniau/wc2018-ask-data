# Run vague2_haiku_brut

| Paramètre | Valeur |
|---|---|
| fournisseur / modèle | rejeu / haiku-sous-agent |
| variante du prompt | brut |
| mode | direct |
| répétitions | 1 |
| jeu / prompt | 7a8956439f6a / e1eccf5679a5 |
| date | 2026-10-06T15:32:10 |

Réponses rejouées depuis un fichier. Lignes illisibles : 0. Corrections de format : aucune.

## Synthèse

| Mesure | Effectif (IC 95 %) |
|---|---|
| **Exactitude**, questions répondables | 23/52 (44 %) [32-58] |
| **Faux silencieux** : s'exécute, renvoie un faux résultat | 24/52 (46 %) [33-59] |
| Part de faux parmi les réponses qui s'exécutent | 24/47 (51 %) [37-65] |
| Erreurs d'exécution (requête finale) | 1/52 (2 %) [0-10] |
| Abstentions à tort | 4/52 (8 %) [3-18] |
| Ambiguïtés signalées | 1/8 (12 %) [2-47] |
| Réponse conforme à une interprétation (ambiguës) | 4/6 (67 %) [30-90] |
| Faux signalements : question claire jugée ambiguë | 5/52 (10 %) [4-21] |
| Hors périmètre : abstention juste | 6/6 (100 %) [61-100] |
| Hors périmètre : réponse inventée | 0/6 (0 %) [0-39] |
| Incidents (pas de réponse, refus, exception) | 0 |

Jetons : 0 en entrée, 0 lus en cache, 0 en sortie, 0 appels. Durée moyenne par question : 0.0 s.

## Par split

| Split | Exactitude | Faux silencieux | Ambiguïtés signalées | Hors périmètre refusé |
|---|---|---|---|---|
| dev | 13/27 (48 %) [31-66] | 12/27 (44 %) | 1/4 (25 %) | 3/3 (100 %) |
| test | 10/25 (40 %) [23-59] | 12/25 (48 %) | 0/4 (0 %) | 3/3 (100 %) |

## Par catégorie

| Catégorie | Justes | Faux silencieux | Erreurs |
|---|---|---|---|
| classement | 10/18 (56 %) | 7 | 1 |
| comptage | 10/25 (40 %) | 12 | 0 |
| liste | 2/4 (50 %) | 1 | 0 |
| ratio | 1/5 (20 %) | 4 | 0 |

## Par piège

Taux d'échec des questions répondables qui portent le piège. Une question porte souvent plusieurs pièges : ces lignes ne s'additionnent pas.

| Piège | Questions | Échecs |
|---|---|---|
| csc | 6 | 6/6 (100 %) |
| passe_reussie_null | 5 | 5/5 (100 %) |
| jsonb | 2 | 2/2 (100 %) |
| accents | 2 | 2/2 (100 %) |
| convention_corner | 1 | 1/1 (100 %) |
| cartons_deux_types | 1 | 1/1 (100 %) |
| geometrie_surface | 1 | 1/1 (100 %) |
| nom_complet | 1 | 1/1 (100 %) |
| jsonb_tableau | 1 | 1/1 (100 %) |
| seance_tab | 17 | 13/17 (76 %) |
| periode_ou_minute | 3 | 2/3 (67 %) |
| buts_par_le_score | 3 | 2/3 (67 %) |
| ratio | 5 | 3/5 (60 %) |
| noms_en_anglais | 9 | 4/9 (44 %) |
| table_derivee | 3 | 1/3 (33 %) |
| domicile_exterieur | 5 | 1/5 (20 %) |
| libelle_stage | 3 | 0/3 (0 %) |
| faute_commise_ou_subie | 2 | 0/2 (0 %) |
| convention_cadre | 2 | 0/2 (0 %) |
| normalisation_par_match | 1 | 0/1 (0 %) |
| egalite | 1 | 0/1 (0 %) |
| adversaire | 1 | 0/1 (0 %) |

## Forme des faux silencieux

| Diagnostic | Nombre |
|---|---|
| valeurs | 16 |
| entites | 5 |
| vide | 3 |

## Détail des échecs

### buteurs_distincts (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buteurs \| attendu ('n_buteurs',) [[110]] \| obtenu ('joueurs_buteurs',) [[123]]

```sql
SELECT COUNT(DISTINCT e.player_id) as joueurs_buteurs FROM sb.events e JOIN sb.shots s ON e.event_id = s.event_id WHERE s.outcome = 'Goal';
```

### buts_coup_franc (rép. 0) : abstention_a_tort, hors_perimetre

### buts_france (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('n_buts',) [[14]] \| obtenu ('team_name', 'buts') [['France', 12]]

```sql
SELECT t.team_name, COUNT(*) as buts FROM sb.events e JOIN sb.shots s ON e.event_id = s.event_id JOIN sb.teams t ON e.team_id = t.team_id WHERE t.team_name = 'France' AND s.outcome = 'Goal' GROUP BY t.team_id, t.team_name;
```

### buts_prolongation (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('n_buts',) [[3]] \| obtenu ('extra_time_goals',) [[29]]

```sql
SELECT COUNT(*) as extra_time_goals FROM sb.shots sh JOIN sb.events e ON sh.event_id = e.event_id WHERE sh.outcome = 'Goal' AND e.period > 2
```

### buts_temps_additionnel (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('n_buts',) [[19]] \| obtenu ('buts_temps_additionnel_p2',) [[96]]

```sql
SELECT COUNT(*) as buts_temps_additionnel_p2 FROM sb.events e JOIN sb.shots s ON e.event_id = s.event_id WHERE e.period = 2 AND e.minute > 45 AND s.outcome = 'Goal';
```

### buts_total (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('n_buts',) [[169]] \| obtenu ('total_goals',) [[183]]

```sql
SELECT COUNT(*) as total_goals FROM sb.shots WHERE outcome = 'Goal'
```

### classement_xg_top5 (rép. 0) : faux_silencieux, entites

introuvable dans le resultat : joueur \| attendu ('joueur', 'xg') [['Neymar da Silva Santos Junior', 4.178492526], ['Harry Kane', 4.027905531], ['Antoine Griezmann', 3.556915921]] \| obtenu ('player_name', 'total_xg') [['Harry Kane', 4.811405531], ['Neymar da Silva Santos Junior', 4.178492526], ['Antoine Griezmann', 3.556915921]]

```sql
SELECT pl.player_name, SUM(sh.statsbomb_xg) as total_xg FROM sb.shots sh JOIN sb.events e ON sh.event_id = e.event_id JOIN sb.players pl ON e.player_id = pl.player_id GROUP BY pl.player_id, pl.player_name ORDER BY total_xg DESC LIMIT 5
```

### corners_equipe (rép. 0) : faux_silencieux, entites

introuvable dans le resultat : equipe \| attendu ('equipe', 'n_corners') [['Brazil', 41]] \| obtenu ('team_name', 'corners') [['France', 87], ['Brazil', 64], ['Croatia', 58]]

```sql
SELECT t.team_name, COUNT(*) as corners FROM sb.events e JOIN sb.teams t ON e.team_id = t.team_id WHERE e.type = 'Dispossessed' OR e.play_pattern = 'Corner Kick' GROUP BY t.team_id, t.team_name ORDER BY corners DESC;
```

### dribbles_reussis (rép. 0) : faux_silencieux, entites

introuvable dans le resultat : joueur \| attendu ('joueur', 'n_dribbles') [['Francisco Román Alarcón Suárez', 30]] \| obtenu ('player_name', 'dribbles_reussis') [['Kylian Mbappé Lottin', 52], ['Neymar da Silva Santos Junior', 43], ['Eden Hazard', 42]]

```sql
SELECT pl.player_name, COUNT(*) as dribbles_reussis FROM sb.events e JOIN sb.players pl ON e.player_id = pl.player_id WHERE e.type = 'Dribble' AND (e.details->>'outcome' = 'Successful' OR e.counterpress = false) GROUP BY pl.player_id, pl.player_name ORDER BY dribbles_reussis DESC;
```

### duree_possession (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : duree_moyenne \| attendu ('duree_moyenne',) [[21.08106169296987]] \| obtenu ('duree_moyenne',) [[20.995981784087864]]

```sql
SELECT AVG(duration_seconds) as duree_moyenne FROM sb.possessions WHERE play_pattern != 'Penalty Shootout';
```

### equipe_plus_xg (rép. 0) : faux_silencieux, entites

introuvable dans le resultat : equipe \| attendu ('equipe', 'xg') [['Belgium', 12.7244262895]] \| obtenu ('team_name', 'total_xg') [['Croatia', 19.0870290802], ['England', 15.7975037083], ['Belgium', 12.7039656315]]

```sql
SELECT t.team_name, SUM(sum_xg) as total_xg FROM sb.possessions p JOIN sb.teams t ON p.team_id = t.team_id GROUP BY t.team_id, t.team_name ORDER BY total_xg DESC;
```

### joueurs_expulses (rép. 0) : abstention_a_tort, hors_perimetre

### matchs_nuls (rép. 0) : non_signalee

```sql
SELECT COUNT(*) as matchs_nuls FROM sb.matches WHERE home_score = away_score;
```

### meilleur_buteur (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_buts \| attendu ('joueur', 'n_buts') [['Harry Kane', 6]] \| obtenu ('player_name', 'goals') [['Harry Kane', 7], ['Denis Cheryshev', 5], ['Cristiano Ronaldo dos Santos Aveiro', 4]]

```sql
SELECT pl.player_name, COUNT(*) as goals FROM sb.shots sh JOIN sb.events e ON sh.event_id = e.event_id JOIN sb.players pl ON e.player_id = pl.player_id WHERE sh.outcome = 'Goal' GROUP BY pl.player_id, pl.player_name ORDER BY goals DESC
```

### meilleur_joueur (rép. 0) : non_signalee

### meilleur_passeur (rép. 0) : non_signalee

```sql
SELECT pl.player_name, COUNT(*) as passes_decisives FROM sb.passes p JOIN sb.players pl ON p.recipient_id = pl.player_id WHERE p.goal_assist = true GROUP BY pl.player_id, pl.player_name ORDER BY passes_decisives DESC;
```

### meilleur_taux_passes (rép. 0) : faux_silencieux, entites

introuvable dans le resultat : equipe \| attendu ('equipe', 'taux') [['Spain', 0.8938961779806047]] \| obtenu ('team_name', 'pass_completion_rate') [['England', 0.0], ['Colombia', 0.0], ['Germany', 0.0]]

```sql
SELECT t.team_name, COUNT(CASE WHEN p.outcome = 'Complete' THEN 1 END)::NUMERIC / NULLIF(COUNT(*), 0) as pass_completion_rate FROM sb.passes p JOIN sb.events e ON p.event_id = e.event_id JOIN sb.teams t ON e.team_id = t.team_id GROUP BY t.team_id, t.team_name ORDER BY pass_completion_rate DESC
```

### meilleure_defense (rép. 0) : non_signalee

```sql
SELECT t.team_name, COALESCE(SUM(CASE WHEN m.home_team_id = t.team_id THEN m.away_score ELSE 0 END), 0) + COALESCE(SUM(CASE WHEN m.away_team_id = t.team_id THEN m.home_score ELSE 0 END), 0) as goals_conceded FROM sb.teams t JOIN sb.matches m ON (m.home_team_id = t.team_id OR m.away_team_id = t.team_id) GROUP BY t.team_id, t.team_name ORDER BY goals_conceded ASC
```

### nb_csc (rép. 0) : abstention_a_tort, hors_perimetre

### nb_seances_tab (rép. 0) : abstention_a_tort, hors_perimetre

### part_buts_premiere_periode (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : part \| attendu ('part',) [[0.38461538461538464]] \| obtenu ('first_period_share',) [[0.31693989071038253]]

```sql
SELECT COUNT(CASE WHEN e.period = 1 THEN 1 END)::NUMERIC / NULLIF(COUNT(*), 0) as first_period_share FROM sb.shots sh JOIN sb.events e ON sh.event_id = e.event_id WHERE sh.outcome = 'Goal'
```

### passes_dec_hazard (rép. 0) : non_signalee

```sql
SELECT COUNT(*) as goal_assists FROM sb.passes p JOIN sb.events e ON p.event_id = e.event_id JOIN sb.players pl ON e.player_id = pl.player_id WHERE pl.player_name ILIKE '%Hazard%' AND p.goal_assist = true
```

### passes_modric (rép. 0) : faux_silencieux, vide

aucune ligne obtenue \| attendu ('n_passes',) [[430]] \| obtenu ('player_name', 'passes_reussies') []

```sql
SELECT pl.player_name, COUNT(*) as passes_reussies FROM sb.passes p JOIN sb.events e ON p.event_id = e.event_id JOIN sb.players pl ON e.player_id = pl.player_id WHERE pl.player_name = 'Luka Modric' AND p.outcome = 'Successful' GROUP BY pl.player_id, pl.player_name;
```

### passes_profondeur (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_passes \| attendu ('n_passes',) [[42]] \| obtenu ('successful_through_balls',) [[0]]

```sql
SELECT COUNT(*) as successful_through_balls FROM sb.passes WHERE is_through_ball = true AND outcome = 'Complete'
```

### passes_reussies_joueur (rép. 0) : faux_silencieux, vide

aucune ligne obtenue \| attendu ('joueur', 'n_passes') [['Sergio Ramos García', 469]] \| obtenu ('player_name', 'successful_passes') []

```sql
SELECT pl.player_name, COUNT(*) as successful_passes FROM sb.passes p JOIN sb.events e ON p.event_id = e.event_id JOIN sb.players pl ON e.player_id = pl.player_id WHERE p.outcome = 'Complete' GROUP BY pl.player_id, pl.player_name ORDER BY successful_passes DESC
```

### penalties_jeu (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_penalties \| attendu ('n_penalties',) [[29]] \| obtenu ('penalties',) [[0]]

```sql
SELECT COUNT(*) as penalties FROM sb.passes WHERE pass_type = 'Penalty'
```

### penalties_transformes (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_penalties_marques \| attendu ('n_penalties_marques',) [[22]] \| obtenu ('penalties_marques',) [[48]]

```sql
SELECT COUNT(*) as penalties_marques FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id WHERE s.shot_type = 'Penalty' AND s.outcome = 'Goal';
```

### possession_dominante (rép. 0) : non_signalee

```sql
SELECT t.team_name, SUM(duration_seconds) as total_possession_seconds FROM sb.possessions p JOIN sb.teams t ON p.team_id = t.team_id GROUP BY t.team_id, t.team_name ORDER BY total_possession_seconds DESC;
```

### taux_passes_espagne (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : taux \| attendu ('taux',) [[0.8938961779806047]] \| obtenu ('team_name', 'taux_passes_reussies') [['Spain', 0.0]]

```sql
SELECT t.team_name, SUM(CASE WHEN p.outcome = 'Successful' THEN 1 ELSE 0 END)::float / COUNT(*) as taux_passes_reussies FROM sb.passes p JOIN sb.events e ON p.event_id = e.event_id JOIN sb.teams t ON e.team_id = t.team_id WHERE t.team_name = 'Spain' GROUP BY t.team_id, t.team_name;
```

### tirs_croatie (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_tirs \| attendu ('n_tirs',) [[114]] \| obtenu ('tirs',) [[124]]

```sql
SELECT COUNT(*) as tirs FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id JOIN sb.teams t ON e.team_id = t.team_id WHERE t.team_name = 'Croatia';
```

### tirs_hors_surface (rép. 0) : erreur_execution, 42703: ERROR:  column s.loc_x does not exist

```sql
SELECT t.team_name, COUNT(*) as tirs_hors_surface FROM sb.shots s JOIN sb.events e ON s.event_id = e.event_id JOIN sb.teams t ON e.team_id = t.team_id WHERE s.loc_x < 102 ORDER BY tirs_hors_surface DESC;
```

### tirs_mbappe (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_tirs \| attendu ('n_tirs',) [[8]] \| obtenu ('shots',) [[0]]

```sql
SELECT COUNT(*) as shots FROM sb.shots sh JOIN sb.events e ON sh.event_id = e.event_id JOIN sb.players pl ON e.player_id = pl.player_id WHERE pl.player_name ILIKE '%Mbappe%'
```

### tirs_par_match (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : tirs_par_match \| attendu ('tirs_par_match',) [[26.046875]] \| obtenu ('avg_shots_per_match',) [[26.65625]]

```sql
SELECT COUNT(*)::NUMERIC / NULLIF((SELECT COUNT(*) FROM sb.matches), 0) as avg_shots_per_match FROM sb.shots
```

### titulaires_france (rép. 0) : faux_silencieux, valeurs

introuvable dans le resultat : n_joueurs \| attendu ('n_joueurs',) [[18]] \| obtenu ('players_fielded',) [[23]]

```sql
SELECT COUNT(DISTINCT l.player_id) as players_fielded FROM sb.lineups l JOIN sb.teams t ON l.team_id = t.team_id WHERE t.team_name ILIKE '%France%'
```

### vainqueurs_tab (rép. 0) : faux_silencieux, vide

aucune ligne obtenue \| attendu ('equipe', 'n_seances_gagnees') [['Croatia', 2], ['England', 1], ['Russia', 1]] \| obtenu ('team_name', 'victoires_tao') []

```sql
SELECT t.team_name, COUNT(*) as victoires_tao FROM sb.possessions p JOIN sb.teams t ON p.team_id = t.team_id WHERE p.play_pattern = 'Penalty Shootout' AND p.produced_goal = true GROUP BY t.team_id, t.team_name ORDER BY victoires_tao DESC;
```

### victoires_russie (rép. 0) : non_signalee

