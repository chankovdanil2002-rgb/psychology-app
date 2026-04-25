--
-- PostgreSQL database dump
--

\restrict Xb8upjJT9ds9ApKlwaDh3QcjsxthaE59ZDi8XTAL0PZZy13C1gpyPXFP5NiezT3

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.users_user_permissions DROP CONSTRAINT IF EXISTS users_user_permissions_user_id_92473840_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.users_user_permissions DROP CONSTRAINT IF EXISTS users_user_permissio_permission_id_6d08dcd2_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.users_groups DROP CONSTRAINT IF EXISTS users_groups_user_id_f500bee5_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.users_groups DROP CONSTRAINT IF EXISTS users_groups_group_id_2f3517aa_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.time_slots DROP CONSTRAINT IF EXISTS time_slots_psychologist_id_93c87fbe_fk_psychologist_profiles_id;
ALTER TABLE IF EXISTS ONLY public.reviews DROP CONSTRAINT IF EXISTS reviews_appointment_id_9141b057_fk_appointments_id;
ALTER TABLE IF EXISTS ONLY public.psychologist_specializations DROP CONSTRAINT IF EXISTS psychologist_special_specialization_id_cb576c77_fk_specializ;
ALTER TABLE IF EXISTS ONLY public.psychologist_specializations DROP CONSTRAINT IF EXISTS psychologist_special_psychologist_id_4d69ac51_fk_psycholog;
ALTER TABLE IF EXISTS ONLY public.psychologist_profiles DROP CONSTRAINT IF EXISTS psychologist_profiles_user_id_2abb595a_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.notifications DROP CONSTRAINT IF EXISTS notifications_user_id_468e288d_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.email_confirmation_tokens DROP CONSTRAINT IF EXISTS email_confirmation_tokens_user_id_4f543bec_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.client_profiles DROP CONSTRAINT IF EXISTS client_profiles_user_id_2c51f42e_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.appointments DROP CONSTRAINT IF EXISTS appointments_time_slot_id_95fedf04_fk_time_slots_id;
ALTER TABLE IF EXISTS ONLY public.appointments DROP CONSTRAINT IF EXISTS appointments_psychologist_id_9e301a3d_fk_psycholog;
ALTER TABLE IF EXISTS ONLY public.appointments DROP CONSTRAINT IF EXISTS appointments_client_id_ed088e20_fk_client_profiles_id;
DROP INDEX IF EXISTS public.users_user_permissions_user_id_92473840;
DROP INDEX IF EXISTS public.users_user_permissions_permission_id_6d08dcd2;
DROP INDEX IF EXISTS public.users_groups_user_id_f500bee5;
DROP INDEX IF EXISTS public.users_groups_group_id_2f3517aa;
DROP INDEX IF EXISTS public.users_email_0ea73cca_like;
DROP INDEX IF EXISTS public.unique_active_appointment_per_time_slot;
DROP INDEX IF EXISTS public.time_slots_psychologist_id_93c87fbe;
DROP INDEX IF EXISTS public.time_slots_date_d554e2f9;
DROP INDEX IF EXISTS public.specializations_slug_7284e6fc_like;
DROP INDEX IF EXISTS public.specializations_name_a9fe49f3_like;
DROP INDEX IF EXISTS public.psychologist_specializations_specialization_id_cb576c77;
DROP INDEX IF EXISTS public.psychologist_specializations_psychologist_id_4d69ac51;
DROP INDEX IF EXISTS public.notifications_user_id_468e288d;
DROP INDEX IF EXISTS public.email_confirmation_tokens_user_id_4f543bec;
DROP INDEX IF EXISTS public.email_confirmation_tokens_code_3d08c5d2_like;
DROP INDEX IF EXISTS public.email_confirmation_tokens_code_3d08c5d2;
DROP INDEX IF EXISTS public.django_session_session_key_c0390e0f_like;
DROP INDEX IF EXISTS public.django_session_expire_date_a5c62663;
DROP INDEX IF EXISTS public.django_admin_log_user_id_c564eba6;
DROP INDEX IF EXISTS public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX IF EXISTS public.auth_permission_content_type_id_2f476e4b;
DROP INDEX IF EXISTS public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX IF EXISTS public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX IF EXISTS public.auth_group_name_a6ea08ec_like;
DROP INDEX IF EXISTS public.appointments_time_slot_id_95fedf04;
DROP INDEX IF EXISTS public.appointments_status_ff89895a_like;
DROP INDEX IF EXISTS public.appointments_status_ff89895a;
DROP INDEX IF EXISTS public.appointments_psychologist_id_9e301a3d;
DROP INDEX IF EXISTS public.appointments_client_id_ed088e20;
ALTER TABLE IF EXISTS ONLY public.users_user_permissions DROP CONSTRAINT IF EXISTS users_user_permissions_user_id_permission_id_3b86cbdf_uniq;
ALTER TABLE IF EXISTS ONLY public.users_user_permissions DROP CONSTRAINT IF EXISTS users_user_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_pkey;
ALTER TABLE IF EXISTS ONLY public.users_groups DROP CONSTRAINT IF EXISTS users_groups_user_id_group_id_fc7788e8_uniq;
ALTER TABLE IF EXISTS ONLY public.users_groups DROP CONSTRAINT IF EXISTS users_groups_pkey;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_email_key;
ALTER TABLE IF EXISTS ONLY public.time_slots DROP CONSTRAINT IF EXISTS time_slots_psychologist_id_date_start_time_b072a47a_uniq;
ALTER TABLE IF EXISTS ONLY public.time_slots DROP CONSTRAINT IF EXISTS time_slots_pkey;
ALTER TABLE IF EXISTS ONLY public.specializations DROP CONSTRAINT IF EXISTS specializations_slug_key;
ALTER TABLE IF EXISTS ONLY public.specializations DROP CONSTRAINT IF EXISTS specializations_pkey;
ALTER TABLE IF EXISTS ONLY public.specializations DROP CONSTRAINT IF EXISTS specializations_name_key;
ALTER TABLE IF EXISTS ONLY public.reviews DROP CONSTRAINT IF EXISTS reviews_pkey;
ALTER TABLE IF EXISTS ONLY public.reviews DROP CONSTRAINT IF EXISTS reviews_appointment_id_key;
ALTER TABLE IF EXISTS ONLY public.psychologist_specializations DROP CONSTRAINT IF EXISTS psychologist_specializations_pkey;
ALTER TABLE IF EXISTS ONLY public.psychologist_specializations DROP CONSTRAINT IF EXISTS psychologist_specializat_psychologist_id_speciali_541db4d2_uniq;
ALTER TABLE IF EXISTS ONLY public.psychologist_profiles DROP CONSTRAINT IF EXISTS psychologist_profiles_user_id_key;
ALTER TABLE IF EXISTS ONLY public.psychologist_profiles DROP CONSTRAINT IF EXISTS psychologist_profiles_pkey;
ALTER TABLE IF EXISTS ONLY public.notifications DROP CONSTRAINT IF EXISTS notifications_pkey;
ALTER TABLE IF EXISTS ONLY public.email_confirmation_tokens DROP CONSTRAINT IF EXISTS email_confirmation_tokens_token_key;
ALTER TABLE IF EXISTS ONLY public.email_confirmation_tokens DROP CONSTRAINT IF EXISTS email_confirmation_tokens_pkey;
ALTER TABLE IF EXISTS ONLY public.django_session DROP CONSTRAINT IF EXISTS django_session_pkey;
ALTER TABLE IF EXISTS ONLY public.django_migrations DROP CONSTRAINT IF EXISTS django_migrations_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_pkey;
ALTER TABLE IF EXISTS ONLY public.client_profiles DROP CONSTRAINT IF EXISTS client_profiles_user_id_key;
ALTER TABLE IF EXISTS ONLY public.client_profiles DROP CONSTRAINT IF EXISTS client_profiles_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_name_key;
ALTER TABLE IF EXISTS ONLY public.appointments DROP CONSTRAINT IF EXISTS appointments_pkey;
DROP TABLE IF EXISTS public.users_user_permissions;
DROP TABLE IF EXISTS public.users_groups;
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.time_slots;
DROP TABLE IF EXISTS public.specializations;
DROP TABLE IF EXISTS public.reviews;
DROP TABLE IF EXISTS public.psychologist_specializations;
DROP TABLE IF EXISTS public.psychologist_profiles;
DROP TABLE IF EXISTS public.notifications;
DROP TABLE IF EXISTS public.email_confirmation_tokens;
DROP TABLE IF EXISTS public.django_session;
DROP TABLE IF EXISTS public.django_migrations;
DROP TABLE IF EXISTS public.django_content_type;
DROP TABLE IF EXISTS public.django_admin_log;
DROP TABLE IF EXISTS public.client_profiles;
DROP TABLE IF EXISTS public.auth_permission;
DROP TABLE IF EXISTS public.auth_group_permissions;
DROP TABLE IF EXISTS public.auth_group;
DROP TABLE IF EXISTS public.appointments;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: appointments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.appointments (
    id bigint NOT NULL,
    status character varying(15) NOT NULL,
    comment text,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    client_id bigint NOT NULL,
    psychologist_id bigint NOT NULL,
    time_slot_id bigint NOT NULL
);


--
-- Name: appointments_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.appointments ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.appointments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: client_profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.client_profiles (
    id bigint NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    phone character varying(20),
    date_of_birth date,
    avatar text NOT NULL,
    is_profile_complete boolean NOT NULL,
    user_id bigint NOT NULL
);


--
-- Name: client_profiles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.client_profiles ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.client_profiles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- Name: email_confirmation_tokens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.email_confirmation_tokens (
    id bigint NOT NULL,
    token uuid NOT NULL,
    is_used boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    user_id bigint NOT NULL,
    code character varying(6) NOT NULL
);


--
-- Name: email_confirmation_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.email_confirmation_tokens ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.email_confirmation_tokens_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: notifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notifications (
    id bigint NOT NULL,
    type character varying(30) NOT NULL,
    title character varying(255) NOT NULL,
    message text NOT NULL,
    is_read boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    user_id bigint NOT NULL
);


--
-- Name: notifications_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.notifications ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.notifications_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: psychologist_profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.psychologist_profiles (
    id bigint NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    patronymic character varying(100),
    phone character varying(20),
    photo text NOT NULL,
    experience_years integer,
    education text,
    bio text,
    price numeric(10,2),
    diploma_scan character varying(100) NOT NULL,
    is_verified boolean NOT NULL,
    verified_at timestamp with time zone,
    is_profile_complete boolean NOT NULL,
    user_id bigint NOT NULL
);


--
-- Name: psychologist_profiles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.psychologist_profiles ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.psychologist_profiles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: psychologist_specializations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.psychologist_specializations (
    id bigint NOT NULL,
    is_primary boolean NOT NULL,
    psychologist_id bigint NOT NULL,
    specialization_id bigint NOT NULL
);


--
-- Name: psychologist_specializations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.psychologist_specializations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.psychologist_specializations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: reviews; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.reviews (
    id bigint NOT NULL,
    rating integer NOT NULL,
    text text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    appointment_id bigint NOT NULL
);


--
-- Name: reviews_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.reviews ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.reviews_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: specializations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.specializations (
    id bigint NOT NULL,
    name character varying(200) NOT NULL,
    slug character varying(200) NOT NULL,
    description text NOT NULL,
    icon character varying(100)
);


--
-- Name: specializations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.specializations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.specializations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: time_slots; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.time_slots (
    id bigint NOT NULL,
    date date NOT NULL,
    start_time time without time zone NOT NULL,
    end_time time without time zone NOT NULL,
    is_available boolean NOT NULL,
    psychologist_id bigint NOT NULL
);


--
-- Name: time_slots_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.time_slots ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.time_slots_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    email character varying(254) NOT NULL,
    role character varying(15) NOT NULL,
    is_active boolean NOT NULL,
    is_staff boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


--
-- Name: users_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users_groups (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: users_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.users_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.users ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_user_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users_user_permissions (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: users_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.users_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: appointments; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.appointments (id, status, comment, created_at, updated_at, client_id, psychologist_id, time_slot_id) FROM stdin;
1	completed	Need support with exam stress.	2026-04-16 19:31:06.866906+07	2026-04-16 19:52:56.371981+07	1	1	1
2	completed	Want to discuss anxiety and sleep.	2026-04-16 19:31:06.875922+07	2026-04-16 19:52:56.376658+07	2	2	2
3	completed	Looking for help with adaptation to studies.	2026-04-16 19:31:06.88198+07	2026-04-16 19:52:56.381255+07	3	3	3
4	completed	Need support after a breakup.	2026-04-16 19:31:06.887483+07	2026-04-16 19:52:56.384183+07	4	4	4
5	completed	Burnout and loss of motivation.	2026-04-16 19:31:06.892534+07	2026-04-16 19:52:56.387777+07	5	5	5
6	completed	Hard to manage emotions lately.	2026-04-16 19:31:06.897918+07	2026-04-16 19:52:56.392606+07	6	6	6
7	completed	Want to work on self-esteem.	2026-04-16 19:31:06.901992+07	2026-04-16 19:52:56.396922+07	7	7	7
8	completed	Need help with family pressure.	2026-04-16 19:31:06.906666+07	2026-04-16 19:52:56.400101+07	8	8	8
9	completed	Difficulties with concentration.	2026-04-16 19:31:06.910268+07	2026-04-16 19:52:56.403376+07	9	9	9
10	completed	Relationship conflict and boundaries.	2026-04-16 19:31:06.915652+07	2026-04-16 19:52:56.406815+07	10	10	10
11	completed	Feeling lonely and anxious.	2026-04-16 19:31:06.924114+07	2026-04-16 19:52:56.41007+07	11	11	11
12	completed	Need support after relocation.	2026-04-16 19:31:06.930941+07	2026-04-16 19:52:56.414645+07	12	12	12
13	completed	Trouble balancing study and work.	2026-04-16 19:31:06.936577+07	2026-04-16 19:52:56.418262+07	13	13	13
14	completed	Want to reduce panic symptoms.	2026-04-16 19:31:06.941438+07	2026-04-16 19:52:56.423567+07	14	14	14
15	completed	Need guidance during a crisis period.	2026-04-16 19:31:06.947055+07	2026-04-16 19:52:56.426839+07	15	15	15
16	completed	Need support with exam stress.	2026-04-25 14:56:59.820086+07	2026-04-25 14:56:59.820104+07	1	1	61
17	completed	Want to discuss anxiety and sleep.	2026-04-25 14:56:59.828572+07	2026-04-25 14:56:59.828581+07	2	2	62
18	completed	Looking for help with adaptation to studies.	2026-04-25 14:56:59.834212+07	2026-04-25 14:56:59.834221+07	3	3	63
19	completed	Need support after a breakup.	2026-04-25 14:56:59.838705+07	2026-04-25 14:56:59.838714+07	4	4	64
20	completed	Burnout and loss of motivation.	2026-04-25 14:56:59.844498+07	2026-04-25 14:56:59.844505+07	5	5	65
21	completed	Hard to manage emotions lately.	2026-04-25 14:56:59.850078+07	2026-04-25 14:56:59.850087+07	6	6	66
22	completed	Want to work on self-esteem.	2026-04-25 14:56:59.856579+07	2026-04-25 14:56:59.85659+07	7	7	67
23	completed	Need help with family pressure.	2026-04-25 14:56:59.862843+07	2026-04-25 14:56:59.862854+07	8	8	68
24	completed	Difficulties with concentration.	2026-04-25 14:56:59.868918+07	2026-04-25 14:56:59.86893+07	9	9	69
25	completed	Relationship conflict and boundaries.	2026-04-25 14:56:59.873819+07	2026-04-25 14:56:59.87383+07	10	10	70
26	completed	Feeling lonely and anxious.	2026-04-25 14:56:59.877496+07	2026-04-25 14:56:59.877501+07	11	11	71
27	completed	Need support after relocation.	2026-04-25 14:56:59.883097+07	2026-04-25 14:56:59.88311+07	12	12	72
28	completed	Trouble balancing study and work.	2026-04-25 14:56:59.88776+07	2026-04-25 14:56:59.887772+07	13	13	73
29	completed	Want to reduce panic symptoms.	2026-04-25 14:56:59.892784+07	2026-04-25 14:56:59.892791+07	14	14	74
30	completed	Need guidance during a crisis period.	2026-04-25 14:56:59.897523+07	2026-04-25 14:56:59.897535+07	15	15	75
31	cancelled		2026-04-26 00:21:26.824576+07	2026-04-26 00:21:42.491445+07	22	8	99
34	cancelled		2026-04-26 00:22:34.414152+07	2026-04-26 00:29:04.754729+07	22	8	39
45	cancelled		2026-04-26 00:40:11.991868+07	2026-04-26 00:40:19.029026+07	19	8	99
46	pending	ааааа	2026-04-26 00:44:03.079231+07	2026-04-26 00:44:03.079248+07	27	2	79
44	cancelled		2026-04-26 00:39:41.766235+07	2026-04-26 00:39:56.546514+07	19	6	93
43	cancelled		2026-04-26 00:38:25.681949+07	2026-04-26 00:40:00.154272+07	19	8	99
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	3	add_permission
6	Can change permission	3	change_permission
7	Can delete permission	3	delete_permission
8	Can view permission	3	view_permission
9	Can add group	2	add_group
10	Can change group	2	change_group
11	Can delete group	2	delete_group
12	Can view group	2	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add user	7	add_user
22	Can change user	7	change_user
23	Can delete user	7	delete_user
24	Can view user	7	view_user
25	Can add email confirmation token	6	add_emailconfirmationtoken
26	Can change email confirmation token	6	change_emailconfirmationtoken
27	Can delete email confirmation token	6	delete_emailconfirmationtoken
28	Can view email confirmation token	6	view_emailconfirmationtoken
29	Can add client profile	8	add_clientprofile
30	Can change client profile	8	change_clientprofile
31	Can delete client profile	8	delete_clientprofile
32	Can view client profile	8	view_clientprofile
33	Can add psychologist profile	9	add_psychologistprofile
34	Can change psychologist profile	9	change_psychologistprofile
35	Can delete psychologist profile	9	delete_psychologistprofile
36	Can view psychologist profile	9	view_psychologistprofile
37	Can add specialization	11	add_specialization
38	Can change specialization	11	change_specialization
39	Can delete specialization	11	delete_specialization
40	Can view specialization	11	view_specialization
41	Can add psychologist specialization	10	add_psychologistspecialization
42	Can change psychologist specialization	10	change_psychologistspecialization
43	Can delete psychologist specialization	10	delete_psychologistspecialization
44	Can view psychologist specialization	10	view_psychologistspecialization
45	Can add time slot	12	add_timeslot
46	Can change time slot	12	change_timeslot
47	Can delete time slot	12	delete_timeslot
48	Can view time slot	12	view_timeslot
49	Can add appointment	13	add_appointment
50	Can change appointment	13	change_appointment
51	Can delete appointment	13	delete_appointment
52	Can view appointment	13	view_appointment
53	Can add review	14	add_review
54	Can change review	14	change_review
55	Can delete review	14	delete_review
56	Can view review	14	view_review
57	Can add notification	15	add_notification
58	Can change notification	15	change_notification
59	Can delete notification	15	delete_notification
60	Can view notification	15	view_notification
\.


--
-- Data for Name: client_profiles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.client_profiles (id, first_name, last_name, phone, date_of_birth, avatar, is_profile_complete, user_id) FROM stdin;
1	Anna	Petrova	+79002000001	2004-01-10		t	17
2	Dmitry	Sokolov	+79002000002	2003-02-11		t	18
3	Elena	Kuzmina	+79002000003	2004-03-12		t	19
4	Igor	Popov	+79002000004	2005-04-13		t	20
5	Maria	Volkova	+79002000005	2003-05-14		t	21
6	Sergey	Lebedev	+79002000006	2004-06-15		t	22
7	Olga	Smolina	+79002000007	2002-07-16		t	23
8	Alexey	Gromov	+79002000008	2003-08-17		t	24
9	Natalia	Mironova	+79002000009	2004-09-18		t	25
10	Pavel	Denisov	+79002000010	2005-10-19		t	26
11	Irina	Belova	+79002000011	2003-11-20		t	27
12	Roman	Kiselev	+79002000012	2004-12-21		t	28
13	Yana	Zaitseva	+79002000013	2002-01-22		t	29
14	Kirill	Sorokin	+79002000014	2005-02-23		t	30
15	Vera	Tarasova	+79002000015	2003-03-24		t	31
16			\N	\N		f	32
18			\N	\N		f	34
19	Кирилл	Медведев	+79080142876	2006-08-25	data:image/jpeg;base64,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	t	35
22	наиб	манафов	+79535829179	2010-09-05	data:image/jpeg;base64,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	t	38
27	Наиб	Медведев	+79080142874	2005-09-05	data:image/jpeg;base64,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	t	43
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	group
3	auth	permission
4	contenttypes	contenttype
5	sessions	session
6	users	emailconfirmationtoken
7	users	user
8	clients	clientprofile
9	psychologists	psychologistprofile
10	specializations	psychologistspecialization
11	specializations	specialization
12	schedule	timeslot
13	appointments	appointment
14	reviews	review
15	notifications	notification
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2026-04-16 19:24:37.483469+07
2	contenttypes	0002_remove_content_type_name	2026-04-16 19:24:37.489996+07
3	auth	0001_initial	2026-04-16 19:24:37.545629+07
4	auth	0002_alter_permission_name_max_length	2026-04-16 19:24:37.551091+07
5	auth	0003_alter_user_email_max_length	2026-04-16 19:24:37.555075+07
6	auth	0004_alter_user_username_opts	2026-04-16 19:24:37.559863+07
7	auth	0005_alter_user_last_login_null	2026-04-16 19:24:37.564376+07
8	auth	0006_require_contenttypes_0002	2026-04-16 19:24:37.566056+07
9	auth	0007_alter_validators_add_error_messages	2026-04-16 19:24:37.56947+07
10	auth	0008_alter_user_username_max_length	2026-04-16 19:24:37.573846+07
11	auth	0009_alter_user_last_name_max_length	2026-04-16 19:24:37.577962+07
12	auth	0010_alter_group_name_max_length	2026-04-16 19:24:37.585276+07
13	auth	0011_update_proxy_permissions	2026-04-16 19:24:37.589714+07
14	auth	0012_alter_user_first_name_max_length	2026-04-16 19:24:37.594933+07
15	users	0001_initial	2026-04-16 19:24:37.673087+07
16	admin	0001_initial	2026-04-16 19:24:37.692279+07
17	admin	0002_logentry_remove_auto_add	2026-04-16 19:24:37.697627+07
18	admin	0003_logentry_add_action_flag_choices	2026-04-16 19:24:37.702914+07
19	psychologists	0001_initial	2026-04-16 19:24:37.710205+07
20	schedule	0001_initial	2026-04-16 19:24:37.723311+07
21	clients	0001_initial	2026-04-16 19:24:37.73004+07
22	appointments	0001_initial	2026-04-16 19:24:37.742778+07
23	appointments	0002_initial	2026-04-16 19:24:37.749849+07
24	appointments	0003_initial	2026-04-16 19:24:37.761631+07
25	clients	0002_initial	2026-04-16 19:24:37.771435+07
26	notifications	0001_initial	2026-04-16 19:24:37.778757+07
27	notifications	0002_initial	2026-04-16 19:24:37.790059+07
28	specializations	0001_initial	2026-04-16 19:24:37.819694+07
29	psychologists	0002_initial	2026-04-16 19:24:37.828312+07
30	psychologists	0003_initial	2026-04-16 19:24:37.840966+07
31	reviews	0001_initial	2026-04-16 19:24:37.85712+07
32	sessions	0001_initial	2026-04-16 19:24:37.867199+07
33	users	0002_emailconfirmationtoken_code	2026-04-25 23:40:50.525118+07
34	appointments	0004_allow_rebooking_cancelled_slots	2026-04-26 00:35:47.520873+07
35	psychologists	0004_store_photo_as_data_url	2026-04-26 00:54:13.596238+07
36	clients	0003_store_avatar_as_data_url	2026-04-26 00:54:14.575959+07
37	psychologists	0005_compact_photo_data_urls	2026-04-26 00:56:58.870886+07
38	clients	0004_compact_avatar_data_urls	2026-04-26 00:56:59.346848+07
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: email_confirmation_tokens; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.email_confirmation_tokens (id, token, is_used, created_at, expires_at, user_id, code) FROM stdin;
1	fc530e28-5f96-442c-a3ac-8ac03aad3b18	t	2026-04-16 19:30:52.742389+07	2026-05-16 19:30:52.739297+07	1	
2	f81d9160-a37a-4b96-9f09-2bfd2f7564fd	t	2026-04-16 19:30:53.283869+07	2026-05-16 19:30:53.282902+07	2	
3	dfd8e7dd-b19f-4b57-9861-2706a6b71df5	t	2026-04-16 19:30:53.78536+07	2026-05-16 19:30:53.784062+07	3	
4	803cfc73-5a57-44b6-94a7-36cff643dd21	t	2026-04-16 19:30:54.365956+07	2026-05-16 19:30:54.365318+07	4	
5	152152f2-5916-4f2d-ba3c-2756aea710b5	t	2026-04-16 19:30:54.881997+07	2026-05-16 19:30:54.881091+07	5	
6	2f03dbf0-4e3b-4d65-ab35-98d790ed1f88	t	2026-04-16 19:30:55.367505+07	2026-05-16 19:30:55.366731+07	6	
7	2aac1c82-8f15-4439-abf5-dbc941ce97db	t	2026-04-16 19:30:55.838405+07	2026-05-16 19:30:55.837172+07	7	
8	8ed07d82-65ae-4322-8253-fd70290ff522	t	2026-04-16 19:30:56.270289+07	2026-05-16 19:30:56.269108+07	8	
9	073dccd4-b139-4314-bda4-895c9446e651	t	2026-04-16 19:30:56.722399+07	2026-05-16 19:30:56.721406+07	9	
10	0c37e2b9-3c4e-4bd3-9e1e-2c9ca4f888c3	t	2026-04-16 19:30:57.175933+07	2026-05-16 19:30:57.175109+07	10	
11	7786c7d5-9f38-4a9e-9130-567dbab4d804	t	2026-04-16 19:30:57.650322+07	2026-05-16 19:30:57.649464+07	11	
12	8c3fb8af-3b27-4706-b791-107d46efb2f0	t	2026-04-16 19:30:58.131128+07	2026-05-16 19:30:58.130136+07	12	
13	c6f740e2-9f19-4e4b-bcc1-939f6feadc42	t	2026-04-16 19:30:58.589906+07	2026-05-16 19:30:58.589001+07	13	
14	90c736f5-af91-4504-b36f-0328e05571d4	t	2026-04-16 19:30:59.060823+07	2026-05-16 19:30:59.05972+07	14	
15	b60464a9-c38a-48ba-9dd8-233cd91584fc	t	2026-04-16 19:30:59.518362+07	2026-05-16 19:30:59.517526+07	15	
16	ae2e05ff-8a4b-486f-ac92-752b678b6a10	t	2026-04-16 19:30:59.985531+07	2026-05-16 19:30:59.984337+07	16	
17	b4c3653c-a004-43d0-bc53-d670a4362eb5	t	2026-04-16 19:31:00.429118+07	2026-05-16 19:31:00.427493+07	17	
18	4edf4e29-86ea-4a48-955b-8020d83f761c	t	2026-04-16 19:31:00.873366+07	2026-05-16 19:31:00.872506+07	18	
19	498cb476-d906-42e3-83ef-7a90d019b40c	t	2026-04-16 19:31:01.338046+07	2026-05-16 19:31:01.337091+07	19	
20	31e50c1a-078c-4b42-b5ba-a13ffe9716c3	t	2026-04-16 19:31:01.789986+07	2026-05-16 19:31:01.788903+07	20	
21	a174fe11-ebe3-4ae8-b1ed-7824f59f7e08	t	2026-04-16 19:31:02.241634+07	2026-05-16 19:31:02.240793+07	21	
22	69c14f3a-2468-4c47-9e09-d503e7881930	t	2026-04-16 19:31:02.685405+07	2026-05-16 19:31:02.68452+07	22	
23	72211953-4ea5-480e-9def-1789281158a8	t	2026-04-16 19:31:03.156382+07	2026-05-16 19:31:03.15533+07	23	
24	d7c99be0-30ab-469a-9be7-ef70b4f8696b	t	2026-04-16 19:31:03.616408+07	2026-05-16 19:31:03.615617+07	24	
25	7346fc77-095d-4522-ba9c-24e4232c55fd	t	2026-04-16 19:31:04.084001+07	2026-05-16 19:31:04.082974+07	25	
26	5feaa487-a4fe-476e-855d-38622ca9d5ff	t	2026-04-16 19:31:04.549684+07	2026-05-16 19:31:04.548898+07	26	
27	b8b6160f-17ac-41ca-a3a6-ccda6b5376db	t	2026-04-16 19:31:05.026076+07	2026-05-16 19:31:05.025135+07	27	
28	a7b79725-4cda-4e49-ba81-fc738d825004	t	2026-04-16 19:31:05.463798+07	2026-05-16 19:31:05.462414+07	28	
29	85acdbba-6ce2-4f70-aaa2-a5f40434d59c	t	2026-04-16 19:31:05.917254+07	2026-05-16 19:31:05.916426+07	29	
30	836e8c0d-2dc8-4db8-a2b5-cb9bc4def236	t	2026-04-16 19:31:06.381871+07	2026-05-16 19:31:06.380986+07	30	
31	a794b63c-a5ac-43d0-9333-e431b4d3ec28	t	2026-04-16 19:31:06.843503+07	2026-05-16 19:31:06.842386+07	31	
32	14c1f271-c062-4a26-ae9d-030b99fa310d	f	2026-04-16 19:37:32.274877+07	2026-04-17 19:37:32.274681+07	32	
34	0679eeb3-eb51-4b87-be2a-7ca1c6815ddd	t	2026-04-25 15:09:19.174044+07	2026-04-26 15:09:19.173598+07	34	
35	7efbdbd8-755b-44f6-a91f-ff6186c200e7	t	2026-04-25 15:37:46.600846+07	2026-04-26 15:37:46.600427+07	35	
38	0827bc81-c07b-4b4d-a7c6-639429191d3a	t	2026-04-25 23:47:13.086901+07	2026-04-26 23:47:13.086469+07	38	209528
39	f2979bae-e167-4e45-944c-729f2d28ec46	t	2026-04-26 00:41:27.602856+07	2026-04-27 00:41:27.602683+07	43	476133
\.


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.notifications (id, type, title, message, is_read, created_at, user_id) FROM stdin;
1	system	Demo notification 1	Demo message 1 for admin@young-psy.ru.	f	2026-04-16 19:31:07.065759+07	1
2	review_request	Demo notification 2	Demo message 2 for a.ivanova@young-psy.ru.	f	2026-04-16 19:31:07.068778+07	2
3	appointment_completed	Demo notification 3	Demo message 3 for m.smirnov@young-psy.ru.	f	2026-04-16 19:31:07.072168+07	3
4	verification_approved	Demo notification 4	Demo message 4 for e.kozlova@young-psy.ru.	f	2026-04-16 19:31:07.074817+07	4
5	appointment_confirmed	Demo notification 5	Demo message 5 for d.novikov@young-psy.ru.	f	2026-04-16 19:31:07.077294+07	5
6	system	Demo notification 6	Demo message 6 for v.fedorova@young-psy.ru.	f	2026-04-16 19:31:07.07992+07	6
7	review_request	Demo notification 7	Demo message 7 for i.morozov@young-psy.ru.	f	2026-04-16 19:31:07.082394+07	7
8	appointment_completed	Demo notification 8	Demo message 8 for k.volkova@young-psy.ru.	f	2026-04-16 19:31:07.084431+07	8
9	verification_approved	Demo notification 9	Demo message 9 for r.lebedev@young-psy.ru.	f	2026-04-16 19:31:07.087276+07	9
10	appointment_confirmed	Demo notification 10	Demo message 10 for o.orlova@young-psy.ru.	f	2026-04-16 19:31:07.089976+07	10
11	system	Demo notification 11	Demo message 11 for p.kovalev@young-psy.ru.	f	2026-04-16 19:31:07.091426+07	11
12	review_request	Demo notification 12	Demo message 12 for n.nikolaeva@young-psy.ru.	f	2026-04-16 19:31:07.092998+07	12
13	appointment_completed	Demo notification 13	Demo message 13 for a.andreev@young-psy.ru.	f	2026-04-16 19:31:07.095888+07	13
14	verification_approved	Demo notification 14	Demo message 14 for y.sidorova@young-psy.ru.	f	2026-04-16 19:31:07.097853+07	14
15	appointment_confirmed	Demo notification 15	Demo message 15 for m.egorov@young-psy.ru.	f	2026-04-16 19:31:07.09945+07	15
\.


--
-- Data for Name: psychologist_profiles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.psychologist_profiles (id, first_name, last_name, patronymic, phone, photo, experience_years, education, bio, price, diploma_scan, is_verified, verified_at, is_profile_complete, user_id) FROM stdin;
12	Artem	Andreev	Igorevich	+79001000012		4	Institute of Social Psychology, 2022	Supports clients with communication and confidence issues.	2600.00		t	2026-04-25 14:56:50.976205+07	t	13
13	Yulia	Sidorova	Olegovna	+79001000013		2	Institute of Practical Psychology, 2024	Uses a warm approach for personal growth and reflection.	2300.00		t	2026-04-25 14:56:51.517353+07	t	14
14	Mikhail	Egorov	Petrovich	+79001000014		5	Institute of Clinical Psychology, 2021	Works with stress recovery and crisis adaptation.	2800.00		t	2026-04-25 14:56:52.002189+07	t	15
15	Sofia	Makarova	Romanovna	+79001000015		3	Institute of Practical Psychology, 2023	Helps with boundaries, relationships, and self-support.	2550.00		t	2026-04-25 14:56:52.49688+07	t	16
1	Alina	Ivanova	Sergeevna	+79001000001		3	Institute of Practical Psychology, 2023	Works with anxiety, adaptation, and self-esteem questions.	2500.00		t	2026-04-25 14:56:43.793517+07	t	2
2	Maksim	Smirnov	Andreevich	+79001000002		4	Institute of Practical Psychology, 2022	Focuses on burnout, motivation, and student stress.	2600.00		t	2026-04-25 14:56:44.274021+07	t	3
3	Elena	Kozlova	Igorevna	+79001000003		2	Institute of Practical Psychology, 2024	Supports young adults in relationships and personal growth.	2400.00		t	2026-04-25 14:56:44.77543+07	t	4
4	Daniil	Novikov	Olegovich	+79001000004		5	Institute of Clinical Psychology, 2021	Works with trauma, crisis situations, and adaptation.	2800.00		t	2026-04-25 14:56:45.423076+07	t	5
5	Vera	Fedorova	Petrovna	+79001000005		3	Institute of Practical Psychology, 2023	Helps with self-esteem and difficult life periods.	2550.00		t	2026-04-25 14:56:46.129952+07	t	6
6	Ilya	Morozov	Vladimirovich	+79001000006		4	Institute of Social Psychology, 2022	Specializes in communication, boundaries, and conflict work.	2650.00		t	2026-04-25 14:56:46.846496+07	t	7
7	Ksenia	Volkova	Romanovna	+79001000007		3	Institute of Practical Psychology, 2023	Uses a supportive, structured approach for student clients.	2500.00		t	2026-04-25 14:56:47.581988+07	t	8
8	Roman	Lebedev	Dmitrievich	+79001000008		5	Institute of Clinical Psychology, 2021	Works with anxiety, panic symptoms, and burnout.	2850.00		t	2026-04-25 14:56:48.35253+07	t	9
9	Olga	Orlova	Nikolaevna	+79001000009		2	Institute of Practical Psychology, 2024	Supports students around exams and adaptation to change.	2350.00		t	2026-04-25 14:56:49.12803+07	t	10
10	Pavel	Kovalev	Sergeevich	+79001000010		4	Institute of Practical Psychology, 2022	Focuses on relationships and emotional regulation.	2700.00		t	2026-04-25 14:56:49.854992+07	t	11
11	Natalia	Nikolaeva	Alekseevna	+79001000011		3	Institute of Practical Psychology, 2023	Works with grief, loss, and inner stability.	2500.00		t	2026-04-25 14:56:50.487389+07	t	12
\.


--
-- Data for Name: psychologist_specializations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.psychologist_specializations (id, is_primary, psychologist_id, specialization_id) FROM stdin;
1	t	1	1
2	f	1	6
3	t	2	2
4	f	2	7
5	t	3	3
6	f	3	8
7	t	4	4
8	f	4	9
9	t	5	5
10	f	5	10
11	t	6	6
12	f	6	11
13	t	7	7
14	f	7	12
15	t	8	8
16	f	8	13
17	t	9	9
18	f	9	14
19	t	10	10
20	f	10	15
21	t	11	11
22	f	11	1
23	t	12	12
24	f	12	2
25	t	13	13
26	f	13	3
27	t	14	14
28	f	14	4
29	t	15	15
30	f	15	5
\.


--
-- Data for Name: reviews; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.reviews (id, rating, text, created_at, appointment_id) FROM stdin;
29	5	Clear, calm, and very attentive work.	2026-04-25 14:56:59.926989+07	29
30	5	The consultation met my expectations.	2026-04-25 14:56:59.929461+07	30
1	4	The session was calm and helpful.	2026-04-16 19:31:06.949327+07	1
2	5	I felt heard and understood.	2026-04-16 19:31:06.952802+07	2
3	5	The specialist explained things clearly.	2026-04-16 19:31:06.954834+07	3
4	4	It became easier after the first meeting.	2026-04-16 19:31:06.957362+07	4
5	5	Very supportive and professional.	2026-04-16 19:31:06.959644+07	5
6	5	Helpful conversation with practical steps.	2026-04-16 19:31:06.962174+07	6
7	4	Warm approach and good structure.	2026-04-16 19:31:06.963923+07	7
8	5	I would continue working with this psychologist.	2026-04-16 19:31:06.966117+07	8
9	5	The consultation helped me look at the problem differently.	2026-04-16 19:31:06.967982+07	9
10	4	Good specialist for student-related stress.	2026-04-16 19:31:06.970074+07	10
11	5	I liked the respectful and careful tone.	2026-04-16 19:31:06.971524+07	11
12	5	The meeting gave me more confidence.	2026-04-16 19:31:06.972634+07	12
13	4	Useful support in a difficult moment.	2026-04-16 19:31:06.973831+07	13
14	5	Clear, calm, and very attentive work.	2026-04-16 19:31:06.975539+07	14
15	5	The consultation met my expectations.	2026-04-16 19:31:06.977516+07	15
16	4	The session was calm and helpful.	2026-04-25 14:56:59.901584+07	16
17	5	I felt heard and understood.	2026-04-25 14:56:59.904977+07	17
18	5	The specialist explained things clearly.	2026-04-25 14:56:59.907309+07	18
19	4	It became easier after the first meeting.	2026-04-25 14:56:59.909464+07	19
20	5	Very supportive and professional.	2026-04-25 14:56:59.911114+07	20
21	5	Helpful conversation with practical steps.	2026-04-25 14:56:59.912378+07	21
22	4	Warm approach and good structure.	2026-04-25 14:56:59.914532+07	22
23	5	I would continue working with this psychologist.	2026-04-25 14:56:59.916345+07	23
24	5	The consultation helped me look at the problem differently.	2026-04-25 14:56:59.917636+07	24
25	4	Good specialist for student-related stress.	2026-04-25 14:56:59.91962+07	25
26	5	I liked the respectful and careful tone.	2026-04-25 14:56:59.921035+07	26
27	5	The meeting gave me more confidence.	2026-04-25 14:56:59.923247+07	27
28	4	Useful support in a difficult moment.	2026-04-25 14:56:59.925041+07	28
\.


--
-- Data for Name: specializations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.specializations (id, name, slug, description, icon) FROM stdin;
1	Individual Consulting	individual-consulting	Individual Consulting support direction for the center.	brain
2	Anxiety Support	anxiety-support	Anxiety Support support direction for the center.	brain
3	Stress Management	stress-management	Stress Management support direction for the center.	brain
4	Family Therapy	family-therapy	Family Therapy support direction for the center.	brain
5	Student Adaptation	student-adaptation	Student Adaptation support direction for the center.	brain
6	Self-Esteem	self-esteem	Self-Esteem support direction for the center.	brain
7	Career Guidance	career-guidance	Career Guidance support direction for the center.	brain
8	Burnout Recovery	burnout-recovery	Burnout Recovery support direction for the center.	brain
9	Relationship Issues	relationship-issues	Relationship Issues support direction for the center.	brain
10	Crisis Support	crisis-support	Crisis Support support direction for the center.	brain
11	Grief Support	grief-support	Grief Support support direction for the center.	brain
12	Teen Support	teen-support	Teen Support support direction for the center.	brain
13	CBT	cbt	CBT support direction for the center.	brain
14	Art Therapy	art-therapy	Art Therapy support direction for the center.	brain
15	Trauma Support	trauma-support	Trauma Support support direction for the center.	brain
\.


--
-- Data for Name: time_slots; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.time_slots (id, date, start_time, end_time, is_available, psychologist_id) FROM stdin;
9	2026-04-09	11:00:00	12:00:00	f	9
37	2026-04-25	10:00:00	11:00:00	t	8
66	2026-04-15	11:00:00	12:00:00	f	6
10	2026-04-10	11:00:00	12:00:00	f	10
38	2026-04-26	12:00:00	13:00:00	t	8
39	2026-04-27	14:00:00	15:00:00	t	8
11	2026-04-11	11:00:00	12:00:00	f	11
67	2026-04-16	11:00:00	12:00:00	f	7
40	2026-04-26	10:00:00	11:00:00	t	9
12	2026-04-12	11:00:00	12:00:00	f	12
41	2026-04-27	12:00:00	13:00:00	t	9
68	2026-04-17	11:00:00	12:00:00	f	8
13	2026-04-13	11:00:00	12:00:00	f	13
69	2026-04-18	11:00:00	12:00:00	f	9
42	2026-04-28	14:00:00	15:00:00	t	9
43	2026-04-27	10:00:00	11:00:00	t	10
70	2026-04-19	11:00:00	12:00:00	f	10
71	2026-04-20	11:00:00	12:00:00	f	11
14	2026-04-14	11:00:00	12:00:00	f	14
44	2026-04-28	12:00:00	13:00:00	t	10
45	2026-04-29	14:00:00	15:00:00	t	10
72	2026-04-21	11:00:00	12:00:00	f	12
46	2026-04-28	10:00:00	11:00:00	t	11
73	2026-04-22	11:00:00	12:00:00	f	13
47	2026-04-29	12:00:00	13:00:00	t	11
15	2026-04-15	11:00:00	12:00:00	f	15
48	2026-04-30	14:00:00	15:00:00	t	11
16	2026-04-18	10:00:00	11:00:00	t	1
49	2026-04-29	10:00:00	11:00:00	t	12
17	2026-04-19	12:00:00	13:00:00	t	1
50	2026-04-30	12:00:00	13:00:00	t	12
18	2026-04-20	14:00:00	15:00:00	t	1
1	2026-04-01	11:00:00	12:00:00	f	1
51	2026-05-01	14:00:00	15:00:00	t	12
19	2026-04-19	10:00:00	11:00:00	t	2
52	2026-04-30	10:00:00	11:00:00	t	13
53	2026-05-01	12:00:00	13:00:00	t	13
20	2026-04-20	12:00:00	13:00:00	t	2
21	2026-04-21	14:00:00	15:00:00	t	2
54	2026-05-02	14:00:00	15:00:00	t	13
55	2026-05-01	10:00:00	11:00:00	t	14
22	2026-04-20	10:00:00	11:00:00	t	3
56	2026-05-02	12:00:00	13:00:00	t	14
57	2026-05-03	14:00:00	15:00:00	t	14
58	2026-05-02	10:00:00	11:00:00	t	15
59	2026-05-03	12:00:00	13:00:00	t	15
60	2026-05-04	14:00:00	15:00:00	t	15
61	2026-04-10	11:00:00	12:00:00	f	1
2	2026-04-02	11:00:00	12:00:00	f	2
62	2026-04-11	11:00:00	12:00:00	f	2
23	2026-04-21	12:00:00	13:00:00	t	3
3	2026-04-03	11:00:00	12:00:00	f	3
63	2026-04-12	11:00:00	12:00:00	f	3
24	2026-04-22	14:00:00	15:00:00	t	3
74	2026-04-23	11:00:00	12:00:00	f	14
4	2026-04-04	11:00:00	12:00:00	f	4
25	2026-04-21	10:00:00	11:00:00	t	4
75	2026-04-24	11:00:00	12:00:00	f	15
5	2026-04-05	11:00:00	12:00:00	f	5
76	2026-04-27	10:00:00	11:00:00	t	1
26	2026-04-22	12:00:00	13:00:00	t	4
6	2026-04-06	11:00:00	12:00:00	f	6
27	2026-04-23	14:00:00	15:00:00	t	4
7	2026-04-07	11:00:00	12:00:00	f	7
28	2026-04-22	10:00:00	11:00:00	t	5
8	2026-04-08	11:00:00	12:00:00	f	8
29	2026-04-23	12:00:00	13:00:00	t	5
30	2026-04-24	14:00:00	15:00:00	t	5
31	2026-04-23	10:00:00	11:00:00	t	6
32	2026-04-24	12:00:00	13:00:00	t	6
33	2026-04-25	14:00:00	15:00:00	t	6
34	2026-04-24	10:00:00	11:00:00	t	7
35	2026-04-25	12:00:00	13:00:00	t	7
36	2026-04-26	14:00:00	15:00:00	t	7
77	2026-04-28	12:00:00	13:00:00	t	1
64	2026-04-13	11:00:00	12:00:00	f	4
78	2026-04-29	14:00:00	15:00:00	t	1
65	2026-04-14	11:00:00	12:00:00	f	5
80	2026-04-29	12:00:00	13:00:00	t	2
81	2026-04-30	14:00:00	15:00:00	t	2
82	2026-04-29	10:00:00	11:00:00	t	3
83	2026-04-30	12:00:00	13:00:00	t	3
84	2026-05-01	14:00:00	15:00:00	t	3
85	2026-04-30	10:00:00	11:00:00	t	4
86	2026-05-01	12:00:00	13:00:00	t	4
87	2026-05-02	14:00:00	15:00:00	t	4
88	2026-05-01	10:00:00	11:00:00	t	5
89	2026-05-02	12:00:00	13:00:00	t	5
90	2026-05-03	14:00:00	15:00:00	t	5
91	2026-05-02	10:00:00	11:00:00	t	6
92	2026-05-03	12:00:00	13:00:00	t	6
94	2026-05-03	10:00:00	11:00:00	t	7
95	2026-05-04	12:00:00	13:00:00	t	7
96	2026-05-05	14:00:00	15:00:00	t	7
97	2026-05-04	10:00:00	11:00:00	t	8
98	2026-05-05	12:00:00	13:00:00	t	8
100	2026-05-05	10:00:00	11:00:00	t	9
101	2026-05-06	12:00:00	13:00:00	t	9
102	2026-05-07	14:00:00	15:00:00	t	9
103	2026-05-06	10:00:00	11:00:00	t	10
79	2026-04-28	10:00:00	11:00:00	f	2
93	2026-05-04	14:00:00	15:00:00	t	6
104	2026-05-07	12:00:00	13:00:00	t	10
105	2026-05-08	14:00:00	15:00:00	t	10
106	2026-05-07	10:00:00	11:00:00	t	11
107	2026-05-08	12:00:00	13:00:00	t	11
108	2026-05-09	14:00:00	15:00:00	t	11
109	2026-05-08	10:00:00	11:00:00	t	12
110	2026-05-09	12:00:00	13:00:00	t	12
111	2026-05-10	14:00:00	15:00:00	t	12
112	2026-05-09	10:00:00	11:00:00	t	13
113	2026-05-10	12:00:00	13:00:00	t	13
114	2026-05-11	14:00:00	15:00:00	t	13
115	2026-05-10	10:00:00	11:00:00	t	14
116	2026-05-11	12:00:00	13:00:00	t	14
117	2026-05-12	14:00:00	15:00:00	t	14
118	2026-05-11	10:00:00	11:00:00	t	15
119	2026-05-12	12:00:00	13:00:00	t	15
120	2026-05-13	14:00:00	15:00:00	t	15
99	2026-05-06	14:00:00	15:00:00	t	8
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, password, last_login, is_superuser, email, role, is_active, is_staff, date_joined) FROM stdin;
1	pbkdf2_sha256$1200000$d3rsEFeucD33j9rVNKYDhT$zyz4U+SAJqhozmO8UIpjgqMDb+AzyXzFZiltZyZtU5M=	\N	t	admin@young-psy.ru	admin	t	t	2026-04-16 19:30:52.147827+07
2	pbkdf2_sha256$1200000$aWZs3Q3PGTNfMgBxkRfqK5$XCcvLcWCQ2f/+1ehGl+ktX3OMm4JGIB/mlb9jz3iKLk=	\N	f	a.ivanova@young-psy.ru	psychologist	t	f	2026-04-16 19:30:52.779986+07
3	pbkdf2_sha256$1200000$tPUPEsMykQBESIatCgbWHQ$ntqxMXTIxFYsRzO0apo7K2QNfMOzroOqw6jV72LSHKM=	\N	f	m.smirnov@young-psy.ru	psychologist	t	f	2026-04-16 19:30:53.292553+07
4	pbkdf2_sha256$1200000$bkDelYfnGtTGAaJigC8bBC$nRPVEOJ74DDYlJMgTg/rslOwRqXSUimifF4UgzBjI/o=	\N	f	e.kozlova@young-psy.ru	psychologist	t	f	2026-04-16 19:30:53.791372+07
5	pbkdf2_sha256$1200000$jdDKKIrVlk8Um2eXoagUiB$dS3rl5mggUVp3rcNLGdwhKfDuYetgy4kjX+0XY9tgAU=	\N	f	d.novikov@young-psy.ru	psychologist	t	f	2026-04-16 19:30:54.37117+07
6	pbkdf2_sha256$1200000$79uil0OmtuPouLKEzWS1XL$0RrP5Y4ordekn1dT+gVXUqfEAWpfckWZUMhZHAqfmAQ=	\N	f	v.fedorova@young-psy.ru	psychologist	t	f	2026-04-16 19:30:54.886237+07
7	pbkdf2_sha256$1200000$JugeD5f9iMRgcfC08Mogym$ppf+BnQJG+xCEqEWEJpabPgP5EkQ4aZJeirhvHnUMls=	\N	f	i.morozov@young-psy.ru	psychologist	t	f	2026-04-16 19:30:55.371478+07
8	pbkdf2_sha256$1200000$UKCqNTE5Ozi6roONInS2h1$iXniGHKH1AsLDSq50cMmZ2NEE7QMfB4UyLLxFdg51J4=	\N	f	k.volkova@young-psy.ru	psychologist	t	f	2026-04-16 19:30:55.842514+07
9	pbkdf2_sha256$1200000$JQ1pTtU4gEQnUuyJNaRCTb$OA4FWXLnw1V6VinexCSl/WzlyLRYVZZ3tsAsKHiFuCE=	\N	f	r.lebedev@young-psy.ru	psychologist	t	f	2026-04-16 19:30:56.274977+07
10	pbkdf2_sha256$1200000$i3zz3AjklbJRNI5ei4JfUm$DavVqBoGqpas7R63GldBx5Y2NMWKF1aL53UZv7DbUkA=	\N	f	o.orlova@young-psy.ru	psychologist	t	f	2026-04-16 19:30:56.726373+07
11	pbkdf2_sha256$1200000$UZGtk4bwelXWufWrY7vgGL$AdYpc5S9I7yG+dX7cq/qGUUcFNMihSFuzeXvCsuuHCw=	\N	f	p.kovalev@young-psy.ru	psychologist	t	f	2026-04-16 19:30:57.181173+07
12	pbkdf2_sha256$1200000$9hdYPnEJ5KKwmsZkgE1Lbb$H7unGe6GR+8LF3/1+i+c8OaczKjL2PtsAj+Vx3BEEPQ=	\N	f	n.nikolaeva@young-psy.ru	psychologist	t	f	2026-04-16 19:30:57.656387+07
13	pbkdf2_sha256$1200000$QvuWm7rfNUJgOYrwjewnSr$Ig0IPKFr5A8BrQ6lDymCpgBX9QR0t2+1uzQRCtt0UDk=	\N	f	a.andreev@young-psy.ru	psychologist	t	f	2026-04-16 19:30:58.138427+07
14	pbkdf2_sha256$1200000$SqiuaKLTrhNU4uBwU3jCm0$++KGoKHpB4B1fCA6i+ru/u5GYLlAmtCBlW7I5jMIaxg=	\N	f	y.sidorova@young-psy.ru	psychologist	t	f	2026-04-16 19:30:58.594185+07
15	pbkdf2_sha256$1200000$x1CcnURVJpDmOlA8Pn3Xu8$XjksZ9DIfXVEcEEiyDIIRHCuWPI6eF3S1Nm3UeG/L/8=	\N	f	m.egorov@young-psy.ru	psychologist	t	f	2026-04-16 19:30:59.066277+07
16	pbkdf2_sha256$1200000$LxVvJfmMs8W5NyXQaC3zFb$J1clflXd2ymQvoMBlJVZL5MuIl4U0WtA2IWJcBLq13s=	\N	f	s.makarova@young-psy.ru	psychologist	t	f	2026-04-16 19:30:59.524456+07
17	pbkdf2_sha256$1200000$VeYwf7dWZkQZPfaMKknAJg$bONtEu1lAuYIo1FKqhY23baYGh0zIevXHyuBY4zXjNk=	\N	f	client01@young-psy.ru	client	t	f	2026-04-16 19:30:59.991365+07
18	pbkdf2_sha256$1200000$TZYPPIoi4kP1gzd9H4YdBS$kgJplwBnG3moCes0lGB1kAjEsSE8oFIhv4rif8HnWbM=	\N	f	client02@young-psy.ru	client	t	f	2026-04-16 19:31:00.431509+07
19	pbkdf2_sha256$1200000$tXNsUk0u2BnP6ixfzmzOd1$smGgx64goglsFo8S4V3S15RRw3cGOAsAQSo1kXTxazw=	\N	f	client03@young-psy.ru	client	t	f	2026-04-16 19:31:00.874408+07
20	pbkdf2_sha256$1200000$arnBvn45LSlmdXkMH0CIL1$82XVt9jC+HXn5MhBwprOWu4/R9XiGnx8XfBbMezvZZg=	\N	f	client04@young-psy.ru	client	t	f	2026-04-16 19:31:01.339579+07
21	pbkdf2_sha256$1200000$6TfWJtc1yfz6xRKkZ4ABEa$BOUVB3bz6v4lJjOnoD22jQrdS5GmOA0L5l/NXsf4BT8=	\N	f	client05@young-psy.ru	client	t	f	2026-04-16 19:31:01.791685+07
22	pbkdf2_sha256$1200000$SP2GPiZicMpb7N6mYzezFI$qUSroNdy7Eg7s29gDJp6QYje/Bxerug1XC2J8pS8L2c=	\N	f	client06@young-psy.ru	client	t	f	2026-04-16 19:31:02.242894+07
23	pbkdf2_sha256$1200000$NUrYMnB10XnHf48NtNto39$WzcWU8YjEs8Be3IhMoZ09er5VWgpsAIkXkblT3ewytI=	\N	f	client07@young-psy.ru	client	t	f	2026-04-16 19:31:02.687683+07
24	pbkdf2_sha256$1200000$AvYm9HyeIPiUY2Gkct7HNs$79rACHI4BsJwLqLD1eJBs5T7DQjj8sCKgKosfEw3JP0=	\N	f	client08@young-psy.ru	client	t	f	2026-04-16 19:31:03.157767+07
25	pbkdf2_sha256$1200000$uShhgka1Z0DzBTV9AueB8H$rq9FNxZIlg0rJBrFsgY18XPoZVbEx1StRcg3JCZjxqk=	\N	f	client09@young-psy.ru	client	t	f	2026-04-16 19:31:03.617736+07
26	pbkdf2_sha256$1200000$jtfCLtb4dbvrUeHkHixnIA$uBqNYc2IjJhlYt49jDALH48lIpuxq9vx98lyMKmKYzE=	\N	f	client10@young-psy.ru	client	t	f	2026-04-16 19:31:04.085653+07
27	pbkdf2_sha256$1200000$8JgoRG6DGD4O1x5kBtS5Zf$CSEu5CMfcCFeM96GlR86B+RSqi+v593sMSgcW4MeD7M=	\N	f	client11@young-psy.ru	client	t	f	2026-04-16 19:31:04.550834+07
28	pbkdf2_sha256$1200000$GuKfBTmYPepgMI75fi0zLU$3pHmF/5Oa1ZKlJqEsi+KecNDd3osbA+LVHetjgqAsA0=	\N	f	client12@young-psy.ru	client	t	f	2026-04-16 19:31:05.028488+07
29	pbkdf2_sha256$1200000$4NhqFwGXjTJ3Gp5JB9oHkD$dgl+q9twdSEiCf75LEx3NawoLX5R6d4VqMetWVXK/u0=	\N	f	client13@young-psy.ru	client	t	f	2026-04-16 19:31:05.465873+07
30	pbkdf2_sha256$1200000$WE7LcGmurLEfpdbGRcfemL$7aIkpSVW+DJXUWF1NgqrlEymvusnDqe61LB70LDS+Wo=	\N	f	client14@young-psy.ru	client	t	f	2026-04-16 19:31:05.918988+07
31	pbkdf2_sha256$1200000$f92xVnWEysiW5VsQQGDGV8$1rp26rjVaGAUc4p6J4XDFMuNjfFhJ7jUjI9CC3U2oFE=	\N	f	client15@young-psy.ru	client	t	f	2026-04-16 19:31:06.383504+07
32	pbkdf2_sha256$1200000$iaCmMxdwg3jLV6hnMHbFpz$EahYM0aoiBHBU5coC28YMQuClDZHAdqWUzlYNX5mx/4=	\N	f	test295610245@young-psy.ru	client	f	f	2026-04-16 19:37:31.633559+07
34	pbkdf2_sha256$1200000$nZEsF5b9EkWeJIRG4Ckc26$e7DqnSnqufjeke8UbtfA4b2FAbZ94Kf/OZDtWhSBr5I=	\N	f	test509255@example.com	client	t	f	2026-04-25 15:09:18.503727+07
35	pbkdf2_sha256$1200000$1V0OB6QASA2BBs3j1aB6Q1$8kGFjFVlLokIfCCqSGH0DeqfPrTkGQGHRY4aDG/jaqw=	\N	f	kirillmedvedev200@gmail.com	client	t	f	2026-04-25 15:37:45.80022+07
38	pbkdf2_sha256$1200000$pEFWinnNHSETu74MkZzMd5$Tcl+uJAOydbwpYyyWPFWs3xsCb35T5nzxbNagudVMB8=	\N	f	manafovnaib12@gmail.com	client	t	f	2026-04-25 23:47:12.360164+07
43	pbkdf2_sha256$1200000$Zi7iCF5dzrZj107l8pIQjD$SVxY5i0pi50gMcU48fFZyrRzWMj3oBiiOHCDbeMfrCg=	\N	f	manafovnaib11@gmail.com	client	t	f	2026-04-26 00:41:26.994744+07
\.


--
-- Data for Name: users_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: users_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: appointments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.appointments_id_seq', 46, true);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 60, true);


--
-- Name: client_profiles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.client_profiles_id_seq', 30, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 15, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 38, true);


--
-- Name: email_confirmation_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.email_confirmation_tokens_id_seq', 39, true);


--
-- Name: notifications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.notifications_id_seq', 15, true);


--
-- Name: psychologist_profiles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.psychologist_profiles_id_seq', 17, true);


--
-- Name: psychologist_specializations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.psychologist_specializations_id_seq', 30, true);


--
-- Name: reviews_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.reviews_id_seq', 30, true);


--
-- Name: specializations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.specializations_id_seq', 15, true);


--
-- Name: time_slots_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.time_slots_id_seq', 122, true);


--
-- Name: users_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_groups_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 48, true);


--
-- Name: users_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_user_permissions_id_seq', 1, false);


--
-- Name: appointments appointments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: client_profiles client_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.client_profiles
    ADD CONSTRAINT client_profiles_pkey PRIMARY KEY (id);


--
-- Name: client_profiles client_profiles_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.client_profiles
    ADD CONSTRAINT client_profiles_user_id_key UNIQUE (user_id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: email_confirmation_tokens email_confirmation_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_confirmation_tokens
    ADD CONSTRAINT email_confirmation_tokens_pkey PRIMARY KEY (id);


--
-- Name: email_confirmation_tokens email_confirmation_tokens_token_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_confirmation_tokens
    ADD CONSTRAINT email_confirmation_tokens_token_key UNIQUE (token);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: psychologist_profiles psychologist_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.psychologist_profiles
    ADD CONSTRAINT psychologist_profiles_pkey PRIMARY KEY (id);


--
-- Name: psychologist_profiles psychologist_profiles_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.psychologist_profiles
    ADD CONSTRAINT psychologist_profiles_user_id_key UNIQUE (user_id);


--
-- Name: psychologist_specializations psychologist_specializat_psychologist_id_speciali_541db4d2_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.psychologist_specializations
    ADD CONSTRAINT psychologist_specializat_psychologist_id_speciali_541db4d2_uniq UNIQUE (psychologist_id, specialization_id);


--
-- Name: psychologist_specializations psychologist_specializations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.psychologist_specializations
    ADD CONSTRAINT psychologist_specializations_pkey PRIMARY KEY (id);


--
-- Name: reviews reviews_appointment_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_appointment_id_key UNIQUE (appointment_id);


--
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (id);


--
-- Name: specializations specializations_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.specializations
    ADD CONSTRAINT specializations_name_key UNIQUE (name);


--
-- Name: specializations specializations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.specializations
    ADD CONSTRAINT specializations_pkey PRIMARY KEY (id);


--
-- Name: specializations specializations_slug_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.specializations
    ADD CONSTRAINT specializations_slug_key UNIQUE (slug);


--
-- Name: time_slots time_slots_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.time_slots
    ADD CONSTRAINT time_slots_pkey PRIMARY KEY (id);


--
-- Name: time_slots time_slots_psychologist_id_date_start_time_b072a47a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.time_slots
    ADD CONSTRAINT time_slots_psychologist_id_date_start_time_b072a47a_uniq UNIQUE (psychologist_id, date, start_time);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users_groups users_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_pkey PRIMARY KEY (id);


--
-- Name: users_groups users_groups_user_id_group_id_fc7788e8_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_user_id_group_id_fc7788e8_uniq UNIQUE (user_id, group_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users_user_permissions users_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: users_user_permissions users_user_permissions_user_id_permission_id_3b86cbdf_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissions_user_id_permission_id_3b86cbdf_uniq UNIQUE (user_id, permission_id);


--
-- Name: appointments_client_id_ed088e20; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX appointments_client_id_ed088e20 ON public.appointments USING btree (client_id);


--
-- Name: appointments_psychologist_id_9e301a3d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX appointments_psychologist_id_9e301a3d ON public.appointments USING btree (psychologist_id);


--
-- Name: appointments_status_ff89895a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX appointments_status_ff89895a ON public.appointments USING btree (status);


--
-- Name: appointments_status_ff89895a_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX appointments_status_ff89895a_like ON public.appointments USING btree (status varchar_pattern_ops);


--
-- Name: appointments_time_slot_id_95fedf04; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX appointments_time_slot_id_95fedf04 ON public.appointments USING btree (time_slot_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: email_confirmation_tokens_code_3d08c5d2; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX email_confirmation_tokens_code_3d08c5d2 ON public.email_confirmation_tokens USING btree (code);


--
-- Name: email_confirmation_tokens_code_3d08c5d2_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX email_confirmation_tokens_code_3d08c5d2_like ON public.email_confirmation_tokens USING btree (code varchar_pattern_ops);


--
-- Name: email_confirmation_tokens_user_id_4f543bec; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX email_confirmation_tokens_user_id_4f543bec ON public.email_confirmation_tokens USING btree (user_id);


--
-- Name: notifications_user_id_468e288d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX notifications_user_id_468e288d ON public.notifications USING btree (user_id);


--
-- Name: psychologist_specializations_psychologist_id_4d69ac51; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX psychologist_specializations_psychologist_id_4d69ac51 ON public.psychologist_specializations USING btree (psychologist_id);


--
-- Name: psychologist_specializations_specialization_id_cb576c77; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX psychologist_specializations_specialization_id_cb576c77 ON public.psychologist_specializations USING btree (specialization_id);


--
-- Name: specializations_name_a9fe49f3_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX specializations_name_a9fe49f3_like ON public.specializations USING btree (name varchar_pattern_ops);


--
-- Name: specializations_slug_7284e6fc_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX specializations_slug_7284e6fc_like ON public.specializations USING btree (slug varchar_pattern_ops);


--
-- Name: time_slots_date_d554e2f9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX time_slots_date_d554e2f9 ON public.time_slots USING btree (date);


--
-- Name: time_slots_psychologist_id_93c87fbe; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX time_slots_psychologist_id_93c87fbe ON public.time_slots USING btree (psychologist_id);


--
-- Name: unique_active_appointment_per_time_slot; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX unique_active_appointment_per_time_slot ON public.appointments USING btree (time_slot_id) WHERE ((status)::text = ANY ((ARRAY['pending'::character varying, 'confirmed'::character varying])::text[]));


--
-- Name: users_email_0ea73cca_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_email_0ea73cca_like ON public.users USING btree (email varchar_pattern_ops);


--
-- Name: users_groups_group_id_2f3517aa; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_groups_group_id_2f3517aa ON public.users_groups USING btree (group_id);


--
-- Name: users_groups_user_id_f500bee5; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_groups_user_id_f500bee5 ON public.users_groups USING btree (user_id);


--
-- Name: users_user_permissions_permission_id_6d08dcd2; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_user_permissions_permission_id_6d08dcd2 ON public.users_user_permissions USING btree (permission_id);


--
-- Name: users_user_permissions_user_id_92473840; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_user_permissions_user_id_92473840 ON public.users_user_permissions USING btree (user_id);


--
-- Name: appointments appointments_client_id_ed088e20_fk_client_profiles_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_client_id_ed088e20_fk_client_profiles_id FOREIGN KEY (client_id) REFERENCES public.client_profiles(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: appointments appointments_psychologist_id_9e301a3d_fk_psycholog; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_psychologist_id_9e301a3d_fk_psycholog FOREIGN KEY (psychologist_id) REFERENCES public.psychologist_profiles(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: appointments appointments_time_slot_id_95fedf04_fk_time_slots_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_time_slot_id_95fedf04_fk_time_slots_id FOREIGN KEY (time_slot_id) REFERENCES public.time_slots(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: client_profiles client_profiles_user_id_2c51f42e_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.client_profiles
    ADD CONSTRAINT client_profiles_user_id_2c51f42e_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: email_confirmation_tokens email_confirmation_tokens_user_id_4f543bec_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_confirmation_tokens
    ADD CONSTRAINT email_confirmation_tokens_user_id_4f543bec_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notifications notifications_user_id_468e288d_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_468e288d_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: psychologist_profiles psychologist_profiles_user_id_2abb595a_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.psychologist_profiles
    ADD CONSTRAINT psychologist_profiles_user_id_2abb595a_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: psychologist_specializations psychologist_special_psychologist_id_4d69ac51_fk_psycholog; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.psychologist_specializations
    ADD CONSTRAINT psychologist_special_psychologist_id_4d69ac51_fk_psycholog FOREIGN KEY (psychologist_id) REFERENCES public.psychologist_profiles(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: psychologist_specializations psychologist_special_specialization_id_cb576c77_fk_specializ; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.psychologist_specializations
    ADD CONSTRAINT psychologist_special_specialization_id_cb576c77_fk_specializ FOREIGN KEY (specialization_id) REFERENCES public.specializations(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reviews reviews_appointment_id_9141b057_fk_appointments_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_appointment_id_9141b057_fk_appointments_id FOREIGN KEY (appointment_id) REFERENCES public.appointments(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: time_slots time_slots_psychologist_id_93c87fbe_fk_psychologist_profiles_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.time_slots
    ADD CONSTRAINT time_slots_psychologist_id_93c87fbe_fk_psychologist_profiles_id FOREIGN KEY (psychologist_id) REFERENCES public.psychologist_profiles(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_groups users_groups_group_id_2f3517aa_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_group_id_2f3517aa_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_groups users_groups_user_id_f500bee5_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_user_id_f500bee5_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_permissions users_user_permissio_permission_id_6d08dcd2_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissio_permission_id_6d08dcd2_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_permissions users_user_permissions_user_id_92473840_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissions_user_id_92473840_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

\unrestrict Xb8upjJT9ds9ApKlwaDh3QcjsxthaE59ZDi8XTAL0PZZy13C1gpyPXFP5NiezT3

