DROP TABLE IF EXISTS question_to_user;
CREATE TABLE quelstion_to_user(id serial PRIMARY KEY NOT NULL,
				user_id integer NOT NULL,
				question_id integer NOT NULL,
				FOREIGN KEY (user_id)
					REFERENCES user_table (user_id),
				FOREIGN KEY (question_id)
					REFERENCES question (id));
