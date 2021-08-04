from datetime import datetime
import connection


def sort_questions(questions, sort_key="submission_time_desc"):
    sort_by_key = {
            "submission_time": sorted(questions, key=lambda x: int(x["submission_time"]), reverse=False),
            "submission_time_desc": sorted(questions, key=lambda x: int(x["submission_time"]), reverse=True),
            "vote_number": sorted(questions, key=lambda x: int(x["vote_number"])),
            "vote_number_desc": sorted(questions, key=lambda x: int(x["vote_number"]), reverse=True),
            "view_number": sorted(questions, key=lambda x: int(x["view_number"])),
            "view_number_desc": sorted(questions, key=lambda x: int(x["view_number"]), reverse=True),
            "title": sorted(questions, key=lambda x: x["title"]),
            "title_desc": sorted(questions, key=lambda x: x["title"], reverse=True),
            "message": sorted(questions, key=lambda x: x["message"]),
            "message_desc": sorted(questions, key=lambda x: x["message"], reverse=True)
            }
    return sort_by_key[sort_key]


def convert_secs_to_date(dictionary):
    dictionary["submission_time"] = datetime.fromtimestamp(int(dictionary["submission_time"]))


def convert_questions_secs_to_date(questions):
    for question in questions:
        question["submission_time"] = datetime.fromtimestamp(int(question["submission_time"]))


def get_mutable_list(filename):
    return [{key: item for key, item in dictionary.items()}
            for dictionary in connection.read_data_from_file(filename)]


def get_updated_questions(question_id, question, filename="sample_data/test_questions.csv"):
    questions = connection.read_data_from_file(filename)
    question_index = [index for index, current_question in enumerate(questions) 
                      if current_question["id"] == question_id][0]
    questions[question_index] = question
    return questions
