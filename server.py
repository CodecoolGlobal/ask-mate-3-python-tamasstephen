from flask import Flask, render_template, request, url_for, redirect, session, flash

import data_handler
import search
import tag
import os
import comment
import user_commits
from bonus_questions import SAMPLE_QUESTIONS
import login
import register_new_user
import util
import psycopg2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = data_handler.UPLOAD_FOLDER

app.secret_key = os.urandom(12)


@app.route("/")
def open_questions():
    if request.args.get("sort"):
        questions = data_handler.get_last_five_questions(request.args.get("sort"))
        return render_template("index.html", questions=questions, headers=data_handler.QUESTION_HEADERS_TO_PRINT)
    questions = data_handler.get_last_five_questions_from_db()
    question_id = ""
    return render_template("index.html", questions=questions, headers=data_handler.QUESTION_HEADERS_TO_PRINT,
                           question_id=question_id)


@app.route("/list")
def open_all_questions():
    if request.args.get("sort"):
        questions = data_handler.get_all_questions(request.args.get("sort"))
        return render_template("index.html", questions=questions, headers=data_handler.QUESTION_HEADERS_TO_PRINT,
                               all=True)
    questions = data_handler.get_all_questions()
    question_id = ""
    return render_template("index.html", questions=questions, headers=data_handler.QUESTION_HEADERS_TO_PRINT,
                           question_id=question_id, all=True)


# validate if user logged in or not
@app.route("/question/<question_id>")
def open_question_page(question_id):
    try:
        if session['user_name']:
            answers = data_handler.get_answers_by_question_id(question_id)
            question = util.get_data_by_id(question_id, "question")[0]
            question_comments = comment.get_comments("question_id", question_id)
            answer_comments = {answer["id"]: comment.get_comments("answer_id", answer["id"]) for answer in answers}
            tags = tag.get_question_tags(question_id)
            data_handler.count_views(question_id)
            return render_template("question.html",
                                   question=question,
                                   answers=answers,
                                   question_comments=question_comments,
                                   answer_comments=answer_comments,
                                   tags=tags,
                                   this_question_id=question_id)
    except KeyError:
        flash("Please Sign up to get access to the whole content")
        # else:
        return redirect(url_for('open_questions'))


# validate if user logged in or not
# REFACTORING Needed
@app.route("/add_question", methods=["GET", "POST"])
def open_add_question():
    try:
        if session['user_name']:
            if request.method == "GET":
                return render_template("add_question.html")
            file = request.files["image"]
            user_id = session['user_id']
            if file.filename != "":
                file.save(os.path.join(app.config["UPLOAD_FOLDER"][0], file.filename))
                data_handler.add_question(request.form, user_id, image_name=file.filename)
            else:
                data_handler.add_question(request.form, user_id)
            return redirect("/")
    except KeyError:
        flash("Please Sign up to get access to the whole content")
        return redirect(url_for('open_questions'))


# REFACTORING Needed
@app.route("/question/<question_id>/add_answer", methods=["POST", "GET"])
def add_answer(question_id):
    if request.method == "POST":
        file = request.files["image"]
        user_id = session['user_id']
        if file.filename != "":
            file.save(os.path.join(app.config["UPLOAD_FOLDER"][1], file.filename))
            data_handler.add_new_answer(request.form, question_id, user_id, image_name=file.filename)
        else:
            data_handler.add_new_answer(request.form, question_id, user_id)
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
    util.delete_item_by_id(answer_id, "answer")
    return redirect(url_for("open_question_page", question_id=question_id))


@app.route("/question/<question_id>/vote_up", methods=["POST"])
def vote_question_up(question_id):
    try:
        if session['user_name']:
            user_id_list = data_handler.get_user_id_by_id(question_id, "question_id", "question_to_user")
            if user_id_list:
                data_handler.gain_reputation(user_id_list[0][
                                                 'user_id'], util.reputation_values['vote_up_question'])
            data_handler.handle_votes(int(question_id), "vote_up")
            return redirect("/")
    except KeyError:
        flash("Please Sign up to get access to the whole content")
        return redirect(url_for('open_questions'))


@app.route("/comments/<comment_id>/delete", methods=['POST'])
def delete_comment(comment_id):
    question_id = comment.get_question_id_by_comment_id(comment_id)
    comment.delete_comment_by_comment_id(comment_id)
    return redirect(url_for("open_question_page", question_id=question_id))


@app.route("/question/<question_id>/vote_down", methods=["POST"])
def vote_question_down(question_id):
    try:
        if session['user_name']:
            user_id_list = data_handler.get_user_id_by_id(question_id, "question_id", "question_to_user")
            if user_id_list:
                data_handler.gain_reputation(user_id_list[0][
                                                 'user_id'], util.reputation_values['vote_down_question'])
            data_handler.handle_votes(int(question_id), "vote_down")
            return redirect("/")
    except KeyError:
        flash("Please Sign up to get access to the whole content")
        return redirect(url_for('open_questions'))


@app.route("/answer/<answer_id>/vote_up", methods=["POST"])
def vote_answer_up(answer_id):
    question_id = util.get_data_by_id(answer_id, "answer")[0]['question_id']
    user_id_list = data_handler.get_user_id_by_id(answer_id, "answer_id", "answer_to_user")
    if user_id_list:
        data_handler.gain_reputation(user_id_list[0][
                                         'user_id'], util.reputation_values['vote_up_answer'])
    data_handler.handle_votes(answer_id, "vote_up", "answer")
    return redirect(url_for("open_question_page", question_id=question_id))


@app.route("/answer/<answer_id>/vote_down", methods=["POST"])
def vote_answer_down(answer_id):
    question_id = util.get_data_by_id(answer_id, "answer")[0]['question_id']
    user_id_list = data_handler.get_user_id_by_id(answer_id, "answer_id", "answer_to_user")
    if user_id_list:
        data_handler.gain_reputation(user_id_list[0][
                                         'user_id'], util.reputation_values['vote_down_answer'])
    data_handler.handle_votes(answer_id, "vote_down", "answer")
    return redirect(url_for("open_question_page", question_id=question_id))


@app.route("/question/<question_id>/comment", methods=["GET", "POST"])
def add_comment_to_question(question_id):
    if request.method == "POST":
        user_id = session['user_id']
        comment.add_comment_to_question_db(question_id, request.form["message"], util.get_current_time())
        comment.bind_comments_to_user(user_id)
        return redirect(url_for("open_question_page", question_id=question_id))
    return render_template("comment.html", question_id=question_id)


@app.route("/answer/<answer_id>/new-comment", methods=["GET", "POST"])
def add_comment_to_answer(answer_id):
    if request.method == "POST":
        user_id = session['user_id']
        comment.add_comment_to_answer_db(answer_id, request.form["message"], util.get_current_time())
        question_id = data_handler.get_question_id_by_answer_id(answer_id)[0]["question_id"]
        comment.bind_comments_to_user(user_id)
        return redirect(url_for("open_question_page", question_id=question_id))
    return render_template("answer_comment.html", answer_id=answer_id)


@app.route("/answer/<answer_id>/edit", methods=["GET", "POST"])
def edit_answer(answer_id):
    if request.method == "POST":
        data_handler.update_answer(answer_id, request.form["message"])
        question_id = data_handler.get_question_id_by_answer_id(answer_id)[0]["question_id"]
        return redirect(url_for("open_question_page", question_id=question_id))
    message = data_handler.get_answer_by_answer_id(answer_id)[0]["message"]
    return render_template('edit_answer.html', answer_id=answer_id, message=message)


@app.route("/comment/<comment_id>/edit", methods=["GET", "POST"])
def edit_comment(comment_id):
    if request.method == "POST":
        comment_mod = comment.get_comment_by_comment_id(comment_id)
        if not comment_mod[0]["edited_count"]:
            comment_mod = 1
        else:
            comment_mod = comment_mod[0]["edited_count"] + 1
        comment.update_comment(comment_id, request.form["message"], util.get_current_time(), comment_mod)
        question_id = comment.get_question_id_by_comment_id(comment_id)
        return redirect(url_for("open_question_page", question_id=question_id))
    message = comment.get_comment_by_comment_id(comment_id)[0]["message"]
    return render_template("edit_comment.html", message=message, comment_id=comment_id)


@app.route("/search")
def search_data():
    questions = search.get_items_with_phrase(request.args.get("q"))
    return render_template("index.html", questions=questions, headers=data_handler.QUESTION_HEADERS_TO_PRINT)


@app.route("/question/<question_id>/new-tag", methods=["GET", "POST"])
def add_tag(question_id):
    if request.method == "GET":
        tags = tag.get_unused_tags(question_id)
        return render_template("tags.html", tags=tags, question_id=question_id)
    if request.form.get('new_tag'):
        tag.create_new_tag(request.form.get("new_tag"))
    else:
        tag.add_tags_to_question(question_id, request.form)
    return redirect(url_for('open_question_page', question_id=question_id))


@app.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_tag_from_question(question_id, tag_id):
    tag.delete_tag_from_question_tag_db(question_id, tag_id)
    return redirect(url_for('open_question_page', question_id=question_id))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        if (not request.form.get("password") or not request.form.get("username") is not True) or " " in request.form.get("username"):
            print(request.form.get("password"), request.form.get("username"))
            flash('Invalid username or password')
            return render_template("register.html")
        else:
            try:
                print("asd")
                print("aaaaaaa")
                hashed_pw = register_new_user.hash_password((request.form['password']))
                username = request.form['username']
                registration_date = util.get_current_time()
                register_new_user.add_new_account_into_db(username, hashed_pw, registration_date)
                flash('The registration was successful.')
                return redirect(url_for('open_questions'))
            except psycopg2.errors.UniqueViolation:
                flash('Username already used')
                return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        try:
            session['user_name'] = request.form['username']
            session['user_id'] = login.get_user_id_by_username(request.form['username'])[0]["user_id"]
            user_login_password = request.form.get('password')
            user_password_in_db = login.get_user_password_by_username(request.form['username'])[0]["password"]
            if user_password_in_db:
                password_check = login.verify_password(user_login_password, user_password_in_db)
                if password_check:
                    return redirect(url_for('open_questions'))
                else:
                    session.pop('user_name', None)
                    session.pop('user_id', None)
                    flash('Invalid username or password')
                    return render_template('login.html')
        except IndexError:
            session.pop('user_name', None)
            session.pop('user_id', None)
            flash('Invalid username or password')
            return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('user_name', None)
    session.pop('user_id', None)
    return redirect(url_for('open_questions'))


@app.route('/users')
def list_all_users():
    users = data_handler.get_all_users()
    return render_template('list_users.html', users=users)


@app.route("/bonus-questions")
def main():
    return render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)


@app.route("/user/<user_id>")
def user_page(user_id):
    questions = user_commits.get_questions_by_user_id(user_id)
    answer_by_questions = user_commits.get_answer_dict_by_question_id(user_commits.get_message_ids(user_id,
                                                                                                   "question_id",
                                                                                                   "question_to_user"))
    answers = user_commits.get_answers_by_user_id(user_id)
    comments = user_commits.get_comments_by_user_id(user_id)
    user_data = user_commits.get_user_data_by_user_id(user_id)[0]
    return render_template("user_data.html",
                           questions=questions,
                           answers=answers,
                           question_answers=answer_by_questions,
                           comments=comments,
                           user=user_data)


@app.route('/tags')
def open_tags_page():
    all_tags = data_handler.get_all_tags()
    return render_template('show_tags.html', tags=all_tags)


@app.route("/answer/<answer_id>/approve/<user_id>", methods=["POST"])
def approve_answer(answer_id, user_id):
    if request.form.get("approved") == 'on':
        data_handler.approve_answer(True, answer_id)
        return redirect(url_for("user_page", user_id=user_id))
    data_handler.approve_answer(False, answer_id)
    return redirect(url_for("user_page", user_id=user_id))


if __name__ == "__main__":
    app.run(
        port=5000,
        debug=True
    )
