from flask import render_template, request, url_for, jsonify
from urllib.parse import urlencode

from ..app import app
from ..constantes import LIEUX_PAR_PAGE, API_ROUTE
from ..modeles.donnees import Personnes, DetailPossessions, DetailRedevances, Reconnaissances, Repertoire
from .generic import hommes, dets_pos, dets_red, recs


def Json_404():
    response = jsonify({"erreur": "Unable to perform the query"})
    response.status_code = 404
    return response

#Reprise de mes routes génériques pour les adapter en api :

@app.route(API_ROUTE + "/name/<int:name_id>")
def api_name_single(name_id):
    try:
        query_name = hommes[name_id - 1]
        return jsonify(query_name.to_jsonapi_name())
    except:
        return Json_404()


@app.route(API_ROUTE + "/dp/<int:dp_id>")
def api_dp_single(dp_id):
    try:
        query_dp = dets_pos[dp_id - 1]
        return jsonify(query_dp.to_jsonapi_dp())
    except:
        return Json_404()

@app.route(API_ROUTE + "/dr/<int:dr_id>")
def api_dr_single(dr_id):
    try:
        query_dr = dets_red[dr_id - 1]
        return jsonify(query_dr.to_jsonapi_dr())
    except:
        return Json_404()

@app.route(API_ROUTE + "/rec/<int:rec_id>")
def api_rec_single(rec_id):
    try:
        query_rec = list(filter(lambda rec: rec.id_reconnaissance == rec_id, recs))[0]
        return jsonify(query_rec.to_jsonapi_rec())
    except:
        return Json_404()

@app.route(API_ROUTE + "/name")
def api_name_browse():
    """ Route permettant la recherche plein-texte

    On s'inspirera de http://jsonapi.org/ faute de pouvoir trouver temps d'y coller à 100%
    """
    # q est très souvent utilisé pour indiquer une capacité de recherche
    motclef = request.args.get("q", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    if motclef:
        query = Place.query.filter(
            Personnes.nom.like("%{}%".format(motclef))
        )
    else:
        query = Personnes.query

    try:
        resultats = query.paginate(page=page, per_page=LIEUX_PAR_PAGE)
    except Exception:
        return Json_404()

    dict_resultats = {
        "links": {
            "self": request.url
        },
        "data": [
            place.to_jsonapi_dict()
            for place in resultats.items
        ]
    }

    if resultats.has_next:
        arguments = {
            "page": resultats.next_num
        }
        if motclef:
            arguments["q"] = motclef
        dict_resultats["links"]["next"] = url_for("api_places_browse", _external=True) + "?" + urlencode(arguments)

    if resultats.has_prev:
        arguments = {
            "page": resultats.prev_num
        }
        if motclef:
            arguments["q"] = motclef
        dict_resultats["links"]["prev"] = url_for("api_places_browse", _external=True) + "?" + urlencode(arguments)

    response = jsonify(dict_resultats)
    return response