import connection
import util
from flask import Markup
from string import ascii_lowercase


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
    return filtered_questions


def highlight_msg(msg, phrase):
    coordinates = get_search_coordinates(phrase, msg)
    return insert_highlight_tags_to_text(coordinates, msg)


def get_search_coordinates(phrase, expression):
    phrase_list = phrase.split()
    expression_list = expression.split()
    coordinates = []
    for index, word in enumerate(expression_list):
        if remove_special_characters(word.lower()) == remove_special_characters(phrase_list[0].lower()):
            if remove_special_characters("".join(expression_list[index:index+len(phrase_list)]).lower()) == remove_special_characters("".join(phrase_list)):
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


def remove_special_characters(text):
    raw_text = "".join([letter for letter in list(text) if letter in ascii_lowercase])
    return raw_text


@connection.connection_handler
def get_all_answers(cursor):
    query = """
        SELECT * FROM answer 
    """
    cursor.execute(query)
    return cursor.fetchall()
