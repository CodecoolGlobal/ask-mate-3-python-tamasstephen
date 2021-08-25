from time import time
import math
import connection
import util
import os
from datetime import datetime
from psycopg2 import sql


HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
QUESTION_HEADERS_TO_PRINT = ["Submission time", "View number", "Vote number", "Title", "Message", "Image Path"]
ALLOWED_FILES = [".jpg", ".png"]
UPLOAD_FOLDER = ["./images/questions", "./images/answers"]


def valid_file_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_FILES


def get_questions_from_file(sorting_rule="submission_time_desc"):
    questions = util.get_mutable_list()
    if not questions:
        return None
    sorted_questions = util.sort_questions(questions, sorting_rule)
    # util.convert_questions_secs_to_date(sorted_questions)
    return sorted_questions


@connection.connection_handler
def get_answers_by_question_id(cursor, question_id):
    query = """
        SELECT * FROM answer
        WHERE question_id = %(question_id)s 
    """
    cursor.execute(query, {"question_id": question_id})
    return cursor.fetchall()


@connection.connection_handler
def update_answer(cursor, answer_id, message):
    query="""
    UPDATE answer
    SET message = %(message)s
    WHERE id = %(answer_id)s
    """
    cursor.execute(query, {"message": message,
                           "answer_id": answer_id})


@connection.connection_handler
def get_answer_by_answer_id(cursor, answer_id):
    query = """
        SELECT * FROM answer
        WHERE id = %(answer_id)s 
    """
    cursor.execute(query, {"answer_id": answer_id})
    return cursor.fetchall()


def add_question(form_data, question_id=None, image_name=None):
    mutable_form_data = get_data_from_form(form_data)
    add_missing_initial_values_to_question(mutable_form_data, image_name, question_id)
    add_question_to_db(mutable_form_data)


def add_new_answer(form_data, question_id, image_name=None):
    mutable_form_data = get_data_from_form(form_data)
    add_missing_initial_values_to_question(mutable_form_data, image_name, question_id)
    add_answer_to_db(mutable_form_data)


@connection.connection_handler
def add_answer_to_db(cursor, answer):
    query = """
        INSERT INTO answer
        (submission_time, vote_number, question_id, message, image)
        VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s)
    """
    cursor.execute(query, {"submission_time": answer["submission_time"],
                           "vote_number": answer["vote_number"],
                           "question_id": answer["question_id"],
                           "message": answer["message"],
                           "image": answer["image"]})


@connection.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    query = """
        SELECT question_id FROM answer
        WHERE id = %(answer_id)s
    """
    cursor.execute(query, {"answer_id": answer_id})
    return cursor.fetchall()


@connection.connection_handler
def add_question_to_db(cursor, question):
    query = """
        INSERT INTO question
        (submission_time, view_number, vote_number, title, message, image)
        VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s)
    """
    cursor.execute(query, {"submission_time": question["submission_time"],
                           "view_number": question["view_number"],
                           "vote_number": question["vote_number"],
                           "title": question["title"],
                           "message": question["message"],
                           "image": question["image"]})


def get_data_from_form(form_data):
    form_dict = {key: value for key, value in form_data.items()}
    return form_dict


def add_missing_initial_values_to_question(new_data, image_name, question_id=None):
    new_data["submission_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data["image"] = f"{UPLOAD_FOLDER[0] if not question_id else UPLOAD_FOLDER[1]}/{image_name}" if image_name else ""
    new_data["vote_number"] = "0"
    if not question_id:
        new_data["view_number"] = "0"
    else:
        new_data["question_id"] = question_id


@connection.connection_handler
def update_question(cursor, question_id, form_data):
    query = """
        UPDATE question
        SET message = %(message)s,
            title = %(title)s
        WHERE id = %(question_id)s
    """
    cursor.execute(query, {"message": form_data["message"],
                           "title": form_data["title"],
                           "question_id": question_id})


@connection.connection_handler
def count_views(cursor, question_id):
    question_id = int(question_id)
    query = """
        UPDATE question
        SET view_number = view_number + 1
        WHERE id = %(question_id)s
    """
    cursor.execute(query, {"question_id": question_id})


# delete?
def delete_item(item_id, headers, filename):
    questions = util.get_mutable_list(filename)
    question_index = [index for index, question in enumerate(questions) if question['id'] == item_id][0]
    if questions[question_index]["image"]:
        os.remove(questions[question_index]["image"])
    questions.pop(question_index)
    connection.write_data_to_file(questions, headers, filename)


def delete_all_answers(question_id):
    answers_by_question = get_answers_by_question_id(question_id)
    for answer in answers_by_question:
        util.delete_item_by_id(answer["id"], "answer")


def handle_votes(item_id, vote, table="question"):
    print(item_id, "fuck")
    vote_count = 1 if vote == "vote_up" else -1
    handle_db_votes(table, vote_count, item_id)


@connection.connection_handler
def handle_db_votes(cursor, table, vote, item_id):
    query = """
        UPDATE {table}
        SET vote_number = vote_number + {vote}
        WHERE id = {item_id}
    """
    cursor.execute(sql.SQL(query).format(table=sql.Identifier(table),
                                         vote=sql.Literal(vote),
                                         item_id=sql.Literal(item_id)))


