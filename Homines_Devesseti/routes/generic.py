from flask import render_template, request, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required

from ..app import app, login, db
from ..modeles.donnees import Personnes, Reconnaissances, Repertoire, DetailRedevances, DetailPossessions, Authorship
from ..modeles.utilisateurs import User
from ..constantes import PERSONNES_PAR_PAGE

#Routes de base :
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

#Routes permettant l'affichage des données du terrier :
@app.route("/name/<int:name_id>")
def nom(name_id):
    hommes = Personnes.query.order_by(Personnes.id).all()
    nbr_hommes = hommes[-1].id
    return render_template("pages/noms.html", nom="Homines Devesseti", homme=hommes[name_id - 1], nbr=nbr_hommes)
#On enlève systématiquement 1 à l'index car Python fait commencer le sien à 0

@app.route("/dp/<int:dp_id>")
def det_pos(dp_id):
    dets_pos = DetailPossessions.query.order_by(DetailPossessions.id_detail_possession).all()
    nbr_det_pos = dets_pos[-1].id_detail_possession
    return render_template("pages/detail_possessions.html", nom="Homines Devesseti", det_pos=dets_pos[dp_id - 1], nbr=nbr_det_pos)

@app.route("/dr/<int:dr_id>")
def det_red(dr_id):
    dets_red = DetailRedevances.query.order_by(DetailRedevances.id_detail_redevance).all()
    nbr_det_red = dets_red[-1].id_detail_redevance
    return render_template("pages/detail_redevances.html", nom="Homines Devesseti", det_red=dets_red[dr_id - 1], nbr=nbr_det_red)

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

#Routes permettant de réaliser des updates :
@app.route("/rec/<int:rec_id>/update", methods=["GET", "POST"])
@login_required
def rec_update(rec_id):
    reco = list(filter(lambda rec: rec.id_reconnaissance == rec_id, Reconnaissances.query.all()))[0]
    page = []
    if reco.page:
        page = list(filter(lambda p: p.id_reconnaissance == rec_id, Repertoire.query.all()))[0]
    #La logique des variables de cette route suit celle de la route précédente
    mois = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août',
            'Septembre', 'Octobre', 'Novembre', 'Décembre']
    corvees = [
        x for (x, *_) in db.session.query(Reconnaissances.manobrias).distinct()
    ]
    erreurs = []
    updated = False
    if request.method == "POST":
        if reco.page:
            if not request.form.get("recPage", "").strip():
                erreurs.append("recPage")
        if not request.form.get("recNotaire", "").strip():
            erreurs.append("recNotaire")
        if not request.form.get("recTemoin1", "").strip():
            erreurs.append("recTemoin1")
        if not request.form.get("recTemoin2", "").strip():
            erreurs.append("recTemoin2")
        if not request.form.get("recTemoin3", "").strip():
            erreurs.append("recTemoin3")
        if not request.form.get("recTemoin4", "").strip():
            erreurs.append("recTemoin4")
        if not request.form.get("recTemoin5", "").strip():
            erreurs.append("recTemoin5")
        if not request.form.get("recAnnee", "").strip():
            erreurs.append("recAnnee")
        if not request.form.get("recMois", "").strip():
            erreurs.append("recMois")
        elif request.form["recMois"] not in mois:
            erreurs.append("recMois")
        if not request.form.get("recJour", "").strip():
            erreurs.append("recJour")
        if not request.form.get("recStatut", "").strip():
            erreurs.append("recStatut")
        if not request.form.get("recDetStatut", "").strip():
            erreurs.append("recDetStatut")
        if not request.form.get("recManobrias", "").strip():
            erreurs.append("recManobrias")
        elif request.form["recManobrias"] not in corvees:
            erreurs.append("recManobrias")
        if not request.form.get("recJornalia", "").strip():
            erreurs.append("recJornalia")
        elif request.form["recJornalia"] not in corvees:
            erreurs.append("recJornalia")
        if not request.form.get("recChareis", "").strip():
            erreurs.append("recChareis")
        elif request.form["recChareis"] not in corvees:
            erreurs.append("recChareis")
        if not request.form.get("recComplementCorvees", "").strip():
            erreurs.append("recComplementCorvees")
        if not request.form.get("recStatutTerres", "").strip():
            erreurs.append("recStatutTerres")
        if not request.form.get("recDomus", "").strip():
            erreurs.append("recDomus")
        if not request.form.get("recOrti", "").strip():
            erreurs.append("recOrti")
        if not request.form.get("recPrata", "").strip():
            erreurs.append("recPrata")
        if not request.form.get("recCompos", "").strip():
            erreurs.append("recCompos")
        if not request.form.get("recNemora", "").strip():
            erreurs.append("recNemora")
        if not request.form.get("recPascua", "").strip():
            erreurs.append("recPascua")
        if not request.form.get("recPasturalia", "").strip():
            erreurs.append("recPasturalia")
        if not request.form.get("recTerrae", "").strip():
            erreurs.append("recTerrae")
        if not request.form.get("recCasalia", "").strip():
            erreurs.append("recCasalia")
        if not request.form.get("recCasamenta", "").strip():
            erreurs.append("recCasamenta")
        if not request.form.get("recGrangiae", "").strip():
            erreurs.append("recGrangiae")
        if not request.form.get("recDenesia", "").strip():
            erreurs.append("recDenesia")
        if not request.form.get("recCalma", "").strip():
            erreurs.append("recCalma")
        if not request.form.get("recAssensa", "").strip():
            erreurs.append("recAssensa")
        if not request.form.get("recMolendinus", "").strip():
            erreurs.append("recMolendinus")
        if not request.form.get("recOuchias", "").strip():
            erreurs.append("recOuchias")
        if not request.form.get("recGaraitum", "").strip():
            erreurs.append("recGaraitum")
        if not request.form.get("recPatile", "").strip():
            erreurs.append("recPatile")
        if not request.form.get("recHospicii", "").strip():
            erreurs.append("recHospicii")
        if not request.form.get("recPetiae", "").strip():
            erreurs.append("recPetiae")
        if not request.form.get("recEsclausae", "").strip():
            erreurs.append("recEsclausae")
        if not request.form.get("recTerminus", "").strip():
            erreurs.append("recTerminus")
        if not request.form.get("recCostam", "").strip():
            erreurs.append("recCostam")
        if not request.form.get("recSana", "").strip():
            erreurs.append("recSana")
        if not request.form.get("recTenementum", "").strip():
            erreurs.append("recTenementum")
        if not request.form.get("recVersana", "").strip():
            erreurs.append("recVersana")
        if not request.form.get("recMasacgio", "").strip():
            erreurs.append("recMasacgio")
        if not request.form.get("recVineae", "").strip():
            erreurs.append("recVineae")
        if not request.form.get("recBlachia", "").strip():
            erreurs.append("recBlachia")
        if not request.form.get("recArbores", "").strip():
            erreurs.append("recArbores")
        if not request.form.get("recPassetae", "").strip():
            erreurs.append("recPassetae")
        if not request.form.get("recChastanerii", "").strip():
            erreurs.append("recChastanerii")
        if not request.form.get("recLevata", "").strip():
            erreurs.append("recLevata")
        if not request.form.get("recCreysementum", "").strip():
            erreurs.append("recCreysementum")
        if not request.form.get("recBessaa", "").strip():
            erreurs.append("recBessaa")
        if not request.form.get("recBesseta", "").strip():
            erreurs.append("recBesseta")
        if not request.form.get("recLameytenchada", "").strip():
            erreurs.append("recLameytenchada")
        if not request.form.get("recBealis", "").strip():
            erreurs.append("recBealis")
        if not request.form.get("recMansum", "").strip():
            erreurs.append("recMansum")
        if not request.form.get("recSanhassium", "").strip():
            erreurs.append("recSanhassium")
        if not request.form.get("recAutres", "").strip():
            erreurs.append("recAutres")
        if not request.form.get("recLieu", "").strip():
            erreurs.append("recLieu")
        if not request.form.get("recPoules", "").strip():
            erreurs.append("recPoules")
        if not request.form.get("recSeigle", "").strip():
            erreurs.append("recSeigle")
        if not request.form.get("recAvoine", "").strip():
            erreurs.append("recAvoine")
        if not request.form.get("recMonnaie", "").strip():
            erreurs.append("recMonnaie")
        if not request.form.get("recMesure", "").strip():
            erreurs.append("recMesure")
        if not request.form.get("recJourPaiement", "").strip():
            erreurs.append("recJourPaiement")
        if not request.form.get("recJuridiction", "").strip():
            erreurs.append("recJuridiction")
        if not request.form.get("recMandement", "").strip():
            erreurs.append("recMandement")
        if not erreurs:
            if reco.page:
                page.ref_du_terrier = request.form["recPage"]
            if request.form["recNotaire"] != "None":
                reco.notaire = request.form["recNotaire"]
            if request.form["recTemoin1"] != "None":
                reco.temoin1 = request.form["recTemoin1"]
            if request.form["recTemoin2"] != "None":
                reco.temoin2 = request.form["recTemoin2"]
            if request.form["recTemoin3"] != "None":
                reco.temoin3 = request.form["recTemoin3"]
            if request.form["recTemoin4"] != "None":
                reco.temoin4 = request.form["recTemoin4"]
            if request.form["recTemoin5"] != "None":
                reco.temoin5 = request.form["recTemoin5"]
            if request.form["recAnnee"] != "None":
                reco.annee = request.form["recAnnee"]
            if request.form["recMois"] != "None":
                reco.mois = request.form["recMois"]
            if request.form["recJour"] != "None":
                reco.jour = request.form["recJour"]
            if request.form["recStatut"] != "None":
                reco.statut = request.form["recStatut"]
            if request.form["recDetStatut"] != "None":
                reco.implication_statut = request.form["recDetStatut"]
            if request.form["recManobrias"] != "None":
                reco.manobrias = request.form["recManobrias"]
            if request.form["recJornalia"] != "None":
                reco.jornalia = request.form["recJornalia"]
            if request.form["recChareis"] != "None":
                reco.chareis = request.form["recChareis"]
            if request.form["recComplementCorvees"] != "None":
                reco.complement_sur_corvees = request.form["recComplementCorvees"]
            if request.form["recStatutTerres"] != "None":
                reco.statut_terre = request.form["recStatutTerres"]
            if request.form["recDomus"] != "None":
                reco.domus = request.form["recDomus"]
            if request.form["recOrti"] != "None":
                reco.orti = request.form["recOrti"]
            if request.form["recPrata"] != "None":
                reco.prata = request.form["recPrata"]
            if request.form["recCompos"] != "None":
                reco.compos = request.form["recCompos"]
            if request.form["recNemora"] != "None":
                reco.nemora = request.form["recNemora"]
            if request.form["recPascua"] != "None":
                reco.pascua = request.form["recPascua"]
            if request.form["recPasturalia"] != "None":
                reco.pasturalia = request.form["recPasturalia"]
            if request.form["recTerrae"] != "None":
                reco.terrae = request.form["recTerrae"]
            if request.form["recCasalia"] != "None":
                reco.casalia = request.form["recCasalia"]
            if request.form["recCasamenta"] != "None":
                reco.casamenta = request.form["recCasamenta"]
            if request.form["recGrangiae"] != "None":
                reco.grangiae = request.form["recGrangiae"]
            if request.form["recDenesia"] != "None":
                reco.denesia = request.form["recDenesia"]
            if request.form["recCalma"] != "None":
                reco.calma = request.form["recCalma"]
            if request.form["recAssensa"] != "None":
                reco.assensa = request.form["recAssensa"]
            if request.form["recMolendinus"] != "None":
                reco.molendinus = request.form["recMolendinus"]
            if request.form["recOuchias"] != "None":
                reco.ouchias = request.form["recOuchias"]
            if request.form["recGaraitum"] != "None":
                reco.garaitum = request.form["recGaraitum"]
            if request.form["recPatile"] != "None":
                reco.patile = request.form["recPatile"]
            if request.form["recHospicii"] != "None":
                reco.hospicii = request.form["recHospicii"]
            if request.form["recPetiae"] != "None":
                reco.petiae = request.form["recPetiae"]
            if request.form["recEsclausae"] != "None":
                reco.esclausae = request.form["recEsclausae"]
            if request.form["recTerminus"] != "None":
                reco.terminus = request.form["recTerminus"]
            if request.form["recCostam"] != "None":
                reco.costam = request.form["recCostam"]
            if request.form["recSana"] != "None":
                reco.sana = request.form["recSana"]
            if request.form["recTenementum"] != "None":
                reco.tenementum = request.form["recTenementum"]
            if request.form["recVersana"] != "None":
                reco.versana = request.form["recVersana"]
            if request.form["recMasacgio"] != "None":
                reco.masacgio = request.form["recMasacgio"]
            if request.form["recVineae"] != "None":
                reco.vineae = request.form["recVineae"]
            if request.form["recBlachia"] != "None":
                reco.blachia = request.form["recBlachia"]
            if request.form["recArbores"] != "None":
                reco.arbores = request.form["recArbores"]
            if request.form["recPassetae"] != "None":
                reco.passetae = request.form["recPassetae"]
            if request.form["recChastanerii"] != "None":
                reco.chastanerii = request.form["recChastanerii"]
            if request.form["recLevata"] != "None":
                reco.levata = request.form["recLevata"]
            if request.form["recCreysementum"] != "None":
                reco.creysementum = request.form["recCreysementum"]
            if request.form["recBessaa"] != "None":
                reco.bessaa = request.form["recBessaa"]
            if request.form["recBesseta"] != "None":
                reco.besseta = request.form["recBesseta"]
            if request.form["recLameytenchada"] != "None":
                reco.lameytenchada = request.form["recLameytenchada"]
            if request.form["recBealis"] != "None":
                reco.bealis = request.form["recBealis"]
            if request.form["recMansum"] != "None":
                reco.mansum = request.form["recMansum"]
            if request.form["recSanhassium"] != "None":
                reco.sanhassium = request.form["recSanhassium"]
            if request.form["recAutres"] != "None":
                reco.autres_possessions = request.form["recAutres"]
            if request.form["recLieu"] != "None":
                reco.lieux_terres = request.form["recLieu"]
            if request.form["recPoules"] != "None":
                reco.cens_en_poule = request.form["recPoules"]
            if request.form["recSeigle"] != "None":
                reco.totalSeigle = request.form["recSeigle"]
            if request.form["recAvoine"] != "None":
                reco.Avoine = request.form["recAvoine"]
            if request.form["recMonnaie"] != "None":
                reco.total_sous_tournois = request.form["recMonnaie"]
            if request.form["recMesure"] != "None":
                reco.mesure_de_cereale_utilisee = request.form["recMesure"]
            if request.form["recJourPaiement"] != "None":
                reco.jour_paiement = request.form["recJourPaiement"]
            if request.form["recJuridiction"] != "None":
                reco.juridiction = request.form["recJuridiction"]
            if request.form["recMandement"] != "None":
                reco.mandement = request.form["recMandement"]
            #Mise à jour des tables :
            db.session.add(reco)
            if rec.page:
                db.session.add(page)
            db.session.add(Authorship(reconnaissances=reco, user=current_user))
            db.session.commit()
            updated = True
        else:
            print(erreurs)
    return render_template(
        "pages/reconnaissances_update.html",
        nom="Gazetteer",
        rec=reco,
        mois=mois,
        corvees=corvees,
        updated=updated,
        page=page
    )

@app.route("/dp/<int:dp_id>/update", methods=["GET", "POST"])
@login_required
def det_pos_update(dp_id):
    dp = DetailPossessions.query.get_or_404(dp_id)
    erreurs = []
    updated = False
    if request.method == "POST":
        if not request.form.get("dpReco", "").strip():
            erreurs.append("dpReco")
        if not request.form.get("dpPersonne", "").strip():
            erreurs.append("dpPersonne")
        if not request.form.get("dpPossession", "").strip():
            erreurs.append("dpPossession")
        if not request.form.get("dpNom", "").strip():
            erreurs.append("dpNom")
        if not request.form.get("dpLieu", "").strip():
            erreurs.append("dpLieu")
        if not request.form.get("dpInfo", "").strip():
            erreurs.append("dpInfo")
        if not request.form.get("dpConfront1", "").strip():
            erreurs.append("dpConfront1")
        if not request.form.get("dpConfront2", "").strip():
            erreurs.append("dpConfront2")
        if not request.form.get("dpConfront3", "").strip():
            erreurs.append("dpConfront3")
        if not request.form.get("dpConfront4", "").strip():
            erreurs.append("dpConfront4")
        if not request.form.get("dpConfront5", "").strip():
            erreurs.append("dpConfront5")
        if not request.form.get("dpConfront6", "").strip():
            erreurs.append("dpConfront6")
        if not erreurs:
            if request.form["dpReco"] != "None":
                dp.id_reconnaissance = request.form["dpReco"]
            if request.form["dpPersonne"] != "None":
                dp.personne_concernee = request.form["dpPersonne"]
            if request.form["dpPossession"] != "None":
                dp.possession = request.form["dpPossession"]
            if request.form["dpNom"] != "None":
                dp.nom = request.form["dpNom"]
            if request.form["dpLieu"] != "None":
                dp.lieu = request.form["dpLieu"]
            if request.form["dpInfo"] != "None":
                dp.supplement = request.form["dpInfo"]
            if request.form["dpConfront1"] != "None":
                dp.confront1 = request.form["dpConfront1"]
            if request.form["dpConfront2"] != "None":
                dp.confront2 = request.form["dpConfront2"]
            if request.form["dpConfront3"] != "None":
                dp.confront3 = request.form["dpConfront3"]
            if request.form["dpConfront4"] != "None":
                dp.confront4 = request.form["dpConfront4"]
            if request.form["dpConfront5"] != "None":
                dp.confront5 = request.form["dpConfront5"]
            if request.form["dpConfront6"] != "None":
                dp.confront6 = request.form["dpConfront6"]
            #Mise à jour des tables :
            db.session.add(dp)
            db.session.add(Authorship(detail_possessions=dp, user=current_user))
            db.session.commit()
            updated = True
        else:
            print(erreurs)
    return render_template(
        "pages/detail_possessions_update.html",
        nom="Gazetteer",
        det_pos=dp,
        updated=updated
    )

@app.route("/dr/<int:dr_id>/update", methods=["GET", "POST"])
@login_required
def det_red_update(dr_id):
    dr = DetailRedevances.query.get_or_404(dr_id)
    erreurs = []
    updated = False
    if request.method == "POST":
        if not request.form.get("drReco", "").strip():
            erreurs.append("drReco")
        if not request.form.get("drPoules", "").strip():
            erreurs.append("drPoules")
        if not request.form.get("drSeigle", "").strip():
            erreurs.append("drSeigle")
        if not request.form.get("drAvoine", "").strip():
            erreurs.append("drAvoine")
        if not request.form.get("drMonnaie", "").strip():
            erreurs.append("drMonnaie")
        if not request.form.get("drBien", "").strip():
            erreurs.append("drBien")
        if not request.form.get("drNom", "").strip():
            erreurs.append("drNom")
        if not request.form.get("drLieu", "").strip():
            erreurs.append("drLieu")
        if not request.form.get("drInfo", "").strip():
            erreurs.append("drInfo")
        if not erreurs:
            if request.form["drReco"] != "None":
                dr.id_reconnaissance = request.form["drReco"]
            if request.form["drPoules"] != "None":
                dr.cens_en_poules = request.form["drPoules"]
            if request.form["drSeigle"] != "None":
                dr.totalSeigle = request.form["drSeigle"]
            if request.form["drAvoine"] != "None":
                dr.totalAvoine = request.form["drAvoine"]
            if request.form["drMonnaie"] != "None":
                dr.total_monnaie = request.form["drMonnaie"]
            if request.form["drBien"] != "None":
                dr.pro = request.form["drBien"]
            if request.form["drNom"] != "None":
                dr.nom = request.form["drNom"]
            if request.form["drLieu"] != "None":
                dr.lieu = request.form["drLieu"]
            if request.form["drInfo"] != "None":
                dr.supplement = request.form["drInfo"]
            #Mise à jour des tables :
            db.session.add(dr)
            db.session.add(Authorship(detail_redevances=dr, user=current_user))
            db.session.commit()
            updated = True
        else:
            print(erreurs)
    return render_template(
        "pages/detail_redevances_update.html",
        nom="Gazetteer",
        det_red=dr,
        updated=updated
    )

@app.route("/name/<int:name_id>/update", methods=["GET", "POST"])
@login_required
def name_update(name_id):
    homme = Personnes.query.get_or_404(name_id)
    sexes = [
        x for (x, *_) in db.session.query(Personnes.genre).distinct()
    ]
    erreurs = []
    updated = False
    if request.method == "POST":
        if not request.form.get("hommePrenom", "").strip():
            erreurs.append("hommePrenom")
        if not request.form.get("hommeNom", "").strip():
            erreurs.append("hommeNom")
        if not request.form.get("hommeSexe", "").strip():
            erreurs.append("hommeSexe")
        elif request.form["hommeSexe"] not in sexes:
            erreurs.append("hommeSexe")
        if not request.form.get("hommeReco", "").strip():
            erreurs.append("hommeReco")
        if not request.form.get("hommeLieu", "").strip():
            erreurs.append("hommeLieu")
        if not request.form.get("hommePrecisionLieu", "").strip():
            erreurs.append("hommePrecisionLieu")
        if not request.form.get("hommeInfo", "").strip():
            erreurs.append("hommeInfo")
        if not erreurs:
            if request.form["hommePrenom"] != "None":
                homme.prenom = request.form["hommePrenom"]
            if request.form["hommeNom"] != "None":
                homme.nom = request.form["hommeNom"]
            if request.form["hommeSexe"] != "None":
                homme.genre = request.form["hommeSexe"]
            if request.form["hommeReco"] != "None":
                homme.id_reconnaissance = request.form["hommeReco"]
            if request.form["hommeLieu"] != "None":
                homme.localite = request.form["hommeLieu"]
            if request.form["hommePrecisionLieu"] != "None":
                homme.precision_sur_origine = request.form["hommePrecisionLieu"]
            if request.form["hommeInfo"] != "None":
                homme.informations_personnelles = request.form["hommeInfo"]
            #Mise à jour des tables :
            db.session.add(homme)
            db.session.add(Authorship(personnes=homme, user=current_user))
            db.session.commit()
            updated = True
        else:
            print(erreurs)
    return render_template(
        "pages/noms_update.html",
        nom="Gazetteer",
        homme=homme,
        sexes=sexes,
        updated=updated
    )

#Routes concernant les comptes utilisateur
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
    flash("Vous êtes déconnecté-e", "info")
    return redirect("/")

#Intégration de la charte de Devesset
@app.route("/charte")
def charte():
    return render_template("charte/Devoir_charte_Devesset_python_accueil.html", nom="Homines Devesseti")

@app.route("/charte/paleo")
def charte_paleo():
    return render_template("charte/Devoir_charte_Devesset_python_allograph.html", nom="Homines Devesseti")

@app.route("/charte/norm")
def charte_norm():
    return render_template("charte/Devoir_charte_Devesset_python_norm.html", nom="Homines Devesseti")

@app.route("/charte/index")
def charte_index():
    return render_template("charte/Devoir_charte_Devesset_python_index.html", nom="Homines Devesseti")

@app.route("/formulaire")
def formulaire():
    attributs = ["nom", "prenom", "localité"]
    return render_template("pages/formulaire_recherche.html", nom="Homines Devesseti", attributs=attributs)

#Route pour mes recherches à facettes :
from whoosh import index, query
from whoosh.index import create_in
from whoosh.qparser import QueryParser
from ..models_whoosh import PageWhoosh

@app.route("/generate_index")
def generate_index():
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
    flash("Index régénéré", "info")
    return redirect("/formulaire")

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
        #La pagination est un peu artisanale, mais je n'ai pas trouvé comment naviguer dans des éléments whoosh
        prev, next = False, False
        if page > 1:
            prev = True
        if page <= len(results)/PERSONNES_PAR_PAGE:
            next = True
        titre = "Résultat pour la recherche `" + motclef.replace('*', '') + "` dans la classe " + attribut
        return render_template("pages/recherche.html", nom="Homines Devesseti", resultats=results, titre=titre,
                               keyword=motclef, next=next, prev=prev, page=page, attribut=attribut)