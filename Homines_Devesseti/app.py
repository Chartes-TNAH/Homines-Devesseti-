from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")
statics = os.path.join(chemin_actuel, "static")

app = Flask("Homines_Devesseti",
    template_folder=templates,
    static_folder=statics)
#Le premier argument de la fonction Flask correspond au nom du répertoire dans lequel sont situés les éléments utilisés
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///homines_devesseti.db?check_same_thread=False'
#L'argument check_same_thread permet d'éviter les problèmes de thread au moment des requêtes utilisant des jointures
db = SQLAlchemy(app)

from .routes import accueil, nom, recherche, index, rec
