from time import time
import math
import connection
import util
import os


HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
QUESTION_HEADERS_TO_PRINT = ["Submission time", "View number", "Vote number", "Title", "Message", "Image Path"]
ALLOWED_FILES = [".jpg", ".png"]
UPLOAD_FOLDER = ["./images/questions", "./images/answers"]


def valid_file_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_FILES


def get_questions_from_file(sorting_rule="submission_time_desc"):
    questions = get_mutable_list("sample_data/test_questions.csv")
    if not questions:
        return None
    sorted_questions = util.sort_questions(questions, sorting_rule)
    util.convert_questions_secs_to_date(sorted_questions)
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
    answers = get_mutable_list("sample_data/test_answers.csv")
    return filter_items_by_id(question_id, answers, "test_answers")


def add_form_data(form_data, filename="sample_data/test_questions.csv", question_id=None, image_name=None):
    mutable_form_data = get_data_from_form(form_data)
    data_to_write = connection.read_data_from_file(filename)
    add_missing_initial_values_to_question(mutable_form_data, data_to_write, image_name, question_id)
    data_to_write.append(mutable_form_data)
    connection.write_data_to_file(data_to_write, get_header(data_to_write[0]), filename)


def get_header(dictionary):
    return HEADERS if "question_id" not in dictionary.keys() else ANSWER_HEADERS


def generate_new_id(list_of_dicts):
    max_id = max([int(dict["id"]) for dict in list_of_dicts]) if list_of_dicts else 0
    return max_id + 1


# refact. one line, rename
def get_data_from_form(form_data):
    form_dict = {key: value for key, value in form_data.items()}
    return form_dict


def add_missing_initial_values_to_question(new_data, data_list, image_name, question_id=None):
    new_data['id'] = generate_new_id(data_list)
    new_data["submission_time"] = int(math.ceil(time()))
    new_data["image"] = f"{UPLOAD_FOLDER[0] if not question_id else UPLOAD_FOLDER[1]}/{image_name}" if image_name else ""
    new_data["vote_number"] = "0"
    if not question_id:
        new_data["view_number"] = "0"
    else:
        new_data["question_id"] = question_id


def count_views(question_id):
    question = get_question_by_id(question_id)
    # should be a function -> readable 
    question['view_number'] = str(int(question['view_number']) + 1)
    questions = connection.read_data_from_file()
    question_index = [index for index, value in enumerate(questions) if value['id'] == question_id][0]
    questions[question_index] = question
    connection.write_data_to_file(questions, HEADERS)


def delete_item(item_id, headers, filename):
    questions = get_mutable_list(filename)
    question_index = [index for index, question in enumerate(questions) if question['id'] == item_id][0]
    if questions[question_index]["image"]:
        os.remove(questions[question_index]["image"])
    questions.pop(question_index)
    connection.write_data_to_file(questions, headers, filename)


def delete_answer(answer_id, answer_headers, filename):
    answers = get_mutable_list(filename)
    filtered_answers = [answer for answer in answers if answer['id'] != answer_id]
    connection.write_data_to_file(filtered_answers, answer_headers, filename)
    question_index = [index for index, question in enumerate(questions) if question['id'] == item_id][0]
    os.remove(questions[question_index]["image"])
    questions.pop(question_index)
    connection.write_data_to_file(questions, headers, filename)


def delete_all_answers(question_id):
    answers_by_question = get_answers_by_question_id(question_id)
    for anwer in answers_by_question:
        delete_item(anwer['id'], ANSWER_HEADERS, "sample_data/test_answers.csv")


def update_question(question_id, form_data):
    question = get_question_by_id(question_id)
    question["message"] = form_data["message"] 
    question["title"] = form_data["title"]
    questions = get_updated_questions(question_id, question)
    connection.write_data_to_file(questions, HEADERS)


def get_updated_questions(question_id, question):
    questions = connection.read_data_from_file()
    question_index = [index for index, current_question in enumerate(questions) 
                      if current_question["id"] == question_id][0]
    questions[question_index] = question
    return questions


