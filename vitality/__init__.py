from flask import (
    Flask, 
    render_template, 
    url_for, 
    request, 
    session, 
    redirect, 
    g
)
from flask_pymongo import PyMongo
from .user import User


### TODO: need to replace this with looking into the database. 
users = []
users.append(User(id=1, username='derek', password='derek'))
users.append(User(id=2, username='bryson', password='bryson'))


import os
# from markupsafe import escape # Used to escape characters


def create_app():

    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = 'somethingverysecret'
    logger = app.logger
    
    @app.before_request
    def before_request():
        g.user = None

        if 'user_id' in session:
            user = [x for x in users if x.id == session['user_id']][0]
            g.user = user

    @app.route('/', methods=["GET"])
    def index():
        logger.info('Rendering Index')
        return render_template("index.html")

    @app.route('/login', methods=["GET", "POST"])
    def login():
        logger.info('Rendering Index')
        
        if request.method == 'POST': 
            # Removing the last session id if there is one already
            session.pop('user_id', None)

            username = request.form['username']
            password = request.form['password']

            # This needs to be replaced once we get the database up and running
            # TODO: This errors out when no username is found, handle that...
            user = [x for x in users if x.username == username][0]

            if user and user.password == password:
                logger.debug('User exists')
                session['user_id'] = user.id
                return redirect(url_for('profile'))
            
            # If username != correct password return back to login
            return redirect(url_for('login'))

        return render_template("login.html")

    @app.route('/createuser', methods=["GET"])
    def createuser():
        logger.info('Rendering Index')
        return render_template("createuser.html")

    @app.route('/profile', methods=["GET"])
    def profile():
        logger.info('Rendering Index')

        if not g.user:
            return redirect(url_for('login'))
        
        return render_template("profile.html")

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

