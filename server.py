from flask import Flask, render_template, request, url_for, redirect
import data_handler
import os

import util

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = data_handler.UPLOAD_FOLDER


@app.route("/", methods=["POST", "GET"])
def open_questions():
    if request.method == "POST":
        questions = data_handler.get_questions_from_file(request.form["sort"])
        return render_template("index.html", questions=questions, headers=data_handler.QUESTION_HEADERS_TO_PRINT)
    questions = data_handler.get_questions_from_file()
    question_id = ""
    return render_template("index.html", questions=questions, headers=data_handler.QUESTION_HEADERS_TO_PRINT, question_id=question_id)


@app.route("/question/<question_id>")
def open_question_page(question_id):
    answers = data_handler.get_answers_by_question_id(question_id)
    question = util.get_data_by_id(question_id, "question")[0]
    data_handler.count_views(question_id)
    return render_template("question.html", question=question, answers=answers, this_question_id=question_id)


# REFACTORING Needed
@app.route("/add_question", methods=["GET", "POST"])
def open_add_question():
    if request.method == "GET":
        return render_template("add_question.html")
    file = request.files["image"]
    if file.filename != "":
        file.save(os.path.join(app.config["UPLOAD_FOLDER"][0], file.filename))
        data_handler.add_question(request.form, image_name=file.filename)
    else:
        data_handler.add_question(request.form)
    return redirect("/")


# REFACTORING Needed
@app.route("/question/<question_id>/add_answer", methods=["POST", "GET"])
def add_answer(question_id):
    print("isfasd")
    if request.method == "POST":
        file = request.files["image"]
        if file.filename != "":
            file.save(os.path.join(app.config["UPLOAD_FOLDER"][1], file.filename))
            data_handler.add_new_answer(request.form, question_id, image_name=file.filename)
        else:
            data_handler.add_new_answer(request.form, question_id)
        return redirect(url_for('open_question_page', question_id=question_id))
    return render_template("add_answer.html", question_id=question_id)


@app.route("/question/<question_id>/delete", methods=["POST"])
def delete_question(question_id):
    data_handler.delete_all_answers(question_id)
    util.delete_item_by_id(question_id, "question")
    return redirect("/")


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def open_edit_question(question_id):
    if request.method == "GET":
        question = util.get_data_by_id(question_id, "question")[0]
        return render_template("edit_question.html", question=question, question_id=question_id)
    data_handler.update_question(question_id, request.form)
    return redirect(url_for("open_question_page", question_id=question_id))


@app.route("/answer/<answer_id>/delete", methods=["POST"])
def delete_answer_from_question_page(answer_id):
    question_id = util.get_data_by_id(answer_id, "answer")[0]["question_id"]
    util.delete_item_by_id(answer_id,"answer")
    return redirect(url_for("open_question_page", question_id=question_id))


@app.route("/question/<question_id>/vote_up", methods=["POST"])
def vote_question_up(question_id):
    print(question_id)
    data_handler.handle_votes(int(question_id), "vote_up")
    return redirect("/")


@app.route("/question/<question_id>/vote_down", methods=["POST"])
def vote_question_down(question_id):
    data_handler.handle_votes(int(question_id), "vote_down")
    return redirect("/")


@app.route("/answer/<answer_id>/vote_up", methods=["POST"])
def vote_answer_up(answer_id):
    question_id = util.get_data_by_id(answer_id, "answer")[0]['question_id']
    data_handler.handle_votes(answer_id, "vote_up", "answer")
    return redirect(url_for("open_question_page", question_id=question_id))


@app.route("/answer/<answer_id>/vote_down", methods=["POST"])
def vote_answer_down(answer_id):
    question_id = util.get_data_by_id(answer_id, "answer")[0]['question_id']
    data_handler.handle_votes(answer_id, "vote_down", "answer")
    return redirect(url_for("open_question_page", question_id=question_id))


if __name__ == "__main__":
    app.run(
        port=9000,
        debug=True
    )
