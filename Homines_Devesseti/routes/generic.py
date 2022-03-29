from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user
import os
from ..app import app, login, db, chemin_actuel
from ..modeles.donnees import Personnes, Reconnaissances, Repertoire, DetailRedevances, DetailPossessions, Authorship
from ..modeles.utilisateurs import User
from ..constantes import PERSONNES_PAR_PAGE

#On va tenter de faire un truc avec lxml
from lxml import etree as ET
@app.route("/charte_hommes")
def charte_hommes():
    NAMESPACES = {
        "tei": "http://www.tei-c.org/ns/1.0"
    }
    path = os.path.join(chemin_actuel, "templates/charte", "Devoir_charte_Devesset.xml")
    file = ET.parse(path)
    root = file.xpath("//tei:personGrp[@role = 'Ratifiants']//tei:persName//text()", namespaces=NAMESPACES)
    #Là l'idée c'est à partir de ça d'essayer de récupérer des noeud txt en entier en les reconstituant pour en faire
    #une classe SQLAlchemy. Question à 1000 francs : comment reconstituer des noeuds ?
    for element in root:
        print(element)


# Routes de base :
@app.route("/")
def accueil():
    return render_template("pages/accueil.html", nom="Homines Devesseti")


@app.route("/index")
def index():
    hommes = Personnes.query.order_by(Personnes.id).all()
    dets_pos = DetailPossessions.query.order_by(DetailPossessions.id_detail_possession).all()
    dets_red = DetailRedevances.query.order_by(DetailRedevances.id_detail_redevance).all()
    recs = Reconnaissances.query.outerjoin(Repertoire).order_by(Reconnaissances.id_reconnaissance).all()
    '''Pour une raison que j'ignore, il est impossible de factoriser les requêtes au début de cette page.
    Il faut donc les répéter à chaque usage'''
    return render_template("pages/index.html", nom="Homines Devesseti",
                           recs=recs, hommes=hommes, dets_pos=dets_pos, dets_red=dets_red)


# Routes permettant l'affichage des données du terrier :
@app.route("/name/<int:name_id>")
def nom(name_id):
    hommes = Personnes.query.order_by(Personnes.id).all()
    nbr_hommes = hommes[-1].id
    return render_template("pages/noms.html", nom="Homines Devesseti", homme=hommes[name_id - 1], nbr=nbr_hommes)
    # On enlève systématiquement 1 à l'index car Python fait commencer le sien à 0


@app.route("/dp/<int:dp_id>")
def det_pos(dp_id):
    dets_pos = DetailPossessions.query.order_by(DetailPossessions.id_detail_possession).all()
    nbr_det_pos = dets_pos[-1].id_detail_possession
    return render_template("pages/detail_possessions.html", nom="Homines Devesseti", det_pos=dets_pos[dp_id - 1],
                           nbr=nbr_det_pos)


@app.route("/dr/<int:dr_id>")
def det_red(dr_id):
    dets_red = DetailRedevances.query.order_by(DetailRedevances.id_detail_redevance).all()
    nbr_det_red = dets_red[-1].id_detail_redevance
    return render_template("pages/detail_redevances.html", nom="Homines Devesseti", det_red=dets_red[dr_id - 1],
                           nbr=nbr_det_red)


@app.route("/rec/<int:rec_id>")
def rec(rec_id):
    recs = Reconnaissances.query.outerjoin(Repertoire).order_by(Reconnaissances.id_reconnaissance).all()
    # Les éléments issus de la jointure forment une liste dans Reconnaissances.page
    reco = list(filter(lambda rec: rec.id_reconnaissance == rec_id, recs))
    '''J'ai voulu ici créer mes routes non pas en fonction de l'id de la ligne mais d'un id perso que j'ai réutilisé
    dans d'autres tables et dont j'ai besoin pour faire des renvois internes.
    La fonction filter permet de retrouver la ligne dont l'id perso correspond à l'id de la route.
    La fontion list permet de transformer le résultat en liste.
    La ligne que je cherche en est donc le premier et seul contenu'''
    nbr_rec = recs[-1].id
    hommes = Personnes.query.order_by(Personnes.id).all()
    dets_pos = DetailPossessions.query.order_by(DetailPossessions.id_detail_possession).all()
    dets_red = DetailRedevances.query.order_by(DetailRedevances.id_detail_redevance).all()
    rec_hommes = list(filter(lambda homme: homme.id_reconnaissance == rec_id, hommes))
    rec_det_pos = list(filter(lambda det_pos: det_pos.id_reconnaissance == rec_id, dets_pos))
    rec_det_red = list(filter(lambda det_red: det_red.id_reconnaissance == rec_id, dets_red))
    '''Pour réaliser ces renvois internes, j'ai également créé une liste contenant tous les éléments concernés par 
    chacune des reconnaissances afin de crer un lien hypertext vers leur page'''
    return render_template("pages/reconnaissances.html", nom="Homines Devesseti", rec=reco[0],
                           rec_hommes=rec_hommes, rec_det_pos=rec_det_pos, rec_det_red=rec_det_red, nbr=nbr_rec)


# Routes concernant les comptes utilisateur :
@app.route("/register", methods=["GET", "POST"])
def inscription():
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        statut, donnees = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if statut is True:
            flash("Enregistrement effectué. Identifiez-vous maintenant", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")


@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté-e", "info")
        return redirect("/")
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        utilisateur = User.identification(
            login=request.form.get("login", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if utilisateur:
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect("/")
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")

    return render_template("pages/connexion.html")


login.login_view = 'connexion'


@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté(e)", "info")
    return redirect("/")


# Intégration de la charte de Devesset :
from bs4 import BeautifulSoup


def transfo_charte(path):
    #fonction un peu artisanale permettant de parser le html obtenu par la transfo de la charte utilisé pour le devoir
    # de XSLT et l'intégrer dans l'appli
    with open(path, 'r', encoding="ISO-8859-1") as f:
        html_doc = f.read()
    soup = BeautifulSoup(html_doc)
    body = str(soup.find('body')).replace('<body>', '').replace('</body>', '')
    changements = [["allograph", "norm", "index", "images", "accueil"], ["_paleo", "_norm", "_index", "_images", ""]]
    for c in changements[0]:
        body = body.replace(
        'file:/C:/Users/virgi/Desktop/Master%20TNAH/Python/Devoir_Python/Homines_Devesseti/templates/charte/Devoir_charte_Devesset_' + c + '.html',
        "{{url_for('charte" + changements[1][changements[0].index(c)] + "')}}")
    for x in range(1, 5):
        body = body.replace(
        "file:/C:/Users/virgi/Desktop/Master%20TNAH/Python/Devoir_Python/Homines_Devesseti/templates/charte/Images/Page_" + str(x) +".jpg",
        "{{url_for('static', filename='images/charte/Page_" + str(x) + ".jpg')}}")
    debut = "{% extends 'conteneur.html' %} {% block corps %}"
    fin = "<nav aria-label=\"research-pagination\" class=\"center-link\"><p><a href=\"{{url_for('accueil')}}\">Retour accueil</a></p></nav>{% endblock %}"
    with open(path, "w", encoding="ISO-8859-1") as f:
        f.write(debut)
        f.write(body)
        f.write(fin)


@app.route("/charte")
def charte():
    list_page = ["accueil", "allograph", "norm", "index", "images"]
    for page in list_page:
        nom_complet = "Devoir_charte_Devesset_" + page + ".html"
        path = os.path.join(chemin_actuel, "templates/charte", nom_complet)
        with open(path, 'r', encoding="ISO-8859-1") as f:
            html_doc = f.read()
        soup = BeautifulSoup(html_doc)
        id = soup.find('html').get('id')
        if id:
            transfo_charte(path)
        f.close()
    return render_template("charte/Devoir_charte_Devesset_accueil.html", nom="Homines Devesseti")


@app.route("/charte/paleo")
def charte_paleo():
    return render_template("charte/Devoir_charte_Devesset_allograph.html", nom="Homines Devesseti")


@app.route("/charte/norm")
def charte_norm():
    return render_template("charte/Devoir_charte_Devesset_norm.html", nom="Homines Devesseti")


@app.route("/charte/index")
def charte_index():
    return render_template("charte/Devoir_charte_Devesset_index.html", nom="Homines Devesseti")


@app.route("/charte/images")
def charte_images():
    return render_template("charte/Devoir_charte_Devesset_images.html", nom="Homines Devesseti")


# Routes pour mes recherches :
from whoosh import index, query
from whoosh.index import create_in
from whoosh.qparser import QueryParser
from ..models_whoosh import PageWhoosh


@app.route("/formulaire")
def formulaire(updated=False):
    try:
        index.open_dir(app.config["WHOOSH_SCHEMA_DIR"])
        attributs = ["nom", "prenom", "localité"]
        return render_template("pages/formulaire_recherche.html", nom="Homines Devesseti", attributs=attributs,
                               updated=updated)
    except:
        return redirect("/generate_index")


@app.route("/generate_index")
def generate_index(updated=False):
    ix = create_in(app.config["WHOOSH_SCHEMA_DIR"], PageWhoosh)
    writer = ix.writer()
    hommes = Personnes.query.order_by(Personnes.id).all()
    for homme in hommes:
        writer.add_document(
            id=homme.id,
            nom=homme.nom,
            prenom=homme.prenom,
            localité=homme.localite
        )
    writer.commit()
    flash("Index mis à jour", "info")
    return formulaire(updated=updated)


@app.route("/recherche")
def recherche():
    attribut = request.args.get("class", "nom")
    motclef = "*" + request.args.get("keyword", None) + "*"
    page = request.args.get("page", 1)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    ix = index.open_dir(app.config["WHOOSH_SCHEMA_DIR"])
    q = QueryParser(attribut, ix.schema).parse(motclef)
    with ix.searcher() as s:
        results = s.search_page(q, page, pagelen=PERSONNES_PAR_PAGE, terms=True)
        # La pagination est un peu artisanale, mais je n'ai pas trouvé comment naviguer dans des éléments whoosh
        prev, next = False, False
        if page > 1:
            prev = True
        if page <= len(results) / PERSONNES_PAR_PAGE:
            next = True
        titre = "Résultat pour la recherche `" + motclef.replace('*', '') + "` dans la classe " + attribut
        return render_template("pages/recherche.html", nom="Homines Devesseti", resultats=results, titre=titre,
                               keyword=motclef, next=next, prev=prev, page=page, attribut=attribut)
