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

## Valeurs des colonnes texte

sb.competitions.competition_name : 'FIFA World Cup'
sb.competitions.season_name : '2018'
sb.competitions.country_name : 'International'
sb.competitions.gender : 'male'
sb.events.type : 'Pass', 'Ball Receipt*', 'Carry', 'Pressure', 'Ball Recovery', 'Duel', 'Block', 'Dribble', 'Clearance', 'Goal Keeper', 'Foul Committed', 'Foul Won', 'Camera On', 'Shot', 'Miscontrol', 'Dribbled Past', 'Interception', 'Dispossessed', 'Camera off', 'Substitution', 'Injury Stoppage', 'Half Start', 'Half End', 'Starting XI', 'Tactical Shift', '50/50', 'Player Off', 'Player On', 'Referee Ball-Drop', 'Shield', 'Bad Behaviour', 'Error', 'Offside', 'Own Goal For', 'Own Goal Against'
sb.events.play_pattern : 'Regular Play', 'From Throw In', 'From Free Kick', 'From Goal Kick', 'From Corner', 'From Kick Off', 'From Keeper', 'From Counter', 'Other'
sb.events.player_position : 'Right Center Back', 'Left Center Back', 'Left Center Midfield', 'Right Back', 'Left Back', 'Right Center Midfield', 'Left Wing', 'Right Wing', 'Center Forward', 'Center Attacking Midfield', 'Goalkeeper', 'Left Midfield', 'Right Midfield', 'Center Defensive Midfield', 'Right Defensive Midfield', 'Left Defensive Midfield', 'Right Center Forward', 'Left Center Forward', 'Center Back', 'Right Wing Back', 'Left Attacking Midfield', 'Left Wing Back', 'Right Attacking Midfield', 'Center Midfield', 'Secondary Striker'
sb.matches.stage : 'Group Stage', 'Round of 16', 'Quarter-finals', 'Semi-finals', '3rd Place Final', 'Final'
sb.matches.stadium : 'Saint-Petersburg Stadium ( Gazprom Arena )', 'Stadion Luzhniki', 'Ak Bars Arena', 'Solidarnost Arena', 'Stadion Nizhny Novgorod (Nizhniy Novgorod)', 'Olimpiyskiy Stadion Fisht', 'Otkritie Bank Arena', 'Rostov Arena', 'Rostec Arena', 'Ekaterinburg Arena', 'Mordovia Arena', 'Volgograd Arena'
sb.matches.stadium_country : 'Russia'
sb.matches.referee : 'Néstor Fabián Pitana', 'Björn Kuipers', 'Alireza Faghani', 'César Arturo Ramos Palazuelos', 'Damir Skomina', 'Gianluca Rocchi', 'Malang Diedhiou', 'Milorad Mažić', 'Mark Geiger', 'Andrés Cunha', 'Cüneyt Çakιr', 'Sandro Ricci', 'Ravshan Irmatov', 'Nawaf Abdulla Ghayyath Shukralla', 'Enrique Cáceres', 'Wilmar Alexander Roldán Pérez', 'Szymon Marciniak', 'Janny Sikazwe', 'Antonio Miguel Mateu Lahoz', 'Clément Turpin', 'Ghead Grisha', 'Bakary Papa Gassama', 'Mohamed Abdulla Hassan Mohd', 'Sergey Karasev', 'Joel Antonio Aguilar Chicas', 'Matthew Conger', 'Felix Brych', 'Jair Marrufo'
sb.passes.height : 'Ground Pass', 'High Pass', 'Low Pass'
sb.passes.body_part : 'Right Foot', 'Left Foot', 'Head', 'Keeper Arm', 'Other', 'Drop Kick'
sb.passes.pass_type : 'Recovery', 'Throw-in', 'Free Kick', 'Goal Kick', 'Corner', 'Interception', 'Kick Off'
sb.passes.technique : 'Through Ball'
sb.passes.outcome : 'Incomplete', 'Out', 'Unknown', 'Pass Offside', 'Injury Clearance'
sb.possessions.play_pattern : 'Regular Play', 'From Throw In', 'From Free Kick', 'From Goal Kick', 'From Corner', 'From Keeper', 'From Kick Off', 'From Counter', 'Other'
sb.shot_freeze_frames.player_position : 'Left Center Back', 'Right Center Back', 'Right Back', 'Left Back', 'Goalkeeper', 'Left Center Midfield', 'Right Center Midfield', 'Center Forward', 'Right Wing', 'Left Wing', 'Left Midfield', 'Right Midfield', 'Center Attacking Midfield', 'Center Defensive Midfield', 'Right Center Forward', 'Left Center Forward', 'Left Defensive Midfield', 'Right Defensive Midfield', 'Center Back', 'Right Wing Back', 'Left Wing Back', 'Secondary Striker', 'Left Attacking Midfield', 'Right Attacking Midfield', 'Center Midfield'
sb.shots.shot_type : 'Open Play', 'Free Kick', 'Penalty'
sb.shots.body_part : 'Right Foot', 'Left Foot', 'Head', 'Other'
sb.shots.technique : 'Normal', 'Half Volley', 'Volley', 'Overhead Kick', 'Diving Header', 'Lob', 'Backheel'
sb.shots.outcome : 'Off T', 'Blocked', 'Saved', 'Goal', 'Wayward', 'Post'
sb.teams.team_name : 'Sweden', 'Portugal', 'Colombia', 'Saudi Arabia', 'France', 'Senegal', 'Iceland', 'Nigeria', 'Australia', 'Serbia', 'Spain', 'Belgium', 'Uruguay', 'Germany', 'South Korea', 'Argentina', 'England', 'Egypt', 'Iran', 'Peru', 'Japan', 'Denmark', 'Switzerland', 'Russia', 'Brazil', 'Panama', 'Croatia', 'Tunisia', 'Morocco', 'Mexico', 'Poland', 'Costa Rica'

## Champs de sb.events.details (jsonb), par type d'evenement

  type = '50/50'
    details -> '50_50' -> 'outcome' -> 'id' (number)
    details -> '50_50' -> 'outcome' -> 'name' (string) : 'Lost', 'Success To Opposition', 'Success To Team', 'Won'
  type = 'Bad Behaviour'
    details -> 'bad_behaviour' -> 'card' -> 'id' (number)
    details -> 'bad_behaviour' -> 'card' -> 'name' (string) : 'Yellow Card'
  type = 'Ball Receipt*'
    details -> 'ball_receipt' -> 'outcome' -> 'id' (number)
    details -> 'ball_receipt' -> 'outcome' -> 'name' (string) : 'Incomplete'
  type = 'Ball Recovery'
    details -> 'ball_recovery' -> 'offensive' (boolean)
    details -> 'ball_recovery' -> 'recovery_failure' (boolean)
  type = 'Block'
    details -> 'block' -> 'deflection' (boolean)
    details -> 'block' -> 'offensive' (boolean)
    details -> 'block' -> 'save_block' (boolean)
  type = 'Clearance'
    details -> 'clearance' -> 'aerial_won' (boolean)
  type = 'Dribble'
    details -> 'dribble' -> 'nutmeg' (boolean)
    details -> 'dribble' -> 'outcome' -> 'id' (number)
    details -> 'dribble' -> 'outcome' -> 'name' (string) : 'Complete', 'Incomplete'
    details -> 'dribble' -> 'overrun' (boolean)
  type = 'Duel'
    details -> 'duel' -> 'outcome' -> 'id' (number)
    details -> 'duel' -> 'outcome' -> 'name' (string) : 'Lost In Play', 'Lost Out', 'Success In Play', 'Success Out', 'Won'
    details -> 'duel' -> 'type' -> 'id' (number)
    details -> 'duel' -> 'type' -> 'name' (string) : 'Aerial Lost', 'Tackle'
  type = 'Foul Committed'
    details -> 'foul_committed' -> 'advantage' (boolean)
    details -> 'foul_committed' -> 'card' -> 'id' (number)
    details -> 'foul_committed' -> 'card' -> 'name' (string) : 'Red Card', 'Second Yellow', 'Yellow Card'
    details -> 'foul_committed' -> 'offensive' (boolean)
    details -> 'foul_committed' -> 'penalty' (boolean)
    details -> 'foul_committed' -> 'type' -> 'id' (number)
    details -> 'foul_committed' -> 'type' -> 'name' (string) : 'Dangerous Play', 'Dive', 'Foul Out', 'Handball'
  type = 'Foul Won'
    details -> 'foul_won' -> 'advantage' (boolean)
    details -> 'foul_won' -> 'defensive' (boolean)
    details -> 'foul_won' -> 'penalty' (boolean)
  type = 'Goal Keeper'
    details -> 'goalkeeper' -> 'body_part' -> 'id' (number)
    details -> 'goalkeeper' -> 'body_part' -> 'name' (string) : 'Both Hands', 'Chest', 'Head', 'Left Foot', 'Left Hand', 'Right Foot', 'Right Hand'
    details -> 'goalkeeper' -> 'end_location' (array)
    details -> 'goalkeeper' -> 'outcome' -> 'id' (number)
    details -> 'goalkeeper' -> 'outcome' -> 'name' (string) : 'Claim', 'Clear', 'Collected Twice', 'Fail', 'In Play Danger', 'In Play Safe', 'Lost', 'No Touch', 'Saved Twice', 'Success', 'Touched In', 'Touched Out', 'Won'
    details -> 'goalkeeper' -> 'position' -> 'id' (number)
    details -> 'goalkeeper' -> 'position' -> 'name' (string) : 'Moving', 'Prone', 'Set'
    details -> 'goalkeeper' -> 'technique' -> 'id' (number)
    details -> 'goalkeeper' -> 'technique' -> 'name' (string) : 'Diving', 'Standing'
    details -> 'goalkeeper' -> 'type' -> 'id' (number)
    details -> 'goalkeeper' -> 'type' -> 'name' (string) : 'Collected', 'Goal Conceded', 'Keeper Sweeper', 'Penalty Conceded', 'Penalty Saved', 'Punch', 'Save', 'Shot Faced', 'Shot Saved', 'Smother'
  type = 'Injury Stoppage'
    details -> 'injury_stoppage' -> 'in_chain' (boolean)
  type = 'Interception'
    details -> 'interception' -> 'outcome' -> 'id' (number)
    details -> 'interception' -> 'outcome' -> 'name' (string) : 'Lost In Play', 'Lost Out', 'Success In Play', 'Success Out', 'Won'
  type = 'Miscontrol'
    details -> 'miscontrol' -> 'aerial_won' (boolean)
  type = 'Starting XI'
    details -> 'tactics' -> 'formation' (number)
    details -> 'tactics' -> 'lineup' (array)
  type = 'Substitution'
    details -> 'substitution' -> 'outcome' -> 'id' (number)
    details -> 'substitution' -> 'outcome' -> 'name' (string) : 'Injury', 'Tactical'
    details -> 'substitution' -> 'replacement' -> 'id' (number)
    details -> 'substitution' -> 'replacement' -> 'name' (string)
  type = 'Tactical Shift'
    details -> 'tactics' -> 'formation' (number)
    details -> 'tactics' -> 'lineup' (array)

# Format de sortie

Les questions ci-dessous sont indépendantes : traite chacune comme si elle
était seule, sans t'appuyer sur les autres. Pour chacune, écris exactement
les champs que tu passerais à l'outil repondre, en une ligne JSON :

{"id": "...", "statut": "...", "sql": "...", "ambiguite": false, "interpretation": "...", "reponse": "..."}

Une ligne par question, dans l'ordre, rien d'autre.

# Questions

qe3bf6d : Combien de remplacements ont été effectués au total ?
q9661c4 : Combien de matchs ont été disputés pendant la Coupe du monde 2018 ?
q38e5c6 : Combien de cartons jaunes ont été distribués ?
q3831a6 : Qui a marqué le but le plus rapide du tournoi, compté depuis le coup d'envoi ?
qb1e97d : Combien de passes Luka Modric a-t-il réussies ?
q46f7a4 : Combien de fautes l'Uruguay a-t-il commises ?
q8746ad : Quelle équipe a tiré le plus de corners ?
q03305b : Quelle équipe a tenté le plus de tirs hors de la surface ?
qee754a : Combien de buts contre son camp ont été inscrits ?
qefbc18 : Quelle équipe atteint le dernier tiers adverse sur la plus grande proportion de ses possessions ?
q1e1290 : Combien de spectateurs ont assisté à la finale ?
q713e71 : Quel est le taux de passes réussies de l'Espagne ?
q233f25 : Quelle est la durée moyenne d'une possession en secondes, hors séances de tirs au but ?
q22854f : Dans quel club jouait Harry Kane pendant la Coupe du monde ?
q44881c : Quelle équipe a cumulé le plus d'expected goals (xG) ?
qd694af : Qui a été le meilleur passeur du tournoi ?
qd0a30b : Combien de tirs ont été tentés lors de la finale ?
q8d0402 : Quel arbitre a dirigé le plus de matchs ?
qbc30e1 : Quel est l'âge moyen des buteurs du tournoi ?
q2c1e13 : Combien de penalties ont été transformés en cours de match ?
q7103d4 : Quelle équipe a eu le plus la possession du ballon ?
qd83ede : Combien de passes décisives Eden Hazard a-t-il délivrées ?
q314c85 : Quelle équipe compte le plus de buteurs différents ?
q6b3d1e : Combien de centres l'Angleterre a-t-elle tentés ?
q1bccc5 : Combien de matchs se sont terminés sur un match nul ?
q498a90 : Combien de joueurs différents ont marqué au moins un but ?
qff14f4 : Dans quel stade la finale s'est-elle jouée ?
q15b114 : Combien de tirs la Croatie a-t-elle tentés ?
qdf4989 : Quel joueur a réussi le plus de dribbles ?
q5c9029 : Quel match a été le plus riche en buts ?
q63a86d : Combien de buts ont été marqués dans le temps additionnel de la seconde période ?
qbfc5dc : Combien de buts la France a-t-elle marqués ?
q31e6bf : Quelles équipes ont remporté une séance de tirs au but, et combien chacune ?
q13b18d : Quel pourcentage des tirs de la France étaient cadrés ?

