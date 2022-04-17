from Homines_Devesseti.app import db, config_app, login
from Homines_Devesseti.modeles.utilisateurs import User
from Homines_Devesseti.modeles.donnees \
    import Authorship, Personnes, DetailPossessions, DetailRedevances, Reconnaissances, Repertoire, Charte
from unittest import TestCase


class Base(TestCase):
    names = [
        Personnes(
            prenom='Jacobus',
            nom='Albi',
            localite='Mastortet',
            genre='H',
            id_reconnaissance=1371
        ),
        Personnes(
            prenom='Vitalis',
            nom='Alvernhasso',
            localite='Devessetum',
            genre='H',
            id_reconnaissance=1773
        ),
        Personnes(
            prenom='Margaros',
            nom='Asteyra',
            localite='Flossac',
            genre='F',
            id_reconnaissance=1861
        ),
        Personnes(
            prenom='Johannes',
            nom='Barerii Dens Chazalet',
            localite='Del Maset',
            genre='H',
            id_reconnaissance=1511
        )
    ]
    dp = [
        DetailPossessions(
            id_reconnaissance=142,
            possession='Terram',
            lieu='In comitate loci de Maysonetis',
        ),
        DetailPossessions(
            id_reconnaissance=142,
            possession='Pasturalia',
            lieu='In comitate loci de Maysonetis',
            confront1='Domui suum'
        ),
        DetailPossessions(
            id_reconnaissance=142,
            possession='Possessiones',
            supplement='Que idem Girandus aquisivit a dicto Marco de Spaetis'
        ),
        DetailPossessions(
            id_reconnaissance=151,
            possession='Possessiones',
            lieu='In comitate de Maisonetis'
        )
    ]
    dr = [
        DetailRedevances(
            id_reconnaissance=142,
            cens_en_poule=0,
            totalSeigle=2.4375,
            totalAvoine=0,
            total_monnaie=0,
            pro='Bayliagio'
        ),
        DetailRedevances(
            id_reconnaissance=142,
            cens_en_poule=0,
            totalSeigle=2.4375,
            totalAvoine=4.875,
            total_monnaie=0.333333333333333,
            pro='Terra et pasturalia',
            lieu='Maysonetis'
        ),
        DetailRedevances(
            id_reconnaissance=151,
            cens_en_poule=0,
            totalSeigle=2.4375,
            totalAvoine=0,
            total_monnaie=0,
            pro='Baylhagio'
        ),
        DetailRedevances(
            id_reconnaissance=151,
            cens_en_poule=0,
            totalSeigle=0,
            totalAvoine=0,
            total_monnaie=0.25,
            pro='Prato'
        )
    ]
    rec = [
        Reconnaissances(
            id_reconnaissance=142,
            annee=1342,
            commandeur='Raynaud de Fay',
            statut='Homo-licgius, justitabilis et expletabilis',
            implication_statut='Talhabilis ad omnimodas voluntatis',
            manobrias='Oui',
            domus='Oui',
            orti='Oui',
            mesure_de_cereale_utilisee='Tence',
            cens_en_poule=1.5,
            totalSeigle=39,
            totalAvoine=43.875,
            total_sous_tournois=14.83333333333,
            pour='Censu et talha',
            notaire='Girandus Girandi de Pulinaco',
        ),
        Reconnaissances(
            id_reconnaissance=151,
            annee=1342,
            commandeur='Raynaud de Fay',
            statut='Homo-licgius, justitabilis et expletabilis',
            implication_statut='Talhabilis ad omnimodas voluntatis',
            manobrias='Oui',
            domus='Oui',
            orti='Oui',
            mesure_de_cereale_utilisee='Tence',
            cens_en_poule=1.5,
            totalSeigle=95.0625,
            totalAvoine=78,
            total_sous_tournois=24.11805555555555,
            pour='Censu et talha',
            notaire='Girandus Girandi de Pulinaco',
        ),
        Reconnaissances(
            id_reconnaissance=161,
            annee=1342,
            commandeur='Raynaud de Fay',
            statut='Homo-licgius, justitabilis et expletabilis',
            notaire='Girandus Girandi de Pulinaco',
        ),
        Reconnaissances(
            id_reconnaissance=162,
            annee=1342,
            commandeur='Raynaud de Fay',
            statut='Homo-licgius, justitabilis et expletabilis',
            implication_statut='Talhabilis ad omnimodas voluntatis',
            manobrias='Oui',
            domus='Oui',
            orti='Oui',
            mesure_de_cereale_utilisee='Tence',
            cens_en_poule=1,
            totalSeigle=31.6875,
            totalAvoine=19.5,
            total_sous_tournois=10.1875,
            notaire='Girandus Girandi de Pulinaco',
        ),
    ]
    pages = [
        Repertoire(
            id_reconnaissance=142,
            ref_du_terrier=811
        ),
        Repertoire(
            id_reconnaissance=151,
            ref_du_terrier=812
        ),
        Repertoire(
            id_reconnaissance=161,
            ref_du_terrier=821
        ),
        Repertoire(
            id_reconnaissance=162,
            ref_du_terrier=821
        )
    ]
    charte = [
        Charte(
            prenom="Petrus",
            nom="La Rocha"
        ),
        Charte(
            prenom="Armandus",
            nom="De Ruppe"
        ),
        Charte(
            prenom="Johannes",
            nom="filius Guilliermi de Ruppe condam"
        )
    ]

    def setUp(self):
        self.app = config_app("test")
        self.db = db
        self.client = self.app.test_client()
        self.db.create_all(app=self.app)

    def tearDown(self):
        self.db.drop_all(app=self.app)

    def insert_all(self, names=True, dp=True, dr=True, rec=True, pages=True, charte=True):
        # On donne à notre DB le contexte d'exécution
        with self.app.app_context():
            if names:
                for fixture in self.names:
                    self.db.session.add(fixture)
            if dp:
                for fixture in self.dp:
                    self.db.session.add(fixture)
            if dr:
                for fixture in self.dr:
                    self.db.session.add(fixture)
            if rec:
                for fixture in self.rec:
                    self.db.session.add(fixture)
            if pages:
                for fixture in self.pages:
                    self.db.session.add(fixture)
            if charte:
                for fixture in self.charte:
                    self.db.session.add(fixture)
            self.db.session.commit()