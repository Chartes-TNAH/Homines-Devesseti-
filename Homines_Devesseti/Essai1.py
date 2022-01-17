from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

#Instanciation de ma base de données
app = Flask("Homines Devesseti")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\virgi\\Desktop\\Master TNAH\\Python\\Devoir_Python\\Homines_Devesseti\\homines_devesseti.db'
## Chemin du fichier correspondant à sa place dans Windows
db = SQLAlchemy(app)

#Definition de mes classes
class DetailPossessions(db.Model):
    Id_detail_possession = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    Id_reconnaissance = db.Column(db.Integer, nullable=False)
    Possession = db.Column(db.Text)
    Nom = db.Column(db.Text)
    Personne_concernee = db.Column(db.Text)
    Lieu = db.Column(db.Text)
    Confront1 = db.Column(db.Text)
    Confront2 = db.Column(db.Text)
    Confront3 = db.Column(db.Text)
    Confront4 = db.Column(db.Text)
    Confront5 = db.Column(db.Text)
    Confront6 = db.Column(db.Text)
    Supplement = db.Column(db.Text)


class DetailRedevances(db.Model):
    Id_detail_redevance = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    Id_detail_reconnaissance = db.Column(db.Integer, nullable=False)
    Cens_en_poule = db.Column(db.Integer, nullable=False)
    TotalSeigle = db.Column(db.Integer, nullable=False)
    TotalAvoine = db.Column(db.Integer, nullable=False)
    Total_monnaie = db.Column(db.Integer, nullable=False)
    Pro = db.Column(db.Text)
    Nom = db.Column(db.Text)
    Lieu = db.Column(db.Text)
    Supplement = db.Column(db.Text)


class Personnes(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    id_reconnaissance = db.Column(db.Integer, nullable=False)
    prenom = db.Column(db.Text)
    nom = db.Column(db.Text)
    localite = db.Column(db.Text)
    genre = db.Column(db.Text)
    precision_sur_origine = db.Column(db.Text)
    informations_personnelles = db.Column(db.Text)
    represente_par = db.Column(db.Text)


class Reconnaissances(db.Model):
    Id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    Annee = db.Column(db.Integer)
    Mois = db.Column(db.Text)
    Jour = db.Column(db.Integer)
    Commandeur = db.Column(db.Text, nullable=False)
    Statut = db.Column(db.Text)
    Implication_statut = db.Column(db.Text)
    Venire_ad_comi_et_critu_castri_Devessti_cum_armis = db.Column(db.Text)
    Manobrias = db.Column(db.Text)
    Jornalia = db.Column(db.Text)
    Chareis = db.Column(db.Text)
    Espleyt = db.Column(db.Text)
    Complement_sur_Corvees = db.Column(db.Text)
    Statut_terre = db.Column(db.Text)
    Domus = db.Column(db.Text)
    Orti = db.Column(db.Text)
    Prata = db.Column(db.Text)
    Compos = db.Column(db.Text)
    Nemora = db.Column(db.Text)
    Pascua = db.Column(db.Text)
    Pasturalia = db.Column(db.Text)
    Terrae = db.Column(db.Text)
    Casalia = db.Column(db.Text)
    Casamenta = db.Column(db.Text)
    Grangiae = db.Column(db.Text)
    Denesia = db.Column(db.Text)
    Calma = db.Column(db.Text)
    Assensa = db.Column(db.Text)
    Molendinus = db.Column(db.Text)
    Ouchias = db.Column(db.Text)
    Garaitum = db.Column(db.Text)
    Patile = db.Column(db.Text)
    Hospicii = db.Column(db.Text)
    Petiae = db.Column(db.Text)
    Esclausae = db.Column(db.Text)
    Terminus = db.Column(db.Text)
    Costam = db.Column(db.Text)
    Sana = db.Column(db.Text)
    Tenementum = db.Column(db.Text)
    Versana = db.Column(db.Text)
    Masacgio = db.Column(db.Text)
    Vineae = db.Column(db.Text)
    Blachia = db.Column(db.Text)
    Arbores = db.Column(db.Text)
    Passetae = db.Column(db.Text)
    Chastanerii = db.Column(db.Text)
    Dens_Meses = db.Column(db.Text)
    Levata = db.Column(db.Text)
    Creysementum = db.Column(db.Text)
    Bessaa = db.Column(db.Text)
    Besseta = db.Column(db.Text)
    Lameytenchada = db.Column(db.Text)
    Bealis = db.Column(db.Text)
    Mansum = db.Column(db.Text)
    Sanhassium = db.Column(db.Text)
    Autres_possessions = db.Column(db.Text)
    CollonneFourzitout = db.Column(db.Text)
    Lieux_terres = db.Column(db.Text)
    Represente = db.Column(db.Text)
    Mesure_de_cereale_utilisee = db.Column(db.Text)
    Cens_en_poule = db.Column(db.Integer)
    TotalFroment = db.Column(db.Integer)
    TotalSeigle = db.Column(db.Integer)
    TotalAvoine = db.Column(db.Integer)
    Total_sous_tournois = db.Column(db.Integer)
    Pour = db.Column(db.Text)
    Jour_paiement = db.Column(db.Text)
    Type_de_Juridiction = db.Column(db.Text)
    Mandement = db.Column(db.Text)
    Fait_a = db.Column(db.Text)
    Notaire = db.Column(db.Text)
    Temoin1 = db.Column(db.Text)
    Temoin2 = db.Column(db.Text)
    Temoin3 = db.Column(db.Text)
    Temoin4 = db.Column(db.Text)
    Temoin5 = db.Column(db.Text)
    Accord = db.Column(db.Text)


class Repertoire(db.Model):
    Id = db.Reconnaissance = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    Ref_du_terrier = db.Column(db.Integer, nullable=False)

#Mes requêtes
hommes = Personnes.query.all()

#Mes routes
@app.route("/")
def accueil():
    return render_template("pages/accueil.html", nom="Homines Devesseti", hommes=hommes)


@app.route("/name/<int:name_id>")
def nom(name_id):
    return render_template("pages/noms.html", nom="Homines Devesseti", homme=hommes[name_id])


# Petit tips final pour s'assurer que Python s'est pas perdu en chemin et exécute bien ce fichier
if __name__ == "__main__":
    app.run(debug=True)
