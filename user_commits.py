import connection
from psycopg2 import sql

import util
import data_handler


def bind_user_to_message(data_dict):
    msg_id, msg_column, msg_table, connection_table, usr_table = (data_dict["id"],
                                                                  data_dict["bind_column"],
                                                                  data_dict["message_table"],
                                                                  data_dict["connection_table"],
                                                                  data_dict["user_table_column"])
    handle_new_message(msg_id, msg_column, msg_table, connection_table)
    handle_user_attributes(usr_table, msg_id)


def handle_new_message(user_id, column, message_table, connection_table):
    message_id = get_last_id_from_table(message_table)[0]['id']
    connect_user_to_id(user_id, column, message_id, connection_table)


@connection.connection_handler
def handle_user_attributes(cursor, column, user_id):
    query = """
        UPDATE user_table
        SET {column} = COALESCE({column}, 0) + 1
        WHERE user_id = {user_id}
    """
    cursor.execute(sql.SQL(query).format(column=sql.Identifier(column),
                                         user_id=sql.Literal(user_id)))


@connection.connection_handler
def get_last_id_from_table(cursor, table):
    query = """
        SELECT id FROM {table}
        ORDER BY id DESC
        LIMIT 1
    """
    cursor.execute(sql.SQL(query).format(table=sql.Identifier(table)))
    return cursor.fetchall()


@connection.connection_handler
def connect_user_to_id(cursor, user_id, column, message_id, table):
    query = """
    INSERT INTO {table}
    (user_id, {column})
    VALUES ({user_id}, {message_id})
    """
    cursor.execute(sql.SQL(query).format(table=sql.Identifier(table),
                                         column=sql.Identifier(column),
                                         user_id=sql.Literal(user_id),
                                         message_id=sql.Literal(message_id)))


def get_questions_by_user_id(user_id):
    question_ids = get_message_ids(user_id, "question_id", "question_to_user")
    return get_elements_from_db_by_id("question_id", "question", question_ids)


def get_answer_dict_by_question_id(question_ids):
    answers = {id_dict['question_id']: data_handler.get_answers_by_question_id(id_dict['question_id'])
               for id_dict in question_ids}
    return answers


def get_answers_by_user_id(user_id):
    answer_ids = get_message_ids(user_id, "answer_id", "answer_to_user")
    return get_elements_from_db_by_id("answer_id", "answer", answer_ids)


def get_comments_by_user_id(user_id):
    comment_ids = get_message_ids(user_id, "comment_id", "comment_to_user")
    return get_elements_from_db_by_id("comment_id", "comment", comment_ids)


def get_elements_from_db_by_id(key, table, dictionary):
    return [util.get_data_by_id(answer_id[key], table)[0] for answer_id in dictionary]


@connection.connection_handler
def get_user_data_by_user_id(cursor, user_id):
    print(user_id)
    query = """
        SELECT * FROM user_table
        WHERE user_id = {user_id} 
    """
    cursor.execute(sql.SQL(query).format(user_id=sql.Literal(user_id)))
    return cursor.fetchall()


@connection.connection_handler
def get_message_ids(cursor, user_id, column, table):
    query = """
        SELECT {column} FROM {table}
        WHERE user_id = {user_id} 
    """
    cursor.execute(sql.SQL(query).format(column=sql.Identifier(column),
                                         table=sql.Identifier(table),
                                         user_id=sql.Literal(user_id)))
    return cursor.fetchall()
