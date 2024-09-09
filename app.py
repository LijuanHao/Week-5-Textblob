from flask import Flask
from textblob import TextBlob
import google.generativeai as palm
import os

api = os.getenv("MAKERSUITE_API_TOKEN")
model = {"model":"models/text-bison-001"}
palm.configure(api_key=api)

app = Flask(__name__)
from flask import render_template,request

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/main",methods=["GET","POST"])
def main():
    q = request.form.get("q")
    if request.method == "POST":
        text = request.form.get("text")
        print(text)
        r = TextBlob(text).sentiment
        return(render_template("main.html", result=r))
    else:
        return(render_template("main.html", result="2"))

@app.route("/makersuite",methods=["GET","POST"])
def makersuite():
    return(render_template("makersuite.html"))

@app.route("/makersuite_1",methods=["GET","POST"])
def makersuite_1():
    q = "Can you help me prepare my tax return?"
    r = palm.generate_text(**model, prompt=q)
    return(render_template("makersuite_1_reply.html",r=r.result))

@app.route("/makersuite_gen",methods=["GET","POST"])
def makersuite_gen():
    q = request.form.get("q")
    r = palm.generate_text(**model, prompt=q)
    return(render_template("makersuite_gen_reply.html",r=r.result))

if __name__ == "__main__":
    app.run()