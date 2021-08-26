import connection
import util


def get_items_with_phrase(phrase):
    phrase = phrase.lower()
    questions = util.get_all_question()
    answers_question_id_s = [item["question_id"] for item in get_all_answers()
                             if phrase in item["message"].lower()]
    filtered_questions = [item for item in questions
                          if phrase in item["message"].lower() or
                          phrase in item["title"].lower() or
                          item["id"] in answers_question_id_s]
    print(filtered_questions)
    return filtered_questions


@connection.connection_handler
def get_all_answers(cursor):
    query = """
        SELECT * FROM answer 
    """
    cursor.execute(query)
    return cursor.fetchall()
