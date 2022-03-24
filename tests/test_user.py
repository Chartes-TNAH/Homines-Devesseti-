import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from base import Base
from Homines_Devesseti.modeles.utilisateurs import User


class TestUser(Base):
    def test_creation(self):
        with self.app.app_context():
            statut, utilisateur = User.creer("joh", "johanna.johanna@enc-sorbonne.fr", "Johanna", "azerty")
            query = User.query.filter(User.user_email == "johanna.johanna@enc-sorbonne.fr").first()
        self.assertEqual(query.user_nom, "Johanna")
        self.assertEqual(query.user_login, "joh")
        self.assertNotEqual(query.user_password, "azerty")
        self.assertTrue(statut)

    def test_login_et_creation(self):
        with self.app.app_context():
            statut, cree = User.creer("joh", "johanna.johanna@enc-sorbonne.fr", "Johanna", "azerty")
            connecte = User.identification("joh", "azerty")
        self.assertEqual(cree, connecte)
        self.assertTrue(statut)
