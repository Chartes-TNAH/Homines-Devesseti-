from flask import url_for
import datetime
from ..app import db

#Les tables correspondent au fichier SQLite, chacune est associée à un équivalent en JSON :

class Authorship(db.Model):
    __tablename__ = "authorship"
    authorship_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_charte_id = db.Column(db.Integer, db.ForeignKey('charte.id'))
    authorship_name_id = db.Column(db.Integer, db.ForeignKey('personnes.id'))
    authorship_dp_id = db.Column(db.Integer, db.ForeignKey('detail_possessions.id_detail_possession'))
    authorship_dr_id = db.Column(db.Integer, db.ForeignKey('detail_redevances.id_detail_redevance'))
    authorship_rec_id = db.Column(db.Integer, db.ForeignKey('reconnaissances.id'))
    authorship_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    authorship_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user = db.relationship("User", back_populates="authorships")
    personnes = db.relationship("Personnes", back_populates="authorships")
    detail_possessions = db.relationship("DetailPossessions", back_populates="authorships")
    detail_redevances = db.relationship("DetailRedevances", back_populates="authorships")
    reconnaissances = db.relationship("Reconnaissances", back_populates="authorships")
    charte = db.relationship("Charte", back_populates="authorships")

    def author_to_json(self):
        return {
            "author": self.user.to_jsonapi_user(),
            "on": self.authorship_date
        }

class DetailPossessions(db.Model):
    __tablename__ = 'detail_possessions'
    id_detail_possession = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    id_reconnaissance = db.Column(db.Integer, db.ForeignKey('reconnaissances.id_reconnaissance'), nullable=False)
    possession = db.Column(db.Text)
    nom = db.Column(db.Text)
    personne_concernee = db.Column(db.Text)
    lieu = db.Column(db.Text)
    confront1 = db.Column(db.Text)
    confront2 = db.Column(db.Text)
    confront3 = db.Column(db.Text)
    confront4 = db.Column(db.Text)
    confront5 = db.Column(db.Text)
    confront6 = db.Column(db.Text)
    supplement = db.Column(db.Text)
    reconnaissances = db.relationship("Reconnaissances", back_populates="detail_possessions")
    authorships = db.relationship("Authorship", back_populates="detail_possessions")

    def to_jsonapi_dp(self):
        return {
            "type": "déclaration de bien",
            "id": self.id_detail_possession,
            "attributes": {
                "reconnaissance": {
                    "id": self.id_reconnaissance,
                    "links": {
                        "page": url_for("rec", rec_id=self.id_reconnaissance, _external=True),
                        "json": url_for("api_rec_single", rec_id=self.id_reconnaissance, _external=True)
                    }
                },
                "personne_concernee": self.personne_concernee,
                "type_de_bien": self.possession,
                "nom": self.nom,
                "localisation": self.lieu,
                "information_complementaire": self.supplement,
                "confronts": [
                    self.confront1,
                    self.confront2,
                    self.confront3,
                    self.confront4,
                    self.confront5,
                    self.confront6
                ],
            },
             "links": {
                "self": url_for("det_pos", dp_id=self.id_detail_possession, _external=True),
                "json": url_for("api_dp_single", dp_id=self.id_detail_possession, _external=True)
            },
            "relationships": {
                 "editions": [
                     author.author_to_json()
                     for author in self.authorships
                 ]
            }
        }

class DetailRedevances(db.Model):
    __tablename__ = 'detail_redevances'
    id_detail_redevance = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    id_reconnaissance = db.Column(db.Integer, db.ForeignKey('reconnaissances.id_reconnaissance'), nullable=False)
    cens_en_poule = db.Column(db.Integer, nullable=False)
    totalSeigle = db.Column(db.Integer, nullable=False)
    totalAvoine = db.Column(db.Integer, nullable=False)
    total_monnaie = db.Column(db.Integer, nullable=False)
    pro = db.Column(db.Text)
    nom = db.Column(db.Text)
    lieu = db.Column(db.Text)
    supplement = db.Column(db.Text)
    reconnaissances = db.relationship("Reconnaissances", back_populates="detail_redevances")
    authorships = db.relationship("Authorship", back_populates="detail_redevances")

    def to_jsonapi_dr(self):
        return {
            "type": "redevance",
            "id": self.id_detail_redevance,
            "attributes": {
                "reconnaissance": {
                    "id": self.id_reconnaissance,
                    "links": {
                        "page": url_for("rec", rec_id=self.id_reconnaissance, _external=True),
                        "json": url_for("api_rec_single", rec_id=self.id_reconnaissance, _external=True)
                    }
                },
                "redevances_a_payer" :{
                    "poules": self.cens_en_poule,
                    "seigle":{
                        "mesure": "Setiers",
                        "valeur": self.totalSeigle
                    },
                    "avoine":{
                        "mesure": "Setiers",
                        "valeur": self.totalAvoine
                    },
                    "monnaie":{
                        "mesure": "Sous tournois",
                        "valeur": self.total_monnaie
                    }
                },
                "bien_associé": self.pro,
                "nom": self.nom,
                "emplacement": self.lieu,
                "information_complementaire": self.supplement,
            },
             "links": {
                "self": url_for("det_red", dr_id=self.id_detail_redevance, _external=True),
                "json": url_for("api_dr_single", dr_id=self.id_detail_redevance, _external=True)
            },
            "relationships": {
                 "editions": [
                     author.author_to_json()
                     for author in self.authorships
                 ]
            }
        }

class Personnes(db.Model):
    __tablename__ = 'personnes'
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    id_reconnaissance = db.Column(db.Integer, db.ForeignKey('reconnaissances.id_reconnaissance'), nullable=False)
    prenom = db.Column(db.Text)
    nom = db.Column(db.Text)
    localite = db.Column(db.Text)
    genre = db.Column(db.Text)
    precision_sur_origine = db.Column(db.Text)
    informations_personnelles = db.Column(db.Text)
    represente_par = db.Column(db.Text)
    reconnaissances = db.relationship("Reconnaissances", back_populates="personnes")
    authorships = db.relationship("Authorship", back_populates="personnes")

    def to_jsonapi_name(self):
        return {
            "type": "personne",
            "id": self.id,
            "attributes": {
                "prenom": self.prenom,
                "nom": self.nom,
                "sexe": self.genre,
                "loacalite": self.localite,
                "informations_personnelles": self.informations_personnelles,
                "reconnaissance": {
                    "id": self.id_reconnaissance,
                    "links": {
                        "page": url_for("rec", rec_id=self.id_reconnaissance, _external=True),
                        "json": url_for("api_rec_single", rec_id=self.id_reconnaissance, _external=True)
                    }
                }
            },
             "links": {
                "self": url_for("nom", name_id=self.id, _external=True),
                "json": url_for("api_name_single", name_id=self.id, _external=True)
            },
            "relationships": {
                 "editions": [
                     author.author_to_json()
                     for author in self.authorships
                 ]
            }
        }

class Reconnaissances(db.Model):
    __tablename__ = 'reconnaissances'
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    id_reconnaissance = db.Column(db.Integer, unique=True, nullable=False)
    annee = db.Column(db.Integer)
    mois = db.Column(db.Text)
    jour = db.Column(db.Integer)
    commandeur = db.Column(db.Text, nullable=False)
    statut = db.Column(db.Text)
    implication_statut = db.Column(db.Text)
    venire_ad_comi_et_critu_castri_Devessti_cum_armis = db.Column(db.Text)
    manobrias = db.Column(db.Text)
    jornalia = db.Column(db.Text)
    chareis = db.Column(db.Text)
    espleyt = db.Column(db.Text)
    complement_sur_Corvees = db.Column(db.Text)
    statut_terre = db.Column(db.Text)
    domus = db.Column(db.Text)
    orti = db.Column(db.Text)
    prata = db.Column(db.Text)
    compos = db.Column(db.Text)
    nemora = db.Column(db.Text)
    pascua = db.Column(db.Text)
    pasturalia = db.Column(db.Text)
    terrae = db.Column(db.Text)
    casalia = db.Column(db.Text)
    casamenta = db.Column(db.Text)
    grangiae = db.Column(db.Text)
    denesia = db.Column(db.Text)
    calma = db.Column(db.Text)
    assensa = db.Column(db.Text)
    molendinus = db.Column(db.Text)
    ouchias = db.Column(db.Text)
    garaitum = db.Column(db.Text)
    patile = db.Column(db.Text)
    hospicii = db.Column(db.Text)
    petiae = db.Column(db.Text)
    esclausae = db.Column(db.Text)
    terminus = db.Column(db.Text)
    costam = db.Column(db.Text)
    sana = db.Column(db.Text)
    tenementum = db.Column(db.Text)
    versana = db.Column(db.Text)
    masacgio = db.Column(db.Text)
    vineae = db.Column(db.Text)
    blachia = db.Column(db.Text)
    arbores = db.Column(db.Text)
    passetae = db.Column(db.Text)
    chastanerii = db.Column(db.Text)
    dens_Meses = db.Column(db.Text)
    levata = db.Column(db.Text)
    creysementum = db.Column(db.Text)
    bessaa = db.Column(db.Text)
    besseta = db.Column(db.Text)
    lameytenchada = db.Column(db.Text)
    bealis = db.Column(db.Text)
    mansum = db.Column(db.Text)
    sanhassium = db.Column(db.Text)
    autres_possessions = db.Column(db.Text)
    collonneFourzitout = db.Column(db.Text)
    lieux_terres = db.Column(db.Text)
    represente = db.Column(db.Text)
    mesure_de_cereale_utilisee = db.Column(db.Text)
    cens_en_poule = db.Column(db.Integer)
    totalFroment = db.Column(db.Integer)
    totalSeigle = db.Column(db.Integer)
    totalAvoine = db.Column(db.Integer)
    total_sous_tournois = db.Column(db.Integer)
    pour = db.Column(db.Text)
    jour_paiement = db.Column(db.Text)
    type_de_Juridiction = db.Column(db.Text)
    mandement = db.Column(db.Text)
    fait_a = db.Column(db.Text)
    notaire = db.Column(db.Text)
    temoin1 = db.Column(db.Text)
    temoin2 = db.Column(db.Text)
    temoin3 = db.Column(db.Text)
    temoin4 = db.Column(db.Text)
    temoin5 = db.Column(db.Text)
    accord = db.Column(db.Text)
    personnes = db.relationship("Personnes", back_populates="reconnaissances")
    page = db.relationship("Repertoire", back_populates="reconnaissances")
    detail_redevances = db.relationship("DetailRedevances", back_populates="reconnaissances")
    detail_possessions = db.relationship("DetailPossessions", back_populates="reconnaissances")
    authorships = db.relationship("Authorship", back_populates="reconnaissances")

    def to_jsonapi_rec(self):
        return {
            "type": "reconnaissance",
            "id": self.id,
            "attributes": {
                "id_reconnaissance": self.id_reconnaissance,
                "localisation_dans_le_terrier": self.page[0].repertoire_to_json(),
                "commandeur": self.commandeur,
                "notaire": self.notaire,
                "temoins": [
                    self.temoin1,
                    self.temoin2,
                    self.temoin3,
                    self.temoin4,
                    self.temoin5
                ],
                "date": {
                    "jour": self.jour,
                    "mois": self.mois,
                    "annee": self.annee
                },
                "statut": [
                    self.statut,
                    self.implication_statut
                ],
                "corvees": {
                    "manobrias": self.manobrias,
                    "jornalia": self.jornalia,
                    "chareis": self.chareis
                },
                "statut_terres": self.statut_terre,
                "biens_declares": {
                    "domus": self.domus,
                    "orti": self.orti,
                    "prata": self.prata,
                    "compos": self.compos,
                    "nemora": self.nemora,
                    "pascua": self.pascua,
                    "pasturalia": self.pasturalia,
                    "terrae": self.terrae,
                    "casalia": self.casalia,
                    "casamenta": self.casamenta,
                    "grangiae": self.grangiae,
                    "denesia": self.denesia,
                    "calma": self.calma,
                    "assensa": self.assensa,
                    "molendinus": self.molendinus,
                    "ouchias": self.ouchias,
                    "garaitum": self.garaitum,
                    "patile": self.patile,
                    "hospicii": self.hospicii,
                    "petiae": self.petiae,
                    "esclausae": self.esclausae,
                    "terminus": self.terminus,
                    "costam": self.costam,
                    "sena": self.sana,
                    "tenementum": self.tenementum,
                    "versana": self.versana,
                    "masacgio": self.masacgio,
                    "vineae": self.vineae,
                    "blachia": self.blachia,
                    "arbores": self.arbores,
                    "passetae": self.passetae,
                    "chastanerii": self.chastanerii,
                    "levata": self.levata,
                    "creysementum": self.creysementum,
                    "bessaa": self.bessaa,
                    "besseta": self.besseta,
                    "lameytenchada": self.lameytenchada,
                    "bealis": self.bealis,
                    "mansum": self.mansum,
                    "sanhassium": self.sanhassium,
                    "autres": self.autres_possessions
                },
                "emplacement": self.lieux_terres,
                "redevances_a_payer": {
                    "poules": self.cens_en_poule,
                    "seigle": {
                        "mesure": "Setiers",
                        "valeur": self.totalSeigle
                    },
                    "avoine": {
                        "mesure": "Setiers",
                        "valeur": self.totalAvoine
                    },
                    "monnaie": {
                        "mesure": "Sous tournois",
                        "valeur": self.total_sous_tournois
                    }
                },
                "mesure_cereale": self.mesure_de_cereale_utilisee,
                "jour_paiement": self.jour_paiement,
                "juridiction": [
                    self.type_de_Juridiction,
                    self.mandement
                ]
            },
             "links": {
                "self": url_for("rec", rec_id=self.id_reconnaissance, _external=True),
                "json": url_for("api_rec_single", rec_id=self.id_reconnaissance, _external=True)
            },
            "relationships": {
                 "editions": [
                     author.author_to_json()
                     for author in self.authorships
                 ]
            }
        }

    def rec_hommes_to_json(self):
        return {
            "prenom": self.prenom,
            "nom": self.nom,
            "id": self.id,
            "link": {
                "page": "r",
                "json": "r"
            }
        }

class Repertoire(db.Model):
    __tablename__ = 'repertoire'
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    id_reconnaissance = db.Column(db.Integer, db.ForeignKey("reconnaissances.id_reconnaissance"), nullable=False)
    ref_du_terrier = db.Column(db.Integer, nullable=False)
    reconnaissances = db.relationship("Reconnaissances", back_populates="page")

    def repertoire_to_json(self):
        if self.ref_du_terrier == "Inconnue":
            return {"page": "Inconnue",
                    "position_dans_la_page": "Inconnue"}
        else:
            return {
                "page": int(str(self.ref_du_terrier).split()[0][:-1]),
                "position_dans_la_page": int(str(self.ref_du_terrier).split()[0][-1])
                #Méthode similaire à celle de la page générique pour extraire les éléments du code utilisé
            }

class Charte(db.Model):
    __tablename__ = "charte"
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    prenom = db.Column(db.Text)
    nom = db.Column(db.Text)
    authorships = db.relationship("Authorship", back_populates="charte")

    def to_jsonapi_name(self):
        return {
            "type": "personne",
            "id": self.id,
            "attributes": {
                "prenom": self.prenom,
                "nom": self.nom,
                "source": {
                    "nom": "charte_de_devesset",
                    "links": {
                        "page": url_for("charte", _external=True),
                        "manifest": url_for("api_charte", _external=True)
                    }
                },
            },
             "links": {
                "self": url_for("charte_nom", name_id=self.id, _external=True),
                "json": url_for("api_charte_nom_single", name_id=self.id, _external=True)
            },
            "relationships": {
                 "editions": [
                     author.author_to_json()
                     for author in self.authorships
                 ]
            }
        }