import unittest
import connection
import os

import data_handler
import search

PHRASE = "It is what it is"

test = unittest.TestCase()
username = os.environ.get("PSQL_USERNAME")
host = os.environ.get("PSQL_HOST")
password = os.environ.get("PSQL_PASSWORD")
db_name = os.environ.get("PSQL_DB_NAME")

test.assertEqual(connection.get_connection_string(), f"postgresql://{username}:{password}@{host}/{db_name}")
test.assertEqual(data_handler.get_answers_by_question_id(1)[0]["id"], 1)

test.assertEqual(search.get_items_with_phrase("list")[0]["title"], "Wordpress loading multiple jQuery Versions")

test.assertEqual(search.get_search_coordinates("it", PHRASE), [(0, 1), (3, 4)])
test.assertEqual(search.insert_highlight_tags_to_text([(0, 1), (3, 4)], PHRASE), "<span class='search_highlight'>It </span>is what <span class='search_highlight'>it </span>is")