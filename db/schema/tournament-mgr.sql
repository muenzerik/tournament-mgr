-- Prepended SQL commands --
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";-- ddl-end ---- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.9.2
-- PostgreSQL version: 12.0
-- Project Site: pgmodeler.io
-- Model Author: ---

SET check_function_bodies = false;
-- ddl-end --


-- Database creation must be done outside a multicommand file.
-- These commands were put in this file only as a convenience.
-- -- object: maennerfestspiele | type: DATABASE --
-- -- DROP DATABASE IF EXISTS maennerfestspiele;
-- CREATE DATABASE maennerfestspiele;
-- -- ddl-end --
-- 

-- object: public.users | type: TABLE --
-- DROP TABLE IF EXISTS public.users CASCADE;
CREATE TABLE public.users (
	"ID" uuid NOT NULL DEFAULT uuid_generate_v1(),
	"DateCreated" timestamp with time zone NOT NULL DEFAULT now(),
	"DateChanged" timestamp with time zone NOT NULL DEFAULT now(),
	"UserName" varchar NOT NULL,
	"Surname" varchar,
	"FirstName" varchar,
	"Email" varchar,
	"Phone" varchar,
	CONSTRAINT users_pk PRIMARY KEY ("ID")

);
-- ddl-end --
-- ALTER TABLE public.users OWNER TO postgres;
-- ddl-end --

-- object: public.players | type: TABLE --
-- DROP TABLE IF EXISTS public.players CASCADE;
CREATE TABLE public.players (
	"ID" uuid NOT NULL DEFAULT uuid_generate_v1(),
	"ID_tournament" uuid,
	"ID_users" uuid NOT NULL,
	CONSTRAINT players_pk PRIMARY KEY ("ID")

);
-- ddl-end --
-- ALTER TABLE public.players OWNER TO postgres;
-- ddl-end --

-- object: public.tournament | type: TABLE --
-- DROP TABLE IF EXISTS public.tournament CASCADE;
CREATE TABLE public.tournament (
	"ID" uuid NOT NULL,
	"Season" date NOT NULL,
	"Slogan" varchar,
	CONSTRAINT tournament_pk PRIMARY KEY ("ID")

);
-- ddl-end --
COMMENT ON COLUMN public.tournament."Slogan" IS E'Ein Motto';
-- ddl-end --
-- ALTER TABLE public.tournament OWNER TO postgres;
-- ddl-end --

-- object: users_fk | type: CONSTRAINT --
-- ALTER TABLE public.players DROP CONSTRAINT IF EXISTS users_fk CASCADE;
ALTER TABLE public.players ADD CONSTRAINT users_fk FOREIGN KEY ("ID_users")
REFERENCES public.users ("ID") MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: players_uq | type: CONSTRAINT --
-- ALTER TABLE public.players DROP CONSTRAINT IF EXISTS players_uq CASCADE;
ALTER TABLE public.players ADD CONSTRAINT players_uq UNIQUE ("ID_users");
-- ddl-end --

-- object: public.discipline_t | type: TYPE --
-- DROP TYPE IF EXISTS public.discipline_t CASCADE;
CREATE TYPE public.discipline_t AS
 ENUM ('Single','OneVsOne');
-- ddl-end --
-- ALTER TYPE public.discipline_t OWNER TO postgres;
-- ddl-end --

-- object: public.discipline | type: TABLE --
-- DROP TABLE IF EXISTS public.discipline CASCADE;
CREATE TABLE public.discipline (
	"ID" uuid NOT NULL DEFAULT uuid_generate_v1(),
	"Name" varchar NOT NULL,
	type public.discipline_t NOT NULL,
	"ID_tournament" uuid,
	CONSTRAINT discipline_pk PRIMARY KEY ("ID")

);
-- ddl-end --
-- ALTER TABLE public.discipline OWNER TO postgres;
-- ddl-end --

-- object: tournament_fk | type: CONSTRAINT --
-- ALTER TABLE public.discipline DROP CONSTRAINT IF EXISTS tournament_fk CASCADE;
ALTER TABLE public.discipline ADD CONSTRAINT tournament_fk FOREIGN KEY ("ID_tournament")
REFERENCES public.tournament ("ID") MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: tournament_fk | type: CONSTRAINT --
-- ALTER TABLE public.players DROP CONSTRAINT IF EXISTS tournament_fk CASCADE;
ALTER TABLE public.players ADD CONSTRAINT tournament_fk FOREIGN KEY ("ID_tournament")
REFERENCES public.tournament ("ID") MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: public.result | type: TABLE --
-- DROP TABLE IF EXISTS public.result CASCADE;
CREATE TABLE public.result (
	"ID" uuid NOT NULL DEFAULT uuid_generate_v1(),
	"DateCreated" timestamp with time zone NOT NULL DEFAULT now(),
	"DateChanged" timestamp with time zone NOT NULL DEFAULT now(),
	"ID_discipline" uuid,
	"ID_tournament" uuid,
	"ID_players" uuid,
	CONSTRAINT result_pk PRIMARY KEY ("ID")

);
-- ddl-end --
-- ALTER TABLE public.result OWNER TO postgres;
-- ddl-end --

-- object: public.match_result | type: TABLE --
-- DROP TABLE IF EXISTS public.match_result CASCADE;
CREATE TABLE public.match_result (
	"ID" uuid NOT NULL DEFAULT uuid_generate_v1(),
	"ID_result" uuid,
	"ID_players" uuid,
	CONSTRAINT match_result_pk PRIMARY KEY ("ID")

);
-- ddl-end --
-- ALTER TABLE public.match_result OWNER TO postgres;
-- ddl-end --

-- object: public.match_score | type: TABLE --
-- DROP TABLE IF EXISTS public.match_score CASCADE;
CREATE TABLE public.match_score (
	"ID" uuid NOT NULL DEFAULT uuid_generate_v1(),
	"Score" smallint,
	"ID_result" uuid,
	CONSTRAINT match_score_pk PRIMARY KEY ("ID")

);
-- ddl-end --
-- ALTER TABLE public.match_score OWNER TO postgres;
-- ddl-end --

-- object: discipline_fk | type: CONSTRAINT --
-- ALTER TABLE public.result DROP CONSTRAINT IF EXISTS discipline_fk CASCADE;
ALTER TABLE public.result ADD CONSTRAINT discipline_fk FOREIGN KEY ("ID_discipline")
REFERENCES public.discipline ("ID") MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: result_uq | type: CONSTRAINT --
-- ALTER TABLE public.result DROP CONSTRAINT IF EXISTS result_uq CASCADE;
ALTER TABLE public.result ADD CONSTRAINT result_uq UNIQUE ("ID_discipline");
-- ddl-end --

-- object: tournament_fk | type: CONSTRAINT --
-- ALTER TABLE public.result DROP CONSTRAINT IF EXISTS tournament_fk CASCADE;
ALTER TABLE public.result ADD CONSTRAINT tournament_fk FOREIGN KEY ("ID_tournament")
REFERENCES public.tournament ("ID") MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: result_uq1 | type: CONSTRAINT --
-- ALTER TABLE public.result DROP CONSTRAINT IF EXISTS result_uq1 CASCADE;
ALTER TABLE public.result ADD CONSTRAINT result_uq1 UNIQUE ("ID_tournament");
-- ddl-end --

-- object: result_fk | type: CONSTRAINT --
-- ALTER TABLE public.match_result DROP CONSTRAINT IF EXISTS result_fk CASCADE;
ALTER TABLE public.match_result ADD CONSTRAINT result_fk FOREIGN KEY ("ID_result")
REFERENCES public.result ("ID") MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: match_result_uq | type: CONSTRAINT --
-- ALTER TABLE public.match_result DROP CONSTRAINT IF EXISTS match_result_uq CASCADE;
ALTER TABLE public.match_result ADD CONSTRAINT match_result_uq UNIQUE ("ID_result");
-- ddl-end --

-- object: players_fk | type: CONSTRAINT --
-- ALTER TABLE public.match_result DROP CONSTRAINT IF EXISTS players_fk CASCADE;
ALTER TABLE public.match_result ADD CONSTRAINT players_fk FOREIGN KEY ("ID_players")
REFERENCES public.players ("ID") MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: match_result_uq1 | type: CONSTRAINT --
-- ALTER TABLE public.match_result DROP CONSTRAINT IF EXISTS match_result_uq1 CASCADE;
ALTER TABLE public.match_result ADD CONSTRAINT match_result_uq1 UNIQUE ("ID_players");
-- ddl-end --

-- object: players_fk | type: CONSTRAINT --
-- ALTER TABLE public.result DROP CONSTRAINT IF EXISTS players_fk CASCADE;
ALTER TABLE public.result ADD CONSTRAINT players_fk FOREIGN KEY ("ID_players")
REFERENCES public.players ("ID") MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: result_uq2 | type: CONSTRAINT --
-- ALTER TABLE public.result DROP CONSTRAINT IF EXISTS result_uq2 CASCADE;
ALTER TABLE public.result ADD CONSTRAINT result_uq2 UNIQUE ("ID_players");
-- ddl-end --

-- object: result_fk | type: CONSTRAINT --
-- ALTER TABLE public.match_score DROP CONSTRAINT IF EXISTS result_fk CASCADE;
ALTER TABLE public.match_score ADD CONSTRAINT result_fk FOREIGN KEY ("ID_result")
REFERENCES public.result ("ID") MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: match_score_uq | type: CONSTRAINT --
-- ALTER TABLE public.match_score DROP CONSTRAINT IF EXISTS match_score_uq CASCADE;
ALTER TABLE public.match_score ADD CONSTRAINT match_score_uq UNIQUE ("ID_result");
-- ddl-end --

-- object: public.sync_lastmod | type: FUNCTION --
-- DROP FUNCTION IF EXISTS public.sync_lastmod() CASCADE;
CREATE FUNCTION public.sync_lastmod ()
	RETURNS trigger
	LANGUAGE plpgsql
	VOLATILE 
	CALLED ON NULL INPUT
	SECURITY INVOKER
	COST 1
	AS $$
BEGIN
 NEW."DateChanged" := NOW();

  RETURN NEW;
END;
$$;
-- ddl-end --
-- ALTER FUNCTION public.sync_lastmod() OWNER TO postgres;
-- ddl-end --

-- object: sync_lastmod | type: TRIGGER --
-- DROP TRIGGER IF EXISTS sync_lastmod ON public.users CASCADE;
CREATE TRIGGER sync_lastmod
	BEFORE UPDATE OF "DateChanged"
	ON public.users
	FOR EACH ROW
	EXECUTE PROCEDURE public.sync_lastmod();
-- ddl-end --

-- object: sync_lastmod | type: TRIGGER --
-- DROP TRIGGER IF EXISTS sync_lastmod ON public.result CASCADE;
CREATE TRIGGER sync_lastmod
	BEFORE UPDATE
	ON public.result
	FOR EACH ROW
	EXECUTE PROCEDURE public.sync_lastmod();
-- ddl-end --


