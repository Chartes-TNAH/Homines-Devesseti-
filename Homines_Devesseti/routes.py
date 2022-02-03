from flask import render_template, request
from .app import app
from .modeles.donnees import Personnes

#Requêtes
hommes = Personnes.query.all()

@app.route("/")
def accueil():
    return render_template("pages/accueil.html", nom="Homines Devesseti", hommes=hommes)

@app.route("/index")
def index():
    return render_template("pages/index.html", nom="Homines Devesseti", hommes=hommes)

@app.route("/name/<int:name_id>")
def nom(name_id):
    return render_template("pages/noms.html", nom="Homines Devesseti", homme=hommes[name_id])

@app.route("/recherche")
def recherche():
    # On préfèrera l'utilisation de .get() ici
    #   qui nous permet d'éviter un if long (if "clef" in dictionnaire and dictonnaire["clef"])
    motclef = request.args.get("keyword", None)
    # On crée une liste vide de résultat (qui restera vide par défaut
    #   si on n'a pas de mot clé)
    resultats = []
    # On fait de même pour le titre de la page
    titre = "Recherche"
    if motclef:
        resultats = Personnes.query.filter(
            Personnes.nom.like("%{}%".format(motclef))
        ).all()
        titre = "Résultat pour la recherche `" + motclef + "`"
    return render_template("pages/recherche.html", resultats=resultats, titre=titre)

