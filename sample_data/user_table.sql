DROP TABLE IF EXISTS public.user_table;
CREATE TABLE user_table (user_id serial PRIMARY KEY NOT NULL,
    password text,
	user_name VARCHAR UNIQUE,
	registration_date timestamp without time zone,
	asked_questions integer,
	number_of_answers integer,
	number_of_comments integer,
	reputation integer);
