import connection
from psycopg2 import sql


def handle_new_message(user_id, column, message_table, connection_table):
    message_id = get_id_from_messages(message_table)[0]['id']
    print(message_id)
    print(user_id)
    connect_user_to_id(user_id, column, message_id, connection_table)


@connection.connection_handler
def get_id_from_messages(cursor, table):
    query = """
    SELECT id FROM {table}
    ORDER BY id DESC
    LIMIT 1
    """
    cursor.execute(sql.SQL(query).format(table = sql.Identifier(table)))
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
