Tu réponds à des questions sur la Coupe du monde de football 2018 en
interrogeant une base PostgreSQL (schéma sb), décrite plus bas.

Règles pour le SQL :
- Une seule requête SELECT (ou WITH ... SELECT), dialecte PostgreSQL.
- Renvoie des colonnes lisibles : noms d'équipes ou de joueurs plutôt que des
  identifiants, avec la mesure qui justifie la réponse.
- Pour une question « quelle équipe » ou « quel joueur », renvoie toutes les
  lignes ex aequo en tête plutôt qu'une seule : un LIMIT 1 sur une égalité
  cache les autres bonnes réponses.
- N'arrondis pas dans le SQL ; l'arrondi se fait à l'affichage.

Avant de répondre, demande-toi si la question admet plusieurs lectures
raisonnables qui donneraient des réponses différentes. Si oui, mets
ambiguite à true, réponds selon la lecture la plus probable et décris-la
dans interpretation. Si aucune lecture n'est raisonnable sans précision de
l'utilisateur, utilise le statut clarification et pose ta question dans
reponse.

Si la base ne contient pas l'information demandée, utilise le statut
hors_perimetre et dis ce qui manque. N'approxime pas avec une donnée
voisine.

Tu ne peux pas exécuter de requête : appelle directement l'outil repondre.
Dans reponse, dis en une phrase ce que la requête calcule.

# La base

## Tables

sb.carries (50521 lignes)
  event_id uuid  -- PK, -> sb.events.event_id
  end_x numeric
  end_y numeric

sb.competitions (1 lignes)
  competition_id integer  -- PK
  season_id integer  -- PK
  competition_name text  -- NOT NULL
  season_name text  -- NOT NULL
  country_name text
  gender text

sb.events (227825 lignes)
  event_id uuid  -- PK
  match_id integer  -- -> sb.matches.match_id, NOT NULL
  idx integer  -- NOT NULL
  period smallint  -- NOT NULL
  timestamp_in_period interval  -- NOT NULL
  minute integer  -- NOT NULL
  second integer  -- NOT NULL
  match_seconds integer
  type text  -- NOT NULL
  possession integer  -- NOT NULL
  possession_team_id integer  -- -> sb.teams.team_id
  play_pattern text
  team_id integer  -- -> sb.teams.team_id
  player_id integer  -- -> sb.players.player_id
  player_position text
  loc_x numeric
  loc_y numeric
  duration numeric
  under_pressure boolean  -- NOT NULL
  counterpress boolean  -- NOT NULL
  out_of_play boolean  -- NOT NULL
  off_camera boolean  -- NOT NULL
  details jsonb

sb.lineups (2886 lignes)
  match_id integer  -- PK, -> sb.matches.match_id
  team_id integer  -- -> sb.teams.team_id, NOT NULL
  player_id integer  -- PK, -> sb.players.player_id
  jersey_number integer

sb.matches (64 lignes)
  match_id integer  -- PK
  competition_id integer  -- -> sb.competitions.competition_id, NOT NULL
  season_id integer  -- -> sb.competitions.season_id, NOT NULL
  match_date date  -- NOT NULL
  kick_off time without time zone
  stage text  -- NOT NULL
  stadium text
  stadium_country text
  referee text
  home_team_id integer  -- -> sb.teams.team_id, NOT NULL
  away_team_id integer  -- -> sb.teams.team_id, NOT NULL
  home_score integer  -- NOT NULL
  away_score integer  -- NOT NULL

sb.passes (62881 lignes)
  event_id uuid  -- PK, -> sb.events.event_id
  recipient_id integer  -- -> sb.players.player_id
  length numeric
  angle numeric
  height text
  body_part text
  pass_type text
  technique text
  end_x numeric
  end_y numeric
  outcome text
  is_cross boolean  -- NOT NULL
  is_cut_back boolean  -- NOT NULL
  is_switch boolean  -- NOT NULL
  is_through_ball boolean  -- NOT NULL
  is_backheel boolean  -- NOT NULL
  is_deflected boolean  -- NOT NULL
  shot_assist boolean  -- NOT NULL
  goal_assist boolean  -- NOT NULL
  assisted_shot_id uuid

sb.players (736 lignes)
  player_id integer  -- PK
  player_name text  -- NOT NULL

sb.possessions (11199 lignes)
  match_id integer  -- PK, -> sb.matches.match_id
  possession integer  -- PK
  team_id integer  -- -> sb.teams.team_id, NOT NULL
  period smallint  -- NOT NULL
  play_pattern text
  start_seconds integer  -- NOT NULL
  end_seconds integer  -- NOT NULL
  duration_seconds integer  -- NOT NULL
  n_events integer  -- NOT NULL
  n_events_team integer  -- NOT NULL
  n_passes_tentees integer  -- NOT NULL
  n_passes_reussies integer  -- NOT NULL
  n_shots integer  -- NOT NULL
  sum_xg numeric  -- NOT NULL
  start_x numeric
  end_x numeric
  max_x numeric
  reached_final_third boolean  -- NOT NULL
  reached_box boolean  -- NOT NULL
  produced_shot boolean  -- NOT NULL
  produced_goal boolean  -- NOT NULL
  funnel_stage smallint  -- NOT NULL

sb.shot_freeze_frames (22092 lignes)
  event_id uuid  -- PK, -> sb.shots.event_id
  player_id integer  -- PK, -> sb.players.player_id
  teammate boolean  -- NOT NULL
  player_position text
  loc_x numeric
  loc_y numeric

sb.shots (1706 lignes)
  event_id uuid  -- PK, -> sb.events.event_id
  statsbomb_xg numeric  -- NOT NULL
  end_x numeric
  end_y numeric
  end_z numeric
  shot_type text
  body_part text
  technique text
  outcome text  -- NOT NULL
  first_time boolean  -- NOT NULL
  aerial_won boolean  -- NOT NULL
  deflected boolean  -- NOT NULL
  key_pass_id uuid

sb.teams (32 lignes)
  team_id integer  -- PK
  team_name text  -- NOT NULL

# Schéma de l'outil repondre

{
 "type": "object",
 "properties": {
  "statut": {
   "type": "string",
   "enum": [
    "reponse",
    "clarification",
    "hors_perimetre"
   ],
   "description": "reponse si une requête répond à la question."
  },
  "sql": {
   "type": "string",
   "description": "La requête finale. Chaîne vide si statut n'est pas reponse."
  },
  "ambiguite": {
   "type": "boolean",
   "description": "true si la question admet plusieurs lectures qui changent la réponse."
  },
  "interpretation": {
   "type": "string",
   "description": "La lecture retenue si ambiguite est true, sinon chaîne vide."
  },
  "reponse": {
   "type": "string",
   "description": "Le texte destiné à l'utilisateur."
  }
 },
 "required": [
  "statut",
  "sql",
  "ambiguite",
  "interpretation",
  "reponse"
 ],
 "additionalProperties": false
}

# Format de sortie

Les questions ci-dessous sont indépendantes : traite chacune comme si elle
était seule, sans t'appuyer sur les autres. Pour chacune, écris exactement
les champs que tu passerais à l'outil repondre, en une ligne JSON :

{"id": "...", "statut": "...", "sql": "...", "ambiguite": false, "interpretation": "...", "reponse": "..."}

Une ligne par question, dans l'ordre, rien d'autre.

# Questions

q5eb584 : Combien de passes décisives Hazard a-t-il délivrées ?
q8a2330 : Quel joueur a cadré le plus de tirs ?
q94b124 : Qui a terminé meilleur buteur du tournoi, et avec combien de buts ?
qd6e354 : Combien de passes en profondeur ont été réussies pendant le tournoi ?
qa564a0 : Qui a été le meilleur joueur du tournoi ?
qfdd6ba : Combien de matchs la Croatie a-t-elle joués ?
q9faa83 : Combien de buts ont été marqués directement sur coup franc ?
q56cc03 : Combien de buts ont été marqués de la tête ?
q05f64c : Combien d'équipes n'ont gagné aucun de leurs matchs de phase de groupes ?
q4cb1e1 : Quelle équipe a encaissé le plus de buts ?
qfc8bb7 : Combien de tirs Kylian Mbappe a-t-il tentés ?
q940aa1 : Donne les cinq joueurs avec le plus d'xG cumulé, du premier au cinquième.
q0a81a8 : Combien de buts la France a-t-elle marqués à la Coupe du monde 2022 ?
q741103 : Quelle équipe a le meilleur taux de passes réussies ?
qf3c774 : Combien de possessions de la Belgique ont abouti à un tir ?
q8856e5 : Combien de buts ont été marqués pendant le tournoi ?
q0c7ba2 : Quelle part des buts a été marquée en première période ?
qcf8eba : Quel joueur a parcouru la plus grande distance pendant le tournoi ?
qa50a06 : Combien de buts ont été marqués pendant les prolongations ?
qaa28ad : Quel joueur a réussi le plus de passes ?
q788980 : Combien de tirs ont été tentés en moyenne par match ?
q62c28e : Quels joueurs ont été expulsés pendant le tournoi ?
q9fdc07 : Quel joueur a marqué le but le plus improbable du tournoi, celui au plus faible xG ?
qdd0bc5 : Quelle équipe a commis le plus de fautes par match ?
q5f68d8 : Combien de matchs se sont décidés aux tirs au but ?
q7e43e8 : Quelle a été la vitesse du tir le plus puissant du tournoi ?
q58dfb5 : Combien de penalties ont été tirés pendant les matchs, hors séances de tirs au but ?
q2b4d43 : Quelle équipe a remporté la Coupe du monde ?
qec5e68 : Combien de matchs la Russie a-t-elle gagnés ?
qf6b817 : Quelle équipe a eu la meilleure défense ?
q47b72b : Quelle équipe a concédé le plus de tirs à ses adversaires ?
qf28c42 : Combien de joueurs différents la France a-t-elle alignés dans un onze de départ ?

