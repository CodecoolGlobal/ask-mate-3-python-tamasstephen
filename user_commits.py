import connection
from psycopg2 import sql


def bind_user_to_question(user_id):
    handle_new_message(user_id, "question_id", "question", "question_to_user")
    handle_user_attributes("asked_questions", user_id)


def handle_new_message(user_id, column, message_table, connection_table):
    message_id = get_last_id_from_table(message_table)[0]['id']
    connect_user_to_id(user_id, column, message_id, connection_table)


@connection.connection_handler
def handle_user_attributes(cursor, column, user_id):
    query = """
        UPDATE user_table
        SET {column} = COALESCE(asked_questions, 0) + 1
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
