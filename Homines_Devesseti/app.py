from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from .constantes import CONFIG

chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")
statics = os.path.join(chemin_actuel, "static")

db = SQLAlchemy()
login = LoginManager()

app = Flask(__name__,
    template_folder=templates,
    static_folder=statics)

'''Le premier argument de la fonction Flask correspond au nom du répertoire dans lequel sont situés les éléments utilisés
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///homines_devesseti.db?check_same_thread=False'
L'argument check_same_thread permet d'éviter les problèmes de thread au moment des requêtes utilisant des jointures
Nous avons ici veillé à placer le fichier sqlite dans le même dossier que celui-ci afin d'éviter toute problème de path
lié à un changement d'os
db = SQLAlchemy(app)

# Mise en place de la gestion d'utilisateurs
login = LoginManager(app)'''

from .routes import generic, api

def config_app(config_name="test"):
    """ Create the application """
    app.config.from_object(CONFIG[config_name])
    # Set up extensions
    db.init_app(app)
    # assets_env = Environment(app)
    login.init_app(app)
    # Register Jinja template functions
    return app

'''with app.app_context():
    db.create_all()'''