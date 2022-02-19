from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from .constantes import SECRET_KEY

chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")
statics = os.path.join(chemin_actuel, "static")

app = Flask("Homines_Devesseti",
    template_folder=templates,
    static_folder=statics)
#Le premier argument de la fonction Flask correspond au nom du répertoire dans lequel sont situés les éléments utilisés
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///homines_devesseti.db?check_same_thread=False'
#L'argument check_same_thread permet d'éviter les problèmes de thread au moment des requêtes utilisant des jointures
db = SQLAlchemy(app)

# Mise en place de la gestion d'utilisateurs
login = LoginManager(app)

from .routes import generic, api