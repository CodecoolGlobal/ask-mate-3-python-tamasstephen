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
    for question in filtered_questions:
        question["message"] = highlight_msg(question["message"], phrase)
        question["title"] = highlight_msg(question["title"], phrase)
    print(filtered_questions)
    return filtered_questions


def highlight_msg(msg, phrase):
    coordinates = get_search_coordinates(phrase, msg)
    return insert_highlight_tags_to_text(coordinates, msg)


def get_search_coordinates(phrase, expression):
    phrase_list = phrase.split()
    expression_list = expression.split()
    coordinates = []
    for index, word in enumerate(expression_list):
        if word.lower() == phrase_list[0].lower():
            if "".join(expression_list[index:index+len(phrase_list)]).lower() == "".join(phrase_list):
                coordinates.append((index, index+len(phrase_list)))
    return coordinates


def insert_highlight_tags_to_text(coordinates, text):
    if not coordinates:
        return text
    text_list = text.split()
    for coordinate in coordinates:
        text_list[coordinate[0]] = f"<span class='search_highlight'>{text_list[coordinate[0]]}"
        text_list[coordinate[1]-1] = f"{text_list[coordinate[1]-1]}</span>"
    return Markup(" ".join(text_list))


@connection.connection_handler
def get_all_answers(cursor):
    query = """
        SELECT * FROM answer 
    """
    cursor.execute(query)
    return cursor.fetchall()
