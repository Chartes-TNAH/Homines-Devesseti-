from flask import render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from .generic import generate_index, formulaire
from ..app import app, login, db
from ..modeles.donnees import Personnes, Reconnaissances, Repertoire, DetailRedevances, \
    DetailPossessions, Authorship, Charte

#Mise à jour :
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
                reco.totalAvoine = request.form["recAvoine"]
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

    if updated == False:
        return render_template(
            "pages/update/reconnaissances_update.html",
            nom="Gazetteer",
            rec=reco,
            mois=mois,
            corvees=corvees,
            updated=updated,
            page=page
        )
    else:
        return formulaire(updated=updated)

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
    if updated == False:
        return render_template(
            "pages/update/detail_possessions_update.html",
            nom="Gazetteer",
            det_pos=dp,
            updated=updated
        )
    else:
        return formulaire(updated=updated)

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
    if updated == False:
        return render_template(
            "pages/update/detail_redevances_update.html",
            nom="Gazetteer",
            det_red=dr,
            updated=updated
        )
    else:
        return formulaire(updated=updated)

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
            # Mise à jour des tables :
            db.session.add(homme)
            db.session.add(Authorship(personnes=homme, user=current_user))
            db.session.commit()
            updated = True
        else:
            print(erreurs)
    if updated == False:
        return render_template(
            "pages/update/noms_update.html",
            nom="Gazetteer",
            homme=homme,
            sexes=sexes,
            updated=updated
        )
    else:
        return generate_index(updated=updated)  # permet de maj l'index automatiquement à chaque modification

@app.route("/charte_homme/<int:name_id>/update", methods=["GET", "POST"])
@login_required
def charte_homme_update(name_id):
    homme = Charte.query.get_or_404(name_id)
    erreurs = []
    updated = False
    if request.method == "POST":
        if not request.form.get("hommePrenom", "").strip():
            erreurs.append("hommePrenom")
        if not request.form.get("hommeNom", "").strip():
            erreurs.append("hommeNom")
        if not erreurs:
            if request.form["hommePrenom"] != "None":
                homme.prenom = request.form["hommePrenom"]
            if request.form["hommeNom"] != "None":
                homme.nom = request.form["hommeNom"]
            # Mise à jour des tables :
            db.session.add(homme)
            db.session.add(Authorship(charte=homme, user=current_user))
            db.session.commit()
            updated = True
        else:
            print(erreurs)
    if updated == False:
        return render_template(
            "pages/update/charte_homme_update.html",
            nom="Gazetteer",
            homme=homme,
            updated=updated
        )
    else:
        return formulaire(updated=updated)

#Création données :
@app.route("/name/create", methods=["GET", "POST"])
@login_required
def name_create():
    sexes = [
        x for (x, *_) in db.session.query(Personnes.genre).distinct()
    ]
    erreurs = []
    updated = False
    if request.method == "POST":
        if not request.form.get("hommeReco", "").strip():
            erreurs.append("hommeReco")
        if request.form["hommeSexe"] not in sexes:
            erreurs.append("hommeSexe")
        if not erreurs:
            prenom = request.form["hommePrenom"]
            nom = request.form["hommeNom"]
            genre = request.form["hommeSexe"]
            id_reconnaissance = request.form["hommeReco"]
            localite = request.form["hommeLieu"]
            precision_sur_origine = request.form["hommePrecisionLieu"]
            informations_personnelles = request.form["hommeInfo"]
            #Mise à jour des tables :
            homme = Personnes(
                prenom=prenom,
                nom=nom,
                genre=genre,
                id_reconnaissance=id_reconnaissance,
                localite=localite,
                precision_sur_origine=precision_sur_origine,
                informations_personnelles=informations_personnelles
            )
            db.session.add(homme)
            db.session.add(Authorship(personnes=homme, user=current_user))
            db.session.commit()
            updated = True
        else:
            print(erreurs)
    if updated == False:
        return render_template(
            "pages/update/noms_create.html",
            nom="Gazetteer",
            sexes=sexes,
        )
    else:
        return generate_index(updated=updated) #permet de maj l'index automatiquement à chaque modification

@app.route("/dr/create", methods=["GET", "POST"])
@login_required
def det_red_create():
    updated = False
    erreurs = []
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
        if not erreurs:
            id_reconnaissance = request.form["drReco"]
            cens_en_poules = request.form["drPoules"]
            totalSeigle = request.form["drSeigle"]
            totalAvoine = request.form["drAvoine"]
            total_monnaie = request.form["drMonnaie"]
            pro = request.form["drBien"]
            nom = request.form["drNom"]
            lieu = request.form["drLieu"]
            supplement = request.form["drInfo"]
            # Mise à jour des tables :
            dr = DetailRedevances(
                id_reconnaissance=id_reconnaissance,
                cens_en_poule=cens_en_poules,
                totalSeigle=totalSeigle,
                totalAvoine=totalAvoine,
                total_monnaie=total_monnaie,
                pro=pro,
                nom=nom,
                lieu=lieu,
                supplement=supplement
            )
            db.session.add(dr)
            db.session.add(Authorship(detail_redevances=dr, user=current_user))
            db.session.commit()
            updated = True
    if updated == False:
        return render_template(
            "pages/update/detail_redevances_create.html",
            nom="Gazetteer",
        )
    else:
        return formulaire(updated=updated)

@app.route("/dp/create", methods=["GET", "POST"])
@login_required
def det_pos_create():
    updated = False
    erreurs = []
    if request.method == "POST":
        if not request.form.get("dpReco", "").strip():
            erreurs.append("dpReco")
        if not erreurs:
            id_reconnaissance = request.form["dpReco"]
            personne_concernee = request.form["dpPersonne"]
            possession = request.form["dpPossession"]
            nom = request.form["dpNom"]
            lieu = request.form["dpLieu"]
            supplement = request.form["dpInfo"]
            confront1 = request.form["dpConfront1"]
            confront2 = request.form["dpConfront2"]
            confront3 = request.form["dpConfront3"]
            confront4 = request.form["dpConfront4"]
            confront5 = request.form["dpConfront5"]
            confront6 = request.form["dpConfront6"]
            #Mise à jour des tables :
            dp = DetailPossessions(
                id_reconnaissance=id_reconnaissance,
                personne_concernee=personne_concernee,
                possession=possession,
                nom=nom,
                lieu=lieu,
                supplement=supplement,
                confront1=confront1,
                confront2=confront2,
                confront3=confront3,
                confront4=confront4,
                confront5=confront5,
                confront6=confront6,
            )
            db.session.add(dp)
            db.session.add(Authorship(detail_possessions=dp, user=current_user))
            db.session.commit()
            updated = True
    if updated == False:
        return render_template(
            "pages/update/detail_possessions_create.html",
            nom="Gazetteer",
        )
    else:
        return formulaire(updated=updated)

@app.route("/rec/create", methods=["GET", "POST"])
@login_required
def rec_create():
    #La logique des variables de cette route suit celle de la route précédente
    mois = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août',
            'Septembre', 'Octobre', 'Novembre', 'Décembre']
    corvees = [
        x for (x, *_) in db.session.query(Reconnaissances.manobrias).distinct()
    ]
    erreurs = []
    updated = False
    if request.method == "POST":
        if request.form["recMois"] not in mois:
            erreurs.append("recMois")
        if request.form["recManobrias"] not in corvees:
            erreurs.append("recManobrias")
        if request.form["recJornalia"] not in corvees:
            erreurs.append("recJornalia")
        if request.form["recChareis"] not in corvees:
            erreurs.append("recChareis")
        if not request.form.get("recId", "").strip():
            erreurs.append("recId")
        if not request.form.get("recCommandeur", "").strip():
            erreurs.append("recCommandeur")
        if not erreurs:
            id_reconnaissance = request.form["recId"]
            commandeur = request.form["recCommandeur"]
            ref_du_terrier = request.form["recPage"]
            notaire = request.form["recNotaire"]
            temoin1 = request.form["recTemoin1"]
            temoin2 = request.form["recTemoin2"]
            temoin3 = request.form["recTemoin3"]
            temoin4 = request.form["recTemoin4"]
            temoin5 = request.form["recTemoin5"]
            annee = request.form["recAnnee"]
            mois = request.form["recMois"]
            jour = request.form["recJour"]
            statut = request.form["recStatut"]
            implication_statut = request.form["recDetStatut"]
            manobrias = request.form["recManobrias"]
            jornalia = request.form["recJornalia"]
            chareis = request.form["recChareis"]
            complement_sur_Corvees = request.form["recComplementCorvees"]
            statut_terre = request.form["recStatutTerres"]
            domus = request.form["recDomus"]
            orti = request.form["recOrti"]
            prata = request.form["recPrata"]
            compos = request.form["recCompos"]
            nemora = request.form["recNemora"]
            pascua = request.form["recPascua"]
            pasturalia = request.form["recPasturalia"]
            terrae = request.form["recTerrae"]
            casalia = request.form["recCasalia"]
            casamenta = request.form["recCasamenta"]
            grangiae = request.form["recGrangiae"]
            denesia = request.form["recDenesia"]
            calma = request.form["recCalma"]
            assensa = request.form["recAssensa"]
            molendinus = request.form["recMolendinus"]
            ouchias = request.form["recOuchias"]
            garaitum = request.form["recGaraitum"]
            patile = request.form["recPatile"]
            hospicii = request.form["recHospicii"]
            petiae = request.form["recPetiae"]
            esclausae = request.form["recEsclausae"]
            terminus = request.form["recTerminus"]
            costam = request.form["recCostam"]
            sana = request.form["recSana"]
            tenementum = request.form["recTenementum"]
            versana = request.form["recVersana"]
            masacgio = request.form["recMasacgio"]
            vineae = request.form["recVineae"]
            blachia = request.form["recBlachia"]
            arbores = request.form["recArbores"]
            passetae = request.form["recPassetae"]
            chastanerii = request.form["recChastanerii"]
            levata = request.form["recLevata"]
            creysementum = request.form["recCreysementum"]
            bessaa = request.form["recBessaa"]
            besseta = request.form["recBesseta"]
            lameytenchada = request.form["recLameytenchada"]
            bealis = request.form["recBealis"]
            mansum = request.form["recMansum"]
            sanhassium = request.form["recSanhassium"]
            autres_possessions = request.form["recAutres"]
            lieux_terres = request.form["recLieu"]
            cens_en_poule = request.form["recPoules"]
            totalSeigle = request.form["recSeigle"]
            Avoine = request.form["recAvoine"]
            total_sous_tournois = request.form["recMonnaie"]
            mesure_de_cereale_utilisee = request.form["recMesure"]
            jour_paiement = request.form["recJourPaiement"]
            type_de_Juridiction = request.form["recJuridiction"]
            mandement = request.form["recMandement"]
            #Mise à jour des tables :
            reco = Reconnaissances(
            id_reconnaissance = id_reconnaissance,
            commandeur = commandeur,
            notaire = notaire,
            temoin1 = temoin1,
            temoin2 = temoin2,
            temoin3 = temoin3,
            temoin4 = temoin4,
            temoin5 = temoin5,
            annee = annee,
            mois = mois,
            jour = jour,
            statut = statut,
            implication_statut = implication_statut,
            manobrias = manobrias,
            jornalia = jornalia,
            chareis = chareis,
            complement_sur_Corvees = complement_sur_Corvees,
            statut_terre = statut_terre,
            domus = domus,
            orti = orti,
            prata = prata,
            compos = compos,
            nemora = nemora,
            pascua = pascua,
            pasturalia = pasturalia,
            terrae = terrae,
            casalia = casalia,
            casamenta = casamenta,
            grangiae = grangiae,
            denesia = denesia,
            calma = calma,
            assensa = assensa,
            molendinus = molendinus,
            ouchias = ouchias,
            garaitum = garaitum,
            patile = patile,
            hospicii = hospicii,
            petiae = petiae,
            esclausae = esclausae,
            terminus = terminus,
            costam = costam,
            sana = sana,
            tenementum = tenementum,
            versana = versana,
            masacgio = masacgio,
            vineae = vineae,
            blachia = blachia,
            arbores = arbores,
            passetae = passetae,
            chastanerii = chastanerii,
            levata = levata,
            creysementum = creysementum,
            bessaa = bessaa,
            besseta = besseta,
            lameytenchada = lameytenchada,
            bealis = bealis,
            mansum = mansum,
            sanhassium = sanhassium,
            autres_possessions = autres_possessions,
            lieux_terres = lieux_terres,
            cens_en_poule = cens_en_poule,
            totalSeigle = totalSeigle,
            totalAvoine = Avoine,
            total_sous_tournois = total_sous_tournois,
            mesure_de_cereale_utilisee = mesure_de_cereale_utilisee,
            jour_paiement = jour_paiement,
            type_de_Juridiction = type_de_Juridiction,
            mandement = mandement
            )
            db.session.add(reco)
            if ref_du_terrier:
                db.session.add(page, ref_du_terrier=ref_du_terrier)
            db.session.add(Authorship(reconnaissances=reco, user=current_user))
            db.session.commit()
            updated = True
        else:
            print(erreurs)
    if updated == False:
        return render_template(
            "pages/update/reconnaissances_create.html",
            nom="Gazetteer",
            mois=mois,
            corvees=corvees,
        )
    else:
        return formulaire(updated=updated)

@app.route("/charte_homme/create", methods=["GET", "POST"])
@login_required
def charte_homme_create():
    updated = False
    if request.method == "POST":
        prenom = request.form["hommePrenom"]
        nom = request.form["hommeNom"]
        #Mise à jour des tables :
        homme = Charte(
            prenom=prenom,
            nom=nom,
        )
        db.session.add(homme)
        db.session.add(Authorship(charte=homme, user=current_user))
        db.session.commit()
        updated = True
    if updated == False:
        return render_template(
            "pages/update/charte_homme_create.html",
            nom="Gazetteer",
        )
    else:
        return formulaire(updated=updated)

@app.route("/<d>/<int:n>/delete", methods=["GET", "POST"])
@login_required
def delete(d, n):
    data = [["name", "dp", "dr", "rec", "charte_homme"], [Personnes, DetailPossessions, DetailRedevances,
                                                          Reconnaissances, Charte]]
    page = []
    try:
        table = data[1][data[0].index(d)]
        if d == "rec":
            ligne = list(filter(lambda r: r.id_reconnaissance == n, Reconnaissances.query.all()))[0]
            if ligne.page:
                page = list(filter(lambda p: p.id_reconnaissance == n, Repertoire.query.all()))[0]
        else:
            ligne = table.query.get(n)
        db.session.delete(ligne)
        if d == "rec":
            db.session.add(Authorship(reconnaissances=ligne, user=current_user))
        elif d == "dp":
            db.session.add(Authorship(detail_possessions=ligne, user=current_user))
        elif d == "dr":
            db.session.add(Authorship(detail_redevances=ligne, user=current_user))
        elif d == "name":
            db.session.add(Authorship(personnes=ligne, user=current_user))
        elif d == "charte_homme":
            db.session.add(Authorship(charte=ligne, user=current_user))
        if page:
            db.session.delete(page)
        db.session.commit()
        if d == "name":
            return generate_index(updated=True)
        else:
            return formulaire(updated=True)
    except:
        if d == "name":
            return redirect(url_for("name_update", name_id=n))
        elif d == "rec":
            return redirect(url_for("rec_update", rec_id=n))
        elif d == "dp":
            return redirect(url_for("det_pos_update", dp_id=n))
        elif d == "dr":
            return redirect(url_for("det_red_update", dr_id=n))
        elif d == "charte_homme":
            return redirect(url_for("charte_homme_update", dr_id=n))

@app.route("/participer")
def participer():
    return render_template("pages/update/participer.html")