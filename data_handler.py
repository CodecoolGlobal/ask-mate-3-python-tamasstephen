# from datetime import datetime
import connection

HEADERS = ["id", "submission_time", "title", "message"]


def get_questions_from_file():
    questions = [{key: item for key, item in dictionary.items() if key in HEADERS} 
                  for dictionary in connection.read_data_from_file()]
    return questions
