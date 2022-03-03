from gazetteer.app import db, config_app, login
from gazetteer.modeles.utilisateurs import User
from gazetteer.modeles.donnees import Place, Authorship
from unittest import TestCase


class Base(TestCase):
    places = [
        Place(
            place_nom='Hippana',
            place_description='Ancient settlement in the western part of Sicily, probably founded in the seventh century B.C.',
            place_longitude=37.7018481,
            place_latitude=13.4357804,
            place_type='settlement'
        ),
        Place(
            place_nom='Nicomedia',
            place_description='Nicomedia was founded in 712/11 BC as a Megarian colony named Astacus and was rebuilt by Nicomedes I of Bithynia in 264 BC. The city was an important administrative center of the Roman Empire.',
            place_longitude=40.7651905,
            place_latitude=29.919887000000003,
            place_type='settlement'
        ),
        Place(
            place_nom='Aornos',
            place_description='Aornos was a mountain fortress and the site of Alexander the Great\'s last siege during the winter of 327-6 BC. The ancient site likely corresponds to Ūṇa, a peak on the Pīr-Sar west of the Indus river.',
            place_longitude=34.75257,
            place_latitude=72.803461,
            place_type='settlement'
        ),
        Place(
            place_nom='The \"Hochtor Sanctuary\"',
            place_description='A Celto-Roman sanctuary situated at an ancient high-mountain pass in the eastern Alps near Grossglockner, excavated beginning in the 1990s. Its ancient name is unknown.',
            place_longitude=47.081765,
            place_latitude=12.842636,
            place_type='sanctuary'
        ),
        Place(
            place_nom='Lipara (settlement)',
            place_description='A Greek colony and long-time settlement on the island of the same name, located to the north of Sicily in the Tyrrhenian Sea. Modern Lipari.',
            place_longitude=38.46740105,
            place_latitude=14.953957299999999,
            place_type='settlement'
        ),
        Place(
            place_nom='Arch of Constantine',
            place_description='The Arch of Constantine at Rome, a triumphal arch dedicated in A.D. 315.',
            place_longitude=41.889892,
            place_latitude=12.4904941,
            place_type='arch'
        ),
        Place(
            place_nom='Taberna Pomaria di Felix',
            place_description='A fruit shop in Pompeii (I, 8, 1) with an entrance on to the Via dell\'Abbondanza.',
            place_longitude=40.75074883061887,
            place_latitude=14.48995445324075,
            place_type='taberna-shop'
        ),
        Place(
            place_nom='S. Paulus',
            place_description='One of Rome\'s four major papal basilicae, S. Paulus was founded by Constantine I in the early fourth century A.D. and expanded by Valentinian I in the 370s.',
            place_longitude=41.858695,
            place_latitude=12.476827,
            place_type='church'
        ),
        Place(
            place_nom='Calleva',
            place_description='Calleva Atrebatum (known as Silchester Roman Town) was an Iron Age oppidum and Roman town in  Britannia. It was the civitas capital of the Atrebates tribe.',
            place_longitude=51.35546,
            place_latitude=-1.0915195,
            place_type='settlement'
        ),
        Place(
            place_nom='Colophon/Colophon ad Mare/Notion',
            place_description='A port city founded by Aeolian settlers at the mouth of the River Avci.',
            place_longitude=37.9928,
            place_latitude=27.1975,
            place_type='settlement'
        ),
        Place(
            place_nom='Bousiris',
            place_description='Bousiris was a city of Lower Egypt near the Phatnitic mouth of the Nile river and was considered one of the possible birthplaces of Osiris.',
            place_longitude=30.913368,
            place_latitude=31.2387955,
            place_type='settlement'
        ),
        Place(
            place_nom='Corinthia',
            place_description='Corinthia was a region of ancient Greece associated with the city-state Corinth.',
            place_longitude=37.798572,
            place_latitude=22.834379,
            place_type='region'
        ),
        Place(
            place_nom='Garumna (river)',
            place_description='The Garonne river is a river of southwestern Gaul and northern Iberia.',
            place_longitude=44.810025550000006,
            place_latitude=-0.3184549,
            place_type='river'
        ),
        Place(
            place_nom='Caelius Mons',
            place_description='The Caelian Hill in Rome.',
            place_longitude=41.88755097676503,
            place_latitude=12.491300775912759,
            place_type='hill'
        ),
        Place(
            place_nom='Prinias (Patela)',
            place_description='An Iron Age settlement on the Patela plateau north of the modern village of Prinias; its ancient name is uncertain. The site is notable for its occupation from the end of the Bronze Age through to the Archaic period, as well as for the monumental architecture and Orientalizing sculpture of its Buildings (\'Temples\') A and B. ',
            place_longitude=35.168633,
            place_latitude=25.000922,
            place_type='settlement'
        ),
    ]

    def setUp(self):
        self.app = config_app("test")
        self.db = db
        self.client = self.app.test_client()
        self.db.create_all(app=self.app)

    def tearDown(self):
        self.db.drop_all(app=self.app)

    def insert_all(self, places=True):
        # On donne à notre DB le contexte d'exécution
        with self.app.app_context():
            if places:
                for fixture in self.places:
                    self.db.session.add(fixture)
            self.db.session.commit()