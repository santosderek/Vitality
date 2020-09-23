from flask import Flask, render_template, url_for
import os
# from markupsafe import escape # Used to escape characters


def create_app():
   
    app = Flask(__name__, instance_relative_config=True)
    
    @app.route('/', methods=["GET"])
    def index():
        return render_template("index.html")
   
    return app

