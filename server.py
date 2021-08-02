from flask import Flask, render_template 

app = Flask(__name__)


@app.route("/")
def open_questions():
    questions= ["return value of a function"] 
    return render_template("index.html", questions=questions) 


@app.route("question/<question_id>")
def open_question_page(question_id):
    question_page_content = ["return value of a func with the question id arg"]
    return render_template("question.html", content=question_page_content)


if __name__ == "__main__":
    app.run()
