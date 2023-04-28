

--
-- TOC entry 3741 (class 0 OID 68178)
-- Dependencies: 212
-- Data for Name: about_aboutpage; Type: TABLE DATA; Schema: public; Owner: bsadmin
--

COPY public.about_aboutpage (id, intro_text, ending_text_1, ending_text_2) FROM stdin;
1	Besound is a non-profit app aiming to bring you the richness of experimenting with sound and sharing it with the world	For safety reasons, only registered users can post sounds. That helps us track any abusive content. Your personal data will be stored safely.	Becoming a member is and will always remain free for everybody
\.


--
-- TOC entry 3743 (class 0 OID 68186)
-- Dependencies: 214
-- Data for Name: about_step; Type: TABLE DATA; Schema: public; Owner: bsadmin
--

COPY public.about_step (id, text, image, page_id) FROM stdin;
1	To record a sound,\r\npress the red circle	circle.svg	1
2	While it’s filled,\r\nrecording is taking place, \r\npress again to stop recording	circle-active.svg	1
3	Add an effect\r\nor leave it as it is	effects.svg	1
4	Remember, all the posts \r\nare completely anonymous <3		1
\.


--
-- TOC entry 3757 (class 0 OID 68270)
-- Dependencies: 228
-- Data for Name: custom_users_customuser; Type: TABLE DATA; Schema: public; Owner: bsadmin
--

COPY public.custom_users_customuser (id, password, last_login, is_superuser, is_staff, is_active, date_joined, first_name, last_name, birth_date, nationality, email) FROM stdin;
3	pbkdf2_sha256$600000$DEDkwo2SDij5emC35t7vub$rQLCeL23HF6JLu/sGf3LnyF4VLXXiSzXJnBFMO114MM=	2023-04-23 01:30:38.547713+02	t	t	t	2023-04-23 01:30:05.585568+02	Elsa	de Alfonso	1984-04-15	Spanish	elsa.de.alfonso@gmail.com
9	pbkdf2_sha256$600000$2DRucwDK05elnUpjmjuTbh$RcWoW7sihPmQKUQiH7W4QRXVAN0FiTZGTYhRG2mEOQ0=	\N	f	f	t	2023-04-23 01:53:27.884869+02	Elsa	de Alfonso	2023-04-22	Raval	elsa@maneko.es
10	pbkdf2_sha256$600000$xFeBBNvN1v5vOg7KuAXlJE$7I8AssOSpt3iL3xf5c8jjjh61uiUs6F7A1hpCPEQPXI=	\N	f	f	t	2023-04-23 01:53:59.681883+02	Sé	No	2023-04-21	Alaska	edealfonso@uoc.edu
\.



--
-- TOC entry 3753 (class 0 OID 68254)
-- Dependencies: 224
-- Data for Name: custom_users_loginpage; Type: TABLE DATA; Schema: public; Owner: bsadmin
--

COPY public.custom_users_loginpage (id, instruction, button) FROM stdin;
1	enter your login data	Log in
\.


--
-- TOC entry 3755 (class 0 OID 68262)
-- Dependencies: 226
-- Data for Name: custom_users_signuppage; Type: TABLE DATA; Schema: public; Owner: bsadmin
--

COPY public.custom_users_signuppage (id, text_1, text_2, button_login, text_3, text_4, button_end, confirmation_post, confirmation_pre) FROM stdin;
1	you have to be logged in \r\nto record sounds	already registered?	Log in	to sign up, \r\nenter your contact details	set your login data	Sign up	has been \r\nsuccessfully created	your email
\.


--
-- TOC entry 3765 (class 0 OID 68345)
-- Dependencies: 236
-- Data for Name: home_homepage; Type: TABLE DATA; Schema: public; Owner: bsadmin
--

COPY public.home_homepage (id, logo, motto, instruction, error_not_found) FROM stdin;
1	logo.svg	Sound experiences to share	tap to hear	Sound not found :),\r\nit might have expired
\.


--
-- TOC entry 3767 (class 0 OID 68353)
-- Dependencies: 238
-- Data for Name: posts_effect; Type: TABLE DATA; Schema: public; Owner: bsadmin
--

COPY public.posts_effect (id, name, slug, the_order) FROM stdin;
1	noeffect	noeffect	0
2	crazy	crazy	2
3	cave	cave	1
\.


--
-- TOC entry 3771 (class 0 OID 68369)
-- Dependencies: 242
-- Data for Name: posts_post; Type: TABLE DATA; Schema: public; Owner: bsadmin
--

COPY public.posts_post (id, name, slug, audio, effect_id) FROM stdin;
1	doh	doh	audio/invalid_keypress.mp3	1
2	misteryviolin	misteryviolin	audio/snippets07.mp3	3
3	ambientsounds	ambientsounds	audio/background01.mp3	3
4	ryainairsucks	ryainairsucks	audio/When_Ryanair_has_landed_Funny.mp3	2
\.


--
-- TOC entry 3769 (class 0 OID 68361)
-- Dependencies: 240
-- Data for Name: posts_recordpage; Type: TABLE DATA; Schema: public; Owner: bsadmin
--

COPY public.posts_recordpage (id, phase1_instruction, phase2_instruction, phase3_instruction, phase3_back, phase3_forward, phase4_instruction, phase4_back, phase4_forward, confirmation_pre_name, confirmation_post_name, confirmation_regret, confirmation_remember, error_text_1, error_text_2, error_back, error_forward, success) FROM stdin;
1	<p>press circle to <strong>start</strong> recording</p>	<p>press circle to <strong>stop</strong> recording</p>	<p>choose an <strong>effect</strong></p>	Start again	OK	<p>give your sound a <strong>name</strong></p>	Go back	Share!	your sound	has been\r\nsuccessfully posted	I regret all this!\r\nPlease remove the post	Remember, all the posts \r\nare completely anonymous <3	Are you sure?	This action will permanently\r\nerase all audio recordings	Take me back	Accept	your sound has been\r\nsuccessfully deleted
\.


--
-- TOC entry 3778 (class 0 OID 0)
-- Dependencies: 211
-- Name: about_aboutpage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bsadmin
--

SELECT pg_catalog.setval('public.about_aboutpage_id_seq', 1, false);


--
-- TOC entry 3779 (class 0 OID 0)
-- Dependencies: 213
-- Name: about_step_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bsadmin
--

SELECT pg_catalog.setval('public.about_step_id_seq', 4, true);


--
-- TOC entry 3784 (class 0 OID 0)
-- Dependencies: 227
-- Name: custom_users_customuser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bsadmin
--

SELECT pg_catalog.setval('public.custom_users_customuser_id_seq', 10, true);


--
-- TOC entry 3786 (class 0 OID 0)
-- Dependencies: 223
-- Name: custom_users_loginpage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bsadmin
--

SELECT pg_catalog.setval('public.custom_users_loginpage_id_seq', 1, false);


--
-- TOC entry 3787 (class 0 OID 0)
-- Dependencies: 225
-- Name: custom_users_signuppage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bsadmin
--

SELECT pg_catalog.setval('public.custom_users_signuppage_id_seq', 1, false);


--
--
-- TOC entry 3791 (class 0 OID 0)
-- Dependencies: 235
-- Name: home_homepage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bsadmin
--

SELECT pg_catalog.setval('public.home_homepage_id_seq', 1, false);


--
-- TOC entry 3792 (class 0 OID 0)
-- Dependencies: 237
-- Name: posts_effect_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bsadmin
--

SELECT pg_catalog.setval('public.posts_effect_id_seq', 3, true);


--
-- TOC entry 3793 (class 0 OID 0)
-- Dependencies: 241
-- Name: posts_post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bsadmin
--

SELECT pg_catalog.setval('public.posts_post_id_seq', 4, true);


--
-- TOC entry 3794 (class 0 OID 0)
-- Dependencies: 239
-- Name: posts_recordpage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bsadmin
--

SELECT pg_catalog.setval('public.posts_recordpage_id_seq', 1, false);

