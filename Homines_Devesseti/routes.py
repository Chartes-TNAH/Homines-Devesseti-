from flask import render_template, request
from .app import app
from .modeles.donnees import Personnes, Reconnaissances, Repertoire, DetailRedevances, DetailPossessions

#Requêtes
hommes = Personnes.query.order_by(Personnes.id).all()
recs = Reconnaissances.query.join(Repertoire).order_by(Reconnaissances.id_reconnaissance).all()
dets_pos = DetailPossessions.query.order_by(DetailPossessions.id_detail_possession).all()
dets_red = DetailRedevances.query.order_by(DetailRedevances.id_detail_redevance).all()
'''Les éléments issus de cette jointure forment une liste dans Reconnaissances.page'''
REPONSES_PAR_PAGES = 20

@app.route("/")
def accueil():
    return render_template("pages/accueil.html", nom="Homines Devesseti")

@app.route("/index")
def index():
    return render_template("pages/index.html", nom="Homines Devesseti",
        recs=recs, hommes=hommes, dets_pos=dets_pos, dets_red=dets_red)

@app.route("/name/<int:name_id>")
def nom(name_id):
    return render_template("pages/noms.html", nom="Homines Devesseti", homme=hommes[name_id - 1])
#On enlève systématiquement 1 à l'index car Python fait commencer le sien à 0

@app.route("/dp/<int:dp_id>")
def det_pos(dp_id):
    return render_template("pages/detail_possessions.html", nom="Homines Devesseti", det_pos=dets_pos[dp_id - 1])

@app.route("/dr/<int:dr_id>")
def det_red(dr_id):
    return render_template("pages/detail_redevances.html", nom="Homines Devesseti", det_red=dets_red[dr_id - 1])

@app.route("/rec/<int:rec_id>")
def rec(rec_id):
    reco = list(filter(lambda rec: rec.id_reconnaissance == rec_id, recs))
    '''J'ai voulu ici créer mes routes non pas en fonction de l'id de la ligne mais d'un id perso que j'ai réutilisé
    dans d'autres tables et dont j'ai besoin pour faire des renvois internes.
    La fonction filter permet de retrouver la ligne dont l'id perso correspond à l'id de la route.
    La fontion list permet de transformer le résultat en liste.
    La ligne que je cherche en est donc le premier et seul contenu'''
    rec_hommes = list(filter(lambda homme: homme.id_reconnaissance == rec_id, hommes))
    rec_det_pos = list(filter(lambda det_pos: det_pos.id_reconnaissance == rec_id, dets_pos))
    rec_det_red = list(filter(lambda det_red: det_red.id_reconnaissance == rec_id, dets_red))
    '''Pour réaliser ces renvois internes, j'ai également créé une liste contenant tous les éléments concernés par 
    chacune des reconnaissances afin de crer un lien hypertext vers leur page'''
    return render_template("pages/reconnaissances.html", nom="Homines Devesseti", rec=reco[0],
        rec_hommes=rec_hommes, rec_det_pos=rec_det_pos, rec_det_red=rec_det_red)

@app.route("/recherche")
def recherche():
    motclef = request.args.get("keyword", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    resultats = []
    titre = "Recherche"
    if motclef:
        resultats = Personnes.query.filter(Personnes.nom.like("%{}%".format(motclef))).paginate(page=page,
            per_page=REPONSES_PAR_PAGES)
        titre = "Résultat pour la recherche `" + motclef + "`"
    return render_template("pages/recherche.html", resultats=resultats, titre=titre, keyword=motclef)

