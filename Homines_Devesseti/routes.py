from flask import render_template, request
from .app import app
from .modeles.donnees import Personnes, Reconnaissances

#Requêtes
hommes = Personnes.query.all()
recs = Reconnaissances.query.all()

@app.route("/")
def accueil():
    return render_template("pages/accueil.html", nom="Homines Devesseti")

@app.route("/index")
def index():
    return render_template("pages/index.html", nom="Homines Devesseti", recs=recs)

@app.route("/name/<int:name_id>")
def nom(name_id):
    return render_template("pages/noms.html", nom="Homines Devesseti", homme=hommes[name_id - 1])
#On enlève systématiquement 1 à l'index car Python fait commencer le sien à 0

@app.route("/rec/<int:rec_id>")
def rec(rec_id):
    return render_template("pages/reconnaissances.html", nom="Homines Devesseti", rec=recs[rec_id - 1])

@app.route("/recherche")
def recherche():
    motclef = request.args.get("keyword", None)
    resultats = []
    titre = "Recherche"
    if motclef:
        resultats = Personnes.query.filter(Personnes.nom.like("%{}%".format(motclef))).all()
        titre = "Résultat pour la recherche `" + motclef + "`"
    return render_template("pages/recherche.html", resultats=resultats, titre=titre)

