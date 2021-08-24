from datetime import datetime
import connection
from psycopg2 import sql



def sort_questions(questions, sort_key="submission_time_desc"):
    sort_by_key = {
            "submission_time": sorted(questions, key=lambda x: x["submission_time"], reverse=False),
            "submission_time_desc": sorted(questions, key=lambda x: x["submission_time"], reverse=True),
            "vote_number": sorted(questions, key=lambda x: int(x["vote_number"])),
            "vote_number_desc": sorted(questions, key=lambda x: int(x["vote_number"]), reverse=True),
            "view_number": sorted(questions, key=lambda x: int(x["view_number"])),
            "view_number_desc": sorted(questions, key=lambda x: int(x["view_number"]), reverse=True),
            "title": sorted(questions, key=lambda x: x["title"]),
            "title_desc": sorted(questions, key=lambda x: x["title"], reverse=True),
            "message": sorted(questions, key=lambda x: x["message"]),
            "message_desc": sorted(questions, key=lambda x: x["message"], reverse=True)
            }
    return sort_by_key[sort_key]


def convert_secs_to_date(dictionary):
    dictionary["submission_time"] = datetime.fromtimestamp(int(dictionary["submission_time"]))


def convert_questions_secs_to_date(questions):
    for question in questions:
        question["submission_time"] = datetime.fromtimestamp(int(question["submission_time"]))


def get_mutable_list():
    return [{key: item for key, item in dictionary.items()}
            for dictionary in get_all_question()]


def get_updated_questions(question_id, question, filename="sample_data/test_questions.csv"):
    questions = connection.read_data_from_file(filename)
    question_index = [index for index, current_question in enumerate(questions) 
                      if current_question["id"] == question_id][0]
    questions[question_index] = question
    return questions


@connection.connection_handler
def get_all_question(cursor):
    query = """
        SELECT * FROM question
    """
    cursor.execute(query)
    data = cursor.fetchall()
    return data


@connection.connection_handler
def get_data_by_id(cursor, item_id, table_name):
    query = """
        SELECT * FROM {table_name}
        WHERE id = {item_id}
    """
    cursor.execute(sql.SQL(query).format(table_name=sql.Identifier(table_name),
                                         item_id=sql.Literal(item_id)))
    return cursor.fetchall()
