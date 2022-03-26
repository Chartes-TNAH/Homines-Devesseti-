from flask import render_template, request, url_for, jsonify
from urllib.parse import urlencode
from ..app import app
from ..constantes import PERSONNES_PAR_PAGE, API_ROUTE
from ..modeles.donnees import Personnes, DetailPossessions, DetailRedevances, Reconnaissances, Repertoire

#Fonction prédéfinie pour l'affichage des données en JSON:

def Json_404():
    response = jsonify({"erreur": "Unable to perform the query"})
    response.status_code = 404
    return response

#Reprise de mes routes génériques pour les adapter en api :

@app.route(API_ROUTE + "/name/<int:name_id>")
def api_name_single(name_id):
    try:
        hommes = Personnes.query.order_by(Personnes.id).all()
        query_name = hommes[name_id - 1]
        return jsonify(query_name.to_jsonapi_name())
    except:
        return Json_404()


@app.route(API_ROUTE + "/dp/<int:dp_id>")
def api_dp_single(dp_id):
    try:
        dets_pos = DetailPossessions.query.order_by(DetailPossessions.id_detail_possession).all()
        query_dp = dets_pos[dp_id - 1]
        return jsonify(query_dp.to_jsonapi_dp())
    except:
        return Json_404()

@app.route(API_ROUTE + "/dr/<int:dr_id>")
def api_dr_single(dr_id):
    try:
        dets_red = DetailRedevances.query.order_by(DetailRedevances.id_detail_redevance).all()
        query_dr = dets_red[dr_id - 1]
        return jsonify(query_dr.to_jsonapi_dr())
    except:
        return Json_404()

@app.route(API_ROUTE + "/rec/<int:rec_id>")
def api_rec_single(rec_id):
    try:
        recs = Reconnaissances.query.outerjoin(Repertoire).order_by(Reconnaissances.id_reconnaissance).all()
        query_rec = list(filter(lambda rec: rec.id_reconnaissance == rec_id, recs))[0]
        #Code pour injecter des données lorsque la jointure ne se fait pas avec la table Répertoire:
        if not query_rec.page:
            query_rec.page = [Repertoire(
            id_reconnaissance="Inconnue",
            ref_du_terrier="Inconnue"
        )]
        return jsonify(reconnaissance=query_rec.to_jsonapi_rec())
    except:
        return Json_404()

@app.route(API_ROUTE + "/search")
def api_name_search():
    motclef = request.args.get("q", None)
    page = request.args.get("page", 1)
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    if motclef:
        query = Personnes.query.filter(
            Personnes.nom.like("%{}%".format(motclef))
        )
    else:
        query = Personnes.query
    try:
        resultats = query.paginate(page=page, per_page=PERSONNES_PAR_PAGE)
    except Exception:
        return Json_404()
    dict_resultats = {
        "links": {
            "self": request.url
        },
        "data": [
            homme.to_jsonapi_name()
            for homme in resultats.items
        ]
    }
    if resultats.has_next:
        arguments = {
            "page": resultats.next_num
        }
        if motclef:
            arguments["q"] = motclef
        dict_resultats["links"]["next"] = url_for("api_name_search", _external=True) + "?" + urlencode(arguments)
    if resultats.has_prev:
        arguments = {
            "page": resultats.prev_num
        }
        if motclef:
            arguments["q"] = motclef
        dict_resultats["links"]["prev"] = url_for("api_name_search", _external=True) + "?" + urlencode(arguments)
    response = jsonify(dict_resultats)
    return response
