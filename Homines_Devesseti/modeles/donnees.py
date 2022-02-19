from flask import url_for
import datetime
from ..app import db

class Authorship(db.Model):
    __tablename__ = "authorship"
    authorship_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_place_id = db.Column(db.Integer, db.ForeignKey('personnes.id'))
    authorship_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    authorship_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user = db.relationship("User", back_populates="authorships")
    personnes = db.relationship("Personnes", back_populates="authorships")

    def author_to_json(self):
        return {
            "author": self.user.to_jsonapi_dict(),
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
    reconnaissances = db.relationship("Reconnaissances", back_populates="personne")
    authorships = db.relationship("Authorship", back_populates="personnes")

    def to_jsonapi_dict(self):
        """ It ressembles a little JSON API format but it is not completely compatible

        :return:
        """
        return {
            "type": "personne",
            "id": self.id,
            "attributes": {
                "nom": self.nom,
                "sexe": self.genre,
                "loacalite": self.localite,
                "informations_personnelles": self.informations_personnelles,
                "reconnaissance": self.id_reconnaissance,
            },
            "links": {
                "self": url_for("nom", name_id=self.id, _external=True),
                "json": url_for("api_places_single", name_id=self.id, _external=True)
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
    personne = db.relationship("Personnes", back_populates="reconnaissances")
    page = db.relationship("Repertoire", back_populates="reconnaissances")
    detail_redevances = db.relationship("DetailRedevances", back_populates="reconnaissances")
    detail_possessions = db.relationship("DetailPossessions", back_populates="reconnaissances")


class Repertoire(db.Model):
    __tablename__ = 'repertoire'
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    id_reconnaissance = db.Column(db.Integer, db.ForeignKey("reconnaissances.id_reconnaissance"), nullable=False)
    ref_du_terrier = db.Column(db.Integer, nullable=False)
    reconnaissances = db.relationship("Reconnaissances", back_populates="page")