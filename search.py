import connection
import util
from flask import Markup


def get_items_with_phrase(phrase):
    phrase = phrase.lower()
    questions = util.get_all_question()
    answers_question_id_s = [item["question_id"] for item in get_all_answers()
                             if phrase in item["message"].lower()]
    filtered_questions = [item for item in questions
                          if phrase in item["message"].lower() or
                          phrase in item["title"].lower() or
                          item["id"] in answers_question_id_s]
    print(filtered_questions)
    return filtered_questions


def get_search_coordinates(phrase, expression):
    phrase_list = phrase.split()
    expression_list = expression.split()
    coordinates = []
    current = 0
    counter = 0
    is_running = True
    for word in expression_list:
        if word.lower() == phrase_list[counter]:
            while is_running:
                if word.lower() == phrase_list[counter]:
                    counter += 1
                    if counter == len(phrase_list):
                        coordinates.append((current, current + counter))
                        is_running = False
                    else:
                        counter += 1
        else:
            counter = 0
            current += 1
            is_running = True



@connection.connection_handler
def get_all_answers(cursor):
    query = """
        SELECT * FROM answer 
    """
    cursor.execute(query)
    return cursor.fetchall()
