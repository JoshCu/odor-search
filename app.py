from dotenv import load_dotenv
import requests
import os
import json
import ast
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
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
    atlas_api_key = os.environ.get("ATLAS_API_KEY")
    url = "https://data.mongodb-api.com/app/data-dpfbx/endpoint/odor_search"

    payload = {"search_term": term}
    headers = {'api-key': atlas_api_key}

    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)
