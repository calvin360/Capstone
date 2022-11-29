from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("base.html")

@app.route("/hello")
def hello():
    return render_template("hello.html")

if __name__ == "__main__":
    app.run()