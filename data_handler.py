from time import time
import math
import connection


HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]


def get_questions_from_file():
    questions = get_mutable_list("sample_data/test_questions.csv")
    sorted_questions = sorted(questions, key=lambda x: int(x["submission_time"]), reverse=True)
    return sorted_questions


# util function
def get_mutable_list(filename):
    return [{key: item for key, item in dictionary.items()}
            for dictionary in connection.read_data_from_file(filename)]


def get_question_by_id(question_id):
    questions = get_mutable_list("sample_data/test_questions.csv")
    return filter_items_by_id(question_id, questions)[0]


# util
def filter_items_by_id(question_id, questions, question_or_answer="question"):
    id_to_check = "id" if question_or_answer == "question" else "question_id"
    return [question for question in questions if question[id_to_check] == question_id]


def get_answers_by_question_id(question_id):
    answers = get_mutable_list("sample_data/answer.csv")
    return filter_items_by_id(question_id, answers, "answers")


def add_form_data(form_data, filename="sample_data/test_questions.csv", question_id=None):
    mutable_form_data = get_data_from_form(form_data)
    data_to_write = connection.read_data_from_file(filename)
    add_missing_initial_values_to_question(mutable_form_data, data_to_write, question_id)
    data_to_write.append(mutable_form_data)
    headers = HEADERS if "question_id" not in data_to_write[0].keys() else ANSWER_HEADERS 
    connection.write_data_to_file(data_to_write, headers)


def generate_new_id(list_of_dicts):
    max_id = max([int(dict["id"]) for dict in list_of_dicts]) if list_of_dicts else 0
    return max_id +1


# refact. one line, rename
def get_data_from_form(form_data):
    form_dict = {key: value for key, value in form_data.items()}
    return form_dict


def add_missing_initial_values_to_question(new_data, data_list, question_id=None):
    new_data['id'] = generate_new_id(data_list)
    new_data["submission_time"] = int(math.ceil(time()))
    new_data["image"] = new_data["image"] if new_data.get("image") else ""
    new_data["vote_number"] = "0"
    if not question_id:
        new_data["view_number"] = "0"
    else:
        new_data["question_id"] = question_id


# tests
if __name__ == "__main__":
    print(get_answers_by_question_id("1"))
    print(get_question_by_id("3"))
    add_form_data({"title": "Title", "message": "This is the message"})


