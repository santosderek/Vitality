from flask import Flask, render_template, url_for
# from markupsafe import escape # Used to escape characters

app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")

app.run(host="0.0.0.0", port="8080", debug=False)
