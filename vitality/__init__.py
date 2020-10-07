from flask import Flask,  render_template, url_for
from flask_pymongo import PyMongo


import os
# from markupsafe import escape # Used to escape characters


def create_app():

    app = Flask(__name__, instance_relative_config=True)
    logger = app.logger
    
    @app.route('/', methods=["GET"])
    def index():
        logger.info('Rendering Index')
        return render_template("index.html")

    @app.errorhandler(403)
    def page_not_found(e):
        logger.info('Rendering 403')
        return "403", 403
    
    @app.errorhandler(404)
    def page_not_found(e):
        logger.info('Rendering 404')
        return "404", 404
    
    @app.errorhandler(410)
    def page_not_found(e):
        logger.info('Rendering 410')
        return "410", 410
    
    @app.errorhandler(500)
    def page_not_found(e):
        logger.info('Rendering 500')
        return "500", 500




    # Return for Application Factory
    return app

