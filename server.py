from flask import Flask, render_template, request, url_for, redirect
import data_handler


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def open_questions():
    if request.method == "POST":
        questions = data_handler.get_questions_from_file(request.form["sort"])
        return render_template("index.html", questions=questions, headers=data_handler.HEADERS)
    questions = data_handler.get_questions_from_file()
    question_id = ""
    return render_template("index.html", questions=questions, headers=data_handler.HEADERS, question_id=question_id)


# @app.route("/<sort>")
# def open_sorted_questions(sort):
#     questions = data_handler.get_questions_from_file(sort)
#     return render_template("index.html", question=questions, headers=data_handler.HEADERS)


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
    data_handler.add_form_data(request.form)
    return redirect("/")


@app.route("/question/<question_id>/add_answer", methods=["POST", "GET"])
def add_answer(question_id):
    if request.method == "POST":
        print(question_id)
        data_handler.add_form_data(request.form, "sample_data/test_answers.csv", question_id)
        return redirect(url_for('open_question_page', question_id=question_id))
    return render_template("add_answer.html", question_id=question_id)


@app.route("/answer/<int:question_id>/delete", methods=["POST"])
def delete_answer(question_id):
    print('lol')
    data_handler.delete_questions(question_id, "sample_data/test_questions.csv")
    return redirect("/")


if __name__ == "__main__":
    app.run(
        port=9000,
        debug=True
    )
