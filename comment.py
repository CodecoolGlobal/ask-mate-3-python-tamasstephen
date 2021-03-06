import connection
from psycopg2 import sql
import data_handler
import user_commits


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


@connection.connection_handler
def add_comment_to_answer_db(cursor, answer_id, message, submission_time):
    query = """
       INSERT INTO comment
       ("answer_id", "message", "submission_time")
       VALUES
       (%(answer_id)s, %(message)s, %(submission_time)s) 
    """
    cursor.execute(query, {"answer_id": answer_id,
                           "message": message,
                           "submission_time": submission_time})


@connection.connection_handler
def get_comment_by_comment_id(cursor, comment_id):
    query = """
        SELECT * from comment
        WHERE id = %(comment_id)s
    """
    cursor.execute(query, {"comment_id": comment_id})
    return cursor.fetchall()


@connection.connection_handler
def update_comment(cursor, comment_id, message, submission_time, comment_mod):
    query = """
    UPDATE comment
    SET message = %(message)s,
        submission_time = %(submission_time)s,
        edited_count = %(comment_mod)s
    WHERE id = %(comment_id)s
    """
    cursor.execute(query, {"comment_id": comment_id,
                           "message": message,
                           "submission_time": submission_time,
                           "comment_mod": comment_mod})


def get_question_id_by_comment_id(comment_id):
    comment = get_comment_by_comment_id(comment_id)[0]
    if comment.get("question_id"):
        return comment["question_id"]
    question_id = data_handler.get_question_id_by_answer_id(comment["answer_id"])[0]["question_id"]
    return question_id


@connection.connection_handler
def delete_comment_by_comment_id(cursor, comment_id):
    query = '''
    DELETE from comment
    WHERE id = %(comment_id)s
    '''
    cursor.execute(query, {"comment_id": comment_id})


def bind_comments_to_user(user_id):
    bind_dict = {"id": user_id,
                 "bind_column": "comment_id",
                 "message_table": "comment",
                 "connection_table": "comment_to_user",
                 "user_table_column": "number_of_comments"}
    user_commits.bind_user_to_message(bind_dict)
