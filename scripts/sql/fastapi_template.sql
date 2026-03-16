--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2 (Debian 16.2-1.pgdg120+2)
-- Dumped by pg_dump version 16.2 (Debian 16.2-1.pgdg120+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Rbac_Permission; Type: TABLE; Schema: public; Owner: jack
--

CREATE TABLE public."Rbac_Permission" (
    id integer NOT NULL,
    code character varying(256) NOT NULL
);


ALTER TABLE public."Rbac_Permission" OWNER TO jack;

--
-- Name: Rbac_Permission_id_seq; Type: SEQUENCE; Schema: public; Owner: jack
--

CREATE SEQUENCE public."Rbac_Permission_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Rbac_Permission_id_seq" OWNER TO jack;

--
-- Name: Rbac_Permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jack
--

ALTER SEQUENCE public."Rbac_Permission_id_seq" OWNED BY public."Rbac_Permission".id;


--
-- Name: Rbac_Role; Type: TABLE; Schema: public; Owner: jack
--

CREATE TABLE public."Rbac_Role" (
    id integer NOT NULL,
    name character varying(16) NOT NULL
);


ALTER TABLE public."Rbac_Role" OWNER TO jack;

--
-- Name: Rbac_Role2Permission; Type: TABLE; Schema: public; Owner: jack
--

CREATE TABLE public."Rbac_Role2Permission" (
    id integer NOT NULL,
    role_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public."Rbac_Role2Permission" OWNER TO jack;

--
-- Name: Rbac_Role2Permission_id_seq; Type: SEQUENCE; Schema: public; Owner: jack
--

CREATE SEQUENCE public."Rbac_Role2Permission_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Rbac_Role2Permission_id_seq" OWNER TO jack;

--
-- Name: Rbac_Role2Permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jack
--

ALTER SEQUENCE public."Rbac_Role2Permission_id_seq" OWNED BY public."Rbac_Role2Permission".id;


--
-- Name: Rbac_Role_id_seq; Type: SEQUENCE; Schema: public; Owner: jack
--

CREATE SEQUENCE public."Rbac_Role_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Rbac_Role_id_seq" OWNER TO jack;

--
-- Name: Rbac_Role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jack
--

ALTER SEQUENCE public."Rbac_Role_id_seq" OWNED BY public."Rbac_Role".id;


--
-- Name: Rbac_User; Type: TABLE; Schema: public; Owner: jack
--

CREATE TABLE public."Rbac_User" (
    id integer NOT NULL,
    name character varying(16) NOT NULL,
    created_time timestamp without time zone DEFAULT now() NOT NULL,
    is_deleted boolean NOT NULL,
    email character varying(32) NOT NULL,
    password character varying(256) NOT NULL
);


ALTER TABLE public."Rbac_User" OWNER TO jack;

--
-- Name: Rbac_User2Role; Type: TABLE; Schema: public; Owner: jack
--

CREATE TABLE public."Rbac_User2Role" (
    id integer NOT NULL,
    user_id integer NOT NULL,
    role_id integer NOT NULL
);


ALTER TABLE public."Rbac_User2Role" OWNER TO jack;

--
-- Name: Rbac_User2Role_id_seq; Type: SEQUENCE; Schema: public; Owner: jack
--

CREATE SEQUENCE public."Rbac_User2Role_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Rbac_User2Role_id_seq" OWNER TO jack;

--
-- Name: Rbac_User2Role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jack
--

ALTER SEQUENCE public."Rbac_User2Role_id_seq" OWNED BY public."Rbac_User2Role".id;


--
-- Name: Rbac_User_id_seq; Type: SEQUENCE; Schema: public; Owner: jack
--

CREATE SEQUENCE public."Rbac_User_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Rbac_User_id_seq" OWNER TO jack;

--
-- Name: Rbac_User_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jack
--

ALTER SEQUENCE public."Rbac_User_id_seq" OWNED BY public."Rbac_User".id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: jack
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO jack;

--
-- Name: Rbac_Permission id; Type: DEFAULT; Schema: public; Owner: jack
--

ALTER TABLE ONLY public."Rbac_Permission" ALTER COLUMN id SET DEFAULT nextval('public."Rbac_Permission_id_seq"'::regclass);


--
-- Name: Rbac_Role id; Type: DEFAULT; Schema: public; Owner: jack
--

ALTER TABLE ONLY public."Rbac_Role" ALTER COLUMN id SET DEFAULT nextval('public."Rbac_Role_id_seq"'::regclass);


--
-- Name: Rbac_Role2Permission id; Type: DEFAULT; Schema: public; Owner: jack
--

ALTER TABLE ONLY public."Rbac_Role2Permission" ALTER COLUMN id SET DEFAULT nextval('public."Rbac_Role2Permission_id_seq"'::regclass);


--
-- Name: Rbac_User id; Type: DEFAULT; Schema: public; Owner: jack
--

ALTER TABLE ONLY public."Rbac_User" ALTER COLUMN id SET DEFAULT nextval('public."Rbac_User_id_seq"'::regclass);


--
-- Name: Rbac_User2Role id; Type: DEFAULT; Schema: public; Owner: jack
--

ALTER TABLE ONLY public."Rbac_User2Role" ALTER COLUMN id SET DEFAULT nextval('public."Rbac_User2Role_id_seq"'::regclass);


--
-- Data for Name: Rbac_Permission; Type: TABLE DATA; Schema: public; Owner: jack
--

COPY public."Rbac_Permission" (id, code) FROM stdin;
\.


--
-- Data for Name: Rbac_Role; Type: TABLE DATA; Schema: public; Owner: jack
--

COPY public."Rbac_Role" (id, name) FROM stdin;
\.


--
-- Data for Name: Rbac_Role2Permission; Type: TABLE DATA; Schema: public; Owner: jack
--

COPY public."Rbac_Role2Permission" (id, role_id, permission_id) FROM stdin;
\.


--
-- Data for Name: Rbac_User; Type: TABLE DATA; Schema: public; Owner: jack
--

COPY public."Rbac_User" (id, name, created_time, is_deleted, email, password) FROM stdin;
1	jack	2026-03-16 22:43:26	f	jack@qq.com	$2b$12$32pzqcJe5CFpoxHVjgu5bO2vFX68pJwkOq.XPC.76rxlsFVcOzTUW
\.


--
-- Data for Name: Rbac_User2Role; Type: TABLE DATA; Schema: public; Owner: jack
--

COPY public."Rbac_User2Role" (id, user_id, role_id) FROM stdin;
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: jack
--

COPY public.alembic_version (version_num) FROM stdin;
6c2450dc53a0
\.


--
-- Name: Rbac_Permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jack
--

SELECT pg_catalog.setval('public."Rbac_Permission_id_seq"', 1, false);


--
-- Name: Rbac_Role2Permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jack
--

SELECT pg_catalog.setval('public."Rbac_Role2Permission_id_seq"', 1, false);


--
-- Name: Rbac_Role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jack
--

SELECT pg_catalog.setval('public."Rbac_Role_id_seq"', 1, false);


--
-- Name: Rbac_User2Role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jack
--

SELECT pg_catalog.setval('public."Rbac_User2Role_id_seq"', 1, false);


--
-- Name: Rbac_User_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jack
--

SELECT pg_catalog.setval('public."Rbac_User_id_seq"', 1, false);


--
-- Name: Rbac_Permission Rbac_Permission_pkey; Type: CONSTRAINT; Schema: public; Owner: jack
--

ALTER TABLE ONLY public."Rbac_Permission"
    ADD CONSTRAINT "Rbac_Permission_pkey" PRIMARY KEY (id);


--
-- Name: Rbac_Role2Permission Rbac_Role2Permission_pkey; Type: CONSTRAINT; Schema: public; Owner: jack
--

ALTER TABLE ONLY public."Rbac_Role2Permission"
    ADD CONSTRAINT "Rbac_Role2Permission_pkey" PRIMARY KEY (id);


--
-- Name: Rbac_Role Rbac_Role_pkey; Type: CONSTRAINT; Schema: public; Owner: jack
--

ALTER TABLE ONLY public."Rbac_Role"
    ADD CONSTRAINT "Rbac_Role_pkey" PRIMARY KEY (id);


--
-- Name: Rbac_User2Role Rbac_User2Role_pkey; Type: CONSTRAINT; Schema: public; Owner: jack
--

ALTER TABLE ONLY public."Rbac_User2Role"
    ADD CONSTRAINT "Rbac_User2Role_pkey" PRIMARY KEY (id);


--
-- Name: Rbac_User Rbac_User_pkey; Type: CONSTRAINT; Schema: public; Owner: jack
--

ALTER TABLE ONLY public."Rbac_User"
    ADD CONSTRAINT "Rbac_User_pkey" PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: jack
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: Rbac_Role2Permission unique_role_permission; Type: CONSTRAINT; Schema: public; Owner: jack
--

ALTER TABLE ONLY public."Rbac_Role2Permission"
    ADD CONSTRAINT unique_role_permission UNIQUE (role_id, permission_id);


--
-- Name: Rbac_User2Role unique_user_role; Type: CONSTRAINT; Schema: public; Owner: jack
--

ALTER TABLE ONLY public."Rbac_User2Role"
    ADD CONSTRAINT unique_user_role UNIQUE (user_id, role_id);


--
-- Name: ix_Rbac_Role2Permission_permission_id; Type: INDEX; Schema: public; Owner: jack
--

CREATE INDEX "ix_Rbac_Role2Permission_permission_id" ON public."Rbac_Role2Permission" USING btree (permission_id);


--
-- Name: ix_Rbac_Role2Permission_role_id; Type: INDEX; Schema: public; Owner: jack
--

CREATE INDEX "ix_Rbac_Role2Permission_role_id" ON public."Rbac_Role2Permission" USING btree (role_id);


--
-- Name: ix_Rbac_User2Role_role_id; Type: INDEX; Schema: public; Owner: jack
--

CREATE INDEX "ix_Rbac_User2Role_role_id" ON public."Rbac_User2Role" USING btree (role_id);


--
-- Name: ix_Rbac_User2Role_user_id; Type: INDEX; Schema: public; Owner: jack
--

CREATE INDEX "ix_Rbac_User2Role_user_id" ON public."Rbac_User2Role" USING btree (user_id);


--
-- PostgreSQL database dump complete
--

