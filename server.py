from flask import Flask, render_template 
import data_handler


app = Flask(__name__)


@app.route("/")
def open_questions():
    questions= data_handler.get_questions_from_file() 
    return render_template("index.html", questions=questions, headers=data_handler.HEADERS) 


@app.route("/question/<question_id>")
def open_question_page(question_id):
    question_page_content = ["return value of a func with the question id arg"]
    return render_template("question.html", content=question_page_content)


@app.route("/add_question")
def open_add_question():
    return render_template("add_question.html")


@app.route("/question/<question_id>/add_answer")
def add_answer(question_id):
    return render_template("add_answer.html", id=question_id)


if __name__ == "__main__":
    app.run(
        debug=True
    )
