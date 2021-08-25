import connection


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
