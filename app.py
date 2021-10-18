from logging import debug
from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from random import randint, choice, sample

from werkzeug.wrappers import response
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"


app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route("/")
def home_page():
    """Home page of survey"""
    return render_template("survey_start.html", survey=survey)


@app.route("/initiate", methods=["POST"])
def begin_survey():
    """Clear the session of responses."""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def handle_question():
    """Save users response and redirect to next question"""

    choice = request.form['answer']

    # add the response to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses


    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")



@app.route("/questions/<int:id>")
def show_question(id):
    """Show current question"""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    if (len(responses) != id):
        flash(f"Invalid question id: {id}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[id]
    return render_template(
        "question.html", question_num=id, question=question)


@app.route("/complete")
def complete():
    """Show survey completion page."""

    return render_template("completion.html")