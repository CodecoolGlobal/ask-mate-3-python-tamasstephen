import connection
from psycopg2 import sql


@connection.connection_handler
def add_comment_to_question_db(cursor, question_id, message, submission_time):
    query = """
        INSERT INTO comment
        ("question_id", "message", "submission_time")
        VALUES (%(question_id)s, %(message)s, %(submission_time)s)
    """
    cursor.execute(query, {"question_id": question_id,
                           "message": message,
                           "submission_time": submission_time})


@connection.connection_handler
def get_comments(cursor, column, item_id):
    query = """
        SELECT * FROM comment
        WHERE {column} = {item_id}
    """
    cursor.execute(sql.SQL(query).format(column=sql.Identifier(column),
                                         item_id=sql.Literal(item_id)))
    return cursor.fetchall()
