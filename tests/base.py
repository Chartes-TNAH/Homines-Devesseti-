from Homines_Devesseti.app import db, config_app, login
from Homines_Devesseti.modeles.utilisateurs import User
from Homines_Devesseti.modeles.donnees import Personnes, Authorship
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

    def setUp(self):
        self.app = config_app("test")
        self.db = db
        self.client = self.app.test_client()
        self.db.create_all(app=self.app)

    def tearDown(self):
        self.db.drop_all(app=self.app)

    def insert_all(self, names=True):
        # On donne à notre DB le contexte d'exécution
        with self.app.app_context():
            if names:
                for fixture in self.names:
                    self.db.session.add(fixture)
            self.db.session.commit()