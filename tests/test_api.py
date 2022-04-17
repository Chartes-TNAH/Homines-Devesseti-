import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from base import Base
from json import loads


class TestApi(Base):
    def test_single_place(self):
        """ Vérifie qu'un lieu est bien traité """
        self.insert_all()
        response = self.client.get("/api/name/1")
        # Le corps de la réponse est dans .data
        # .data est en "bytes". Pour convertir des bytes en str, on fait .decode()
        content = response.data.decode()
        self.assertEqual(
            response.headers["Content-Type"], "application/json"
        )
        json_parse = loads(content)
        self.assertEqual(json_parse["type"], "Personne")
        self.assertEqual(
            json_parse["attributes"]["informations_personnelles"], None)
        self.assertEqual(json_parse["links"]["self"], 'http://localhost/name/1')

        # On vérifie que le lien est correct
        seconde_requete = self.client.get(json_parse["links"]["self"])
        self.assertEqual(seconde_requete.status_code, 200)
