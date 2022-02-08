from flask import render_template, request
from .app import app
from .modeles.donnees import Personnes, Reconnaissances, Repertoire

#Requêtes
hommes = Personnes.query.all()
recs = Reconnaissances.query.join(Repertoire).all()
'''Les éléments issus de cette jointure forment une liste dans Reconnaissances.page'''

@app.route("/")
def accueil():
    return render_template("pages/accueil.html", nom="Homines Devesseti")

@app.route("/index")
def index():
    return render_template("pages/index.html", nom="Homines Devesseti", recs=recs, hommes=hommes)

@app.route("/name/<int:name_id>")
def nom(name_id):
    return render_template("pages/noms.html", nom="Homines Devesseti", homme=hommes[name_id - 1])
#On enlève systématiquement 1 à l'index car Python fait commencer le sien à 0

@app.route("/rec/<int:rec_id>")
def rec(rec_id):
    reco = list(filter(lambda rec: rec.id_reconnaissance == rec_id, recs))
    '''J'ai voulu ici créer mes routes non pas en fonction de l'id de la ligne mais d'un id perso que j'ai réutilisé
    dans d'autres tables et dont j'ai besoin pour faire des renvois internes.
    La fonction filter permet de retrouver la ligne dont l'id perso correspond à l'id de la route.
    La fontion list permet de transformer le résultat en liste.
    La ligne que je cherche en est donc le premier et seul contenu'''
    rec_hommes = list(filter(lambda homme: homme.id_reconnaissance == rec_id, hommes))
    '''Pour ces renvois internes, j'ai également créé une liste contenant toutes les personnes concernée par chacune
    des reconnaissances listées plus haut afin de crer un lien hypertext vers leur page'''
    ## <!--<dt>Page</dt><dd>{{rec.page.ref_du_terrier}}</dd>--> Requête inachevée à cause d'un problème de session SQLite ...
    print(recs[0].page[0].ref_du_terrier)
    return render_template("pages/reconnaissances.html", nom="Homines Devesseti", rec=reco[0], rec_hommes=rec_hommes)

@app.route("/recherche")
def recherche():
    motclef = request.args.get("keyword", None)
    resultats = []
    titre = "Recherche"
    if motclef:
        resultats = Personnes.query.filter(Personnes.nom.like("%{}%".format(motclef))).all()
        titre = "Résultat pour la recherche `" + motclef + "`"
    return render_template("pages/recherche.html", resultats=resultats, titre=titre)

