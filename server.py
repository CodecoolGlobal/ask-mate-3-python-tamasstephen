from flask import Flask, render_template, request, url_for, redirect
import data_handler


app = Flask(__name__)


@app.route("/")
def open_questions():
    questions= data_handler.get_questions_from_file()
    return render_template("index.html", questions=questions, headers=data_handler.HEADERS)


@app.route("/question/<question_id>")
def open_question_page(question_id):
    question = data_handler.get_question_by_id(question_id)
    answers = data_handler.get_answers_by_question_id(question_id)
    return render_template("question.html", question=question, answers=answers)


@app.route("/add_question", methods='POST')
def open_add_question():
    data_handler.add_form_data(request.form)
    return render_template("add_question.html")


@app.route("/question/<question_id>/add_answer", methods=["POST", "GET"])
def add_answer(question_id):
    if request.method == "POST":
        data_handler.add_form_data(request.form, "sample_data/test_answers.csv", question_id)
        return redirect(url_for('open_question_page', question_id=question_id))
    return render_template("add_answer.html", question_id=question_id)


if __name__ == "__main__":
    app.run(
        debug=True
    )
