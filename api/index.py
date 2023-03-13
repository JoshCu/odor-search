import requests
import os
import json
import ast
import openai
from flask import Flask, g, redirect, render_template, request, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
from api.models import User, authenticate_user
login_manager = LoginManager()

app = Flask(__name__)
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = os.getenv("FLASK_SECRET_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
atlas_api_key = os.getenv("ATLAS_API_KEY")


@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    if user_id is None:
        return None
    if user_id != str(os.getenv("UID")):
        return None
    return (User(user_id, str(os.getenv("USER")), str(os.getenv("USER"))))


@app.route("/", methods=("GET", "POST"))
@login_required
def index():
    if request.method == "POST":
        term = request.form["search_term"]
        search_result = search_all(term)
        return redirect(url_for("index", result=search_result))

    search_result = request.args.getlist("result")
    # replace the, None with an empty string
    search_result = [ast.literal_eval(x) for x in search_result]
    for res in search_result:
        if "name" not in res:
            if "IUPACName" in res:
                res["name"] = res["IUPACName"][0]
            elif "all_names" in res:
                res["name"] = res["all_names"][0]
            elif "IsomericSmiles" in res:
                res["name"] = res["IsomericSmiles"]
            else:
                res["name"] = "No name found"
        if "CAS" in res:
            res["CAS"] = [x for x in res["CAS"] if x is not None]
        if "all_names" in res:
            res["all_names"] = [x for x in res["all_names"] if x != res["name"]]

    return render_template("results.html", result=search_result)


def search_all(term):
    # load the environment variables

    url = "https://data.mongodb-api.com/app/data-dpfbx/endpoint/odor_search"

    payload = {"search_term": term}
    headers = {'api-key': atlas_api_key}

    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)


@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User(str(os.getenv("UID")), username, password)
        print(user)
        login_success = authenticate_user(user)
        print(login_success)
        if login_success:
            login_user(user)
            return redirect(url_for("index"))
        else:
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
