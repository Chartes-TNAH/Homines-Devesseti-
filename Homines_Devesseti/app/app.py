from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Instanciation de ma base de données
app = Flask("Homines Devesseti")
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///db\homines_devesseti.db'
## Chemin relatif du fichier sous windows
db = SQLAlchemy(app)

from .routes import accueil, nom, recherche
