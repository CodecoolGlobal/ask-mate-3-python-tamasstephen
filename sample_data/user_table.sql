DROP TABLE IF EXISTS public.user_table;
CREATE TABLE user_table (user_id serial PRIMARY KEY NOT NULL,
    password text,
	user_name text,
	registration_date timestamp without time zone,
	asked_questions integer,
	number_of_answers integer,
	number_of_comments integer,
	reputation integer);

	
INSERT INTO user_table
    (password, user_name, registration_date)
    VALUES ('120sdafds213123', 'gabi@gabi.com', '2021-11-11 04:05:06');