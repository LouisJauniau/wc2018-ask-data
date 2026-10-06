-- Role de connexion de l'agent : lecture seule sur le schema sb.
--
-- A executer en superutilisateur, sur la base wc2018 :
--   psql -d wc2018 -f sql/role_lecteur.sql
-- puis donner un mot de passe au role si le serveur en exige un :
--   ALTER ROLE wc_lecteur PASSWORD '...';
--
-- La chaine d'ingestion recree le schema sb a chaque passage (DROP SCHEMA
-- CASCADE), ce qui efface les droits accordes ici. Relancer ce script apres
-- chaque ingestion.

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'wc_lecteur') THEN
        CREATE ROLE wc_lecteur LOGIN;
    END IF;
END
$$;

GRANT CONNECT ON DATABASE wc2018 TO wc_lecteur;
GRANT USAGE ON SCHEMA sb TO wc_lecteur;
GRANT SELECT ON ALL TABLES IN SCHEMA sb TO wc_lecteur;

-- Defense en profondeur : meme si un droit d'ecriture etait accorde par
-- erreur plus tard, les transactions de ce role restent en lecture seule.
ALTER ROLE wc_lecteur SET default_transaction_read_only = on;
ALTER ROLE wc_lecteur SET statement_timeout = '10s';
