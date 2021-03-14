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

-- object: public."Users" | type: TABLE --
-- DROP TABLE IF EXISTS public."Users" CASCADE;
CREATE TABLE public."Users" (
	"ID" uuid NOT NULL DEFAULT uuid_generate_v1(),
	"DateCreated" timestamp with time zone NOT NULL DEFAULT now(),
	"DateChanged" timestamp with time zone NOT NULL DEFAULT now(),
	"UserName" varchar NOT NULL,
	"Surname" varchar,
	"FirstName" varchar,
	"Email" varchar,
	"Phone" varchar,
	CONSTRAINT "Users_pk" PRIMARY KEY ("ID")

);
-- ddl-end --
-- ALTER TABLE public."Users" OWNER TO postgres;
-- ddl-end --

INSERT INTO public."Users" ("ID", "DateCreated", "DateChanged", "UserName", "Surname", "FirstName", "Email", "Phone") VALUES (DEFAULT, E'2021/03/04', E'2021/03/04', E'mr_moto', E'Münz', E'Erik', E'muenzerik@gmail.com', DEFAULT);
-- ddl-end --

-- object: public."Players" | type: TABLE --
-- DROP TABLE IF EXISTS public."Players" CASCADE;
CREATE TABLE public."Players" (
	"ID" uuid NOT NULL DEFAULT uuid_generate_v1(),
	"ID_Users" uuid NOT NULL,
	"ID_Tournament" uuid,
	CONSTRAINT "Players_pk" PRIMARY KEY ("ID")

);
-- ddl-end --
-- ALTER TABLE public."Players" OWNER TO postgres;
-- ddl-end --

-- object: public."Tournament" | type: TABLE --
-- DROP TABLE IF EXISTS public."Tournament" CASCADE;
CREATE TABLE public."Tournament" (
	"ID" uuid NOT NULL,
	"Season" date NOT NULL,
	"Slogan" varchar,
	CONSTRAINT "Tournament_pk" PRIMARY KEY ("ID")

);
-- ddl-end --
COMMENT ON COLUMN public."Tournament"."Slogan" IS E'Ein Motto';
-- ddl-end --
-- ALTER TABLE public."Tournament" OWNER TO postgres;
-- ddl-end --

-- object: "Users_fk" | type: CONSTRAINT --
-- ALTER TABLE public."Players" DROP CONSTRAINT IF EXISTS "Users_fk" CASCADE;
ALTER TABLE public."Players" ADD CONSTRAINT "Users_fk" FOREIGN KEY ("ID_Users")
REFERENCES public."Users" ("ID") MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: "Players_uq" | type: CONSTRAINT --
-- ALTER TABLE public."Players" DROP CONSTRAINT IF EXISTS "Players_uq" CASCADE;
ALTER TABLE public."Players" ADD CONSTRAINT "Players_uq" UNIQUE ("ID_Users");
-- ddl-end --

-- object: "uuid-ossp" | type: EXTENSION --
-- DROP EXTENSION IF EXISTS "uuid-ossp" CASCADE;
CREATE EXTENSION "uuid-ossp"
WITH SCHEMA public;
-- ddl-end --

-- object: public.discipline_t | type: TYPE --
-- DROP TYPE IF EXISTS public.discipline_t CASCADE;
CREATE TYPE public.discipline_t AS
 ENUM ('Single','OneVsOne');
-- ddl-end --
-- ALTER TYPE public.discipline_t OWNER TO postgres;
-- ddl-end --

-- object: public."Discipline" | type: TABLE --
-- DROP TABLE IF EXISTS public."Discipline" CASCADE;
CREATE TABLE public."Discipline" (
	"ID" uuid NOT NULL DEFAULT uuid_generate_v1(),
	"Name" varchar NOT NULL,
	type public.discipline_t NOT NULL,
	"ID_Tournament" uuid,
	CONSTRAINT "Discipline_pk" PRIMARY KEY ("ID")

);
-- ddl-end --
-- ALTER TABLE public."Discipline" OWNER TO postgres;
-- ddl-end --

-- object: "Tournament_fk" | type: CONSTRAINT --
-- ALTER TABLE public."Discipline" DROP CONSTRAINT IF EXISTS "Tournament_fk" CASCADE;
ALTER TABLE public."Discipline" ADD CONSTRAINT "Tournament_fk" FOREIGN KEY ("ID_Tournament")
REFERENCES public."Tournament" ("ID") MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: "Tournament_fk" | type: CONSTRAINT --
-- ALTER TABLE public."Players" DROP CONSTRAINT IF EXISTS "Tournament_fk" CASCADE;
ALTER TABLE public."Players" ADD CONSTRAINT "Tournament_fk" FOREIGN KEY ("ID_Tournament")
REFERENCES public."Tournament" ("ID") MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: public."Result" | type: TABLE --
-- DROP TABLE IF EXISTS public."Result" CASCADE;
CREATE TABLE public."Result" (
	"ID" uuid NOT NULL DEFAULT uuid_generate_v1(),
	"DateCreated" timestamp with time zone NOT NULL DEFAULT now(),
	"DateChanged" timestamp with time zone NOT NULL DEFAULT now(),
	"ID_Discipline" uuid,
	"ID_Tournament" uuid,
	"ID_Players" uuid,
	CONSTRAINT "Score_pk" PRIMARY KEY ("ID")

);
-- ddl-end --
-- ALTER TABLE public."Result" OWNER TO postgres;
-- ddl-end --

-- object: public."MatchResult" | type: TABLE --
-- DROP TABLE IF EXISTS public."MatchResult" CASCADE;
CREATE TABLE public."MatchResult" (
	"ID" uuid NOT NULL DEFAULT uuid_generate_v1(),
	"ID_Result" uuid,
	"ID_Players" uuid,
	CONSTRAINT "MatchResult_pk" PRIMARY KEY ("ID")

);
-- ddl-end --
-- ALTER TABLE public."MatchResult" OWNER TO postgres;
-- ddl-end --

-- object: public."MatchScore" | type: TABLE --
-- DROP TABLE IF EXISTS public."MatchScore" CASCADE;
CREATE TABLE public."MatchScore" (
	"ID" uuid NOT NULL DEFAULT uuid_generate_v1(),
	"ID_Result" uuid,
	"Score" smallint,
	CONSTRAINT "MatchScore_pk" PRIMARY KEY ("ID")

);
-- ddl-end --
-- ALTER TABLE public."MatchScore" OWNER TO postgres;
-- ddl-end --

-- object: "Discipline_fk" | type: CONSTRAINT --
-- ALTER TABLE public."Result" DROP CONSTRAINT IF EXISTS "Discipline_fk" CASCADE;
ALTER TABLE public."Result" ADD CONSTRAINT "Discipline_fk" FOREIGN KEY ("ID_Discipline")
REFERENCES public."Discipline" ("ID") MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: "Result_uq" | type: CONSTRAINT --
-- ALTER TABLE public."Result" DROP CONSTRAINT IF EXISTS "Result_uq" CASCADE;
ALTER TABLE public."Result" ADD CONSTRAINT "Result_uq" UNIQUE ("ID_Discipline");
-- ddl-end --

-- object: "Tournament_fk" | type: CONSTRAINT --
-- ALTER TABLE public."Result" DROP CONSTRAINT IF EXISTS "Tournament_fk" CASCADE;
ALTER TABLE public."Result" ADD CONSTRAINT "Tournament_fk" FOREIGN KEY ("ID_Tournament")
REFERENCES public."Tournament" ("ID") MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: "Result_uq1" | type: CONSTRAINT --
-- ALTER TABLE public."Result" DROP CONSTRAINT IF EXISTS "Result_uq1" CASCADE;
ALTER TABLE public."Result" ADD CONSTRAINT "Result_uq1" UNIQUE ("ID_Tournament");
-- ddl-end --

-- object: "Result_fk" | type: CONSTRAINT --
-- ALTER TABLE public."MatchResult" DROP CONSTRAINT IF EXISTS "Result_fk" CASCADE;
ALTER TABLE public."MatchResult" ADD CONSTRAINT "Result_fk" FOREIGN KEY ("ID_Result")
REFERENCES public."Result" ("ID") MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: "MatchResult_uq" | type: CONSTRAINT --
-- ALTER TABLE public."MatchResult" DROP CONSTRAINT IF EXISTS "MatchResult_uq" CASCADE;
ALTER TABLE public."MatchResult" ADD CONSTRAINT "MatchResult_uq" UNIQUE ("ID_Result");
-- ddl-end --

-- object: "Players_fk" | type: CONSTRAINT --
-- ALTER TABLE public."MatchResult" DROP CONSTRAINT IF EXISTS "Players_fk" CASCADE;
ALTER TABLE public."MatchResult" ADD CONSTRAINT "Players_fk" FOREIGN KEY ("ID_Players")
REFERENCES public."Players" ("ID") MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: "MatchResult_uq1" | type: CONSTRAINT --
-- ALTER TABLE public."MatchResult" DROP CONSTRAINT IF EXISTS "MatchResult_uq1" CASCADE;
ALTER TABLE public."MatchResult" ADD CONSTRAINT "MatchResult_uq1" UNIQUE ("ID_Players");
-- ddl-end --

-- object: "Players_fk" | type: CONSTRAINT --
-- ALTER TABLE public."Result" DROP CONSTRAINT IF EXISTS "Players_fk" CASCADE;
ALTER TABLE public."Result" ADD CONSTRAINT "Players_fk" FOREIGN KEY ("ID_Players")
REFERENCES public."Players" ("ID") MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: "Result_uq2" | type: CONSTRAINT --
-- ALTER TABLE public."Result" DROP CONSTRAINT IF EXISTS "Result_uq2" CASCADE;
ALTER TABLE public."Result" ADD CONSTRAINT "Result_uq2" UNIQUE ("ID_Players");
-- ddl-end --

-- object: "Result_fk" | type: CONSTRAINT --
-- ALTER TABLE public."MatchScore" DROP CONSTRAINT IF EXISTS "Result_fk" CASCADE;
ALTER TABLE public."MatchScore" ADD CONSTRAINT "Result_fk" FOREIGN KEY ("ID_Result")
REFERENCES public."Result" ("ID") MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: "MatchScore_uq" | type: CONSTRAINT --
-- ALTER TABLE public."MatchScore" DROP CONSTRAINT IF EXISTS "MatchScore_uq" CASCADE;
ALTER TABLE public."MatchScore" ADD CONSTRAINT "MatchScore_uq" UNIQUE ("ID_Result");
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
-- DROP TRIGGER IF EXISTS sync_lastmod ON public."Users" CASCADE;
CREATE TRIGGER sync_lastmod
	BEFORE UPDATE OF "DateChanged"
	ON public."Users"
	FOR EACH ROW
	EXECUTE PROCEDURE public.sync_lastmod();
-- ddl-end --

-- object: sync_lastmod | type: TRIGGER --
-- DROP TRIGGER IF EXISTS sync_lastmod ON public."Result" CASCADE;
CREATE TRIGGER sync_lastmod
	BEFORE UPDATE
	ON public."Result"
	FOR EACH ROW
	EXECUTE PROCEDURE public.sync_lastmod();
-- ddl-end --


