DROP TABLE IF EXISTS answer_to_user;
CREATE TABLE answer_to_user(id serial PRIMARY KEY NOT NULL,
				user_id integer NOT NULL,
				answer_id integer NOT NULL,
				FOREIGN KEY (user_id)
					REFERENCES user_table (user_id)
                    ON DELETE CASCADE,
				FOREIGN KEY (answer_id)
					REFERENCES answer (id)
                    ON DELETE CASCADE);


DROP TABLE IF EXISTS comment_to_user;
CREATE TABLE comment_to_user(id serial PRIMARY KEY NOT NULL,
				user_id integer NOT NULL,
				comment_id integer NOT NULL,
				FOREIGN KEY (user_id)
					REFERENCES user_table (user_id)
                    ON DELETE CASCADE,
				FOREIGN KEY (comment_id)
					REFERENCES comment (id)
					ON DELETE CASCADE);
