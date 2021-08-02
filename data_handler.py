from time import time
import math
import connection

HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADERS = ["id", "submission_time","question_id", "message"]

def get_questions_from_file():
    questions = get_mutable_list("sample_data/test_questions.csv")
    sorted_questions = sorted(questions, key=lambda x: int(x["submission_time"]), reverse=True)
    return sorted_questions


# util function
# TODO: need to get rid of HEADERS condition if we extend the program
def get_mutable_list(filename):
    return [{key: item for key, item in dictionary.items() if key in HEADERS}
            for dictionary in connection.read_data_from_file(filename)]


def get_question_by_id(question_id):
    questions = get_mutable_list("sample_data/test_questions.csv")
    return filter_items_by_id(question_id, questions)[0]


# util
def filter_items_by_id(question_id, questions):
    return [question for question in questions if question["id"] == question_id]


def get_answer_by_question_id(question_id):
    answers = get_mutable_list("sample_data/answer.csv")
    return filter_items_by_id(question_id, answers)


def add_question(form_data):
    question_with_id_and_time = generate_question_dict(form_data)
    questions = connection.read_data_from_file("sample_data/test_questions.csv")
    questions.append(question_with_id_and_time)
    connection.write_data_to_file(questions, HEADERS)


def generate_new_id():
    return


def generate_question_dict(form_data):
    question_dict = {key: value for key, value in form_data.items()}
    add_missing_initial_values_to_question(question_dict)
    return question_dict


# TODO: provide id generator fn
def add_missing_initial_values_to_question(question):
    question['id'] = "4"
    question["submission_time"] = int(math.ceil(time()))
    question["image"] = question["image"] if question.get("image") else ""
    question["view_number"] = "0"
    question["vote_number"] = "0"


if __name__ == "__main__":
    print(get_answer_by_question_id("2"))
    print(get_question_by_id("3"))
    add_question({"title": "Title", "message": "This is the message"})
    


