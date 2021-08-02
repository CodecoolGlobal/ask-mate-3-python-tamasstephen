# from datetime import datetime
import connection

HEADERS = ["id", "submission_time", "title", "message"]
ANSWER_HEADERS = ["id", "submission_time", "message"]


def get_questions_from_file():
    questions = get_mutable_list("sample_data/question.csv")
    sorted_questions = sorted(questions, key=lambda x: int(x["submission_time"]), reverse=True)
    return sorted_questions


# util function
def get_mutable_list(filename):
    return [{key: item for key, item in dictionary.items() if key in HEADERS} 
            for dictionary in connection.read_data_from_file(filename)]


def get_question_by_id(question_id):
    questions = get_mutable_list("sample_data/question.csv")
    return filter_items_by_id(question_id, questions)[0]


# util
def filter_items_by_id(question_id, questions):
    return [question for question in questions if question["id"] == question_id]


def get_answer_by_question_id(question_id): 
    answers = get_mutable_list("sample_data/answer.csv")
    return filter_items_by_id(question_id, answers)


if __name__ == "__main__":
    print(get_answer_by_question_id("2"))
    print(get_question_by_id("3"))
