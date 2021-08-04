from flask import Flask, render_template, request, url_for, redirect
import data_handler
import os

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
    question = data_handler.get_question_by_id(question_id)
    answers = data_handler.get_answers_by_question_id(question_id)
    data_handler.count_views(question_id)
    return render_template("question.html", question=question, answers=answers, this_question_id=question_id)


@app.route("/add_question", methods=["GET", "POST"])
def open_add_question():
    if request.method == "GET":
        return render_template("add_question.html")
    file = request.files["image"]
    if file.filename != "": 
        file.save(os.path.join(app.config["UPLOAD_FOLDER"][0], file.filename))
        data_handler.add_form_data(request.form, image_name=file.filename)
    else:
        data_handler.add_form_data(request.form)
    return redirect("/")


@app.route("/question/<question_id>/add_answer", methods=["POST", "GET"])
def add_answer(question_id):
    if request.method == "POST":
        file = request.files["image"]
        if file.filename != "": 
            file.save(os.path.join(app.config["UPLOAD_FOLDER"][1], file.filename))
            data_handler.add_form_data(request.form, "sample_data/test_answers.csv", question_id, image_name=file.filename)
        else:
            data_handler.add_form_data(request.form, "sample_data/test_answers.csv", question_id)
        return redirect(url_for('open_question_page', question_id=question_id))
    return render_template("add_answer.html", question_id=question_id)


@app.route("/question/<question_id>/delete", methods=["POST"])
def delete_question(question_id):
    data_handler.delete_all_answers(question_id)
    data_handler.delete_item(question_id, data_handler.HEADERS, "sample_data/test_questions.csv")
    return redirect("/")


@app.route("/answer/<answer_id>/delete", methods=["POST"])
def delete_answer(answer_id):
    data_handler.delete_answer(answer_id, data_handler.ANSWER_HEADERS, "sample_data/test_answer.csv")
    return render_template("question.html")


if __name__ == "__main__":
    app.run(
        port=9000,
        debug=True
    )
