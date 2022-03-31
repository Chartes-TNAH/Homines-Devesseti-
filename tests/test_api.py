from base import Base
from json import loads

class TestApi(Base):
    def test_api(self):
        self.insert_all()
        #Tests pour la classe Détail Possessions
        response_dp = self.client.get("/api/dp/2")
        content_dp = response_dp.data.decode()
        ''' Dans cette situation, le corps de la réponse est dans .data
        .data est en "bytes". Pour convertir des bytes en str, on fait .decode()'''
        self.assertEqual(
            response_dp.headers["Content-Type"], "application/json"
        )
        json_parse_dp = loads(content_dp)
        self.assertEqual(json_parse_dp["type"], "Déclaration de bien")
        self.assertEqual(
            json_parse_dp["attributes"]["reconnaissance"]["id"], 142)
        self.assertEqual(json_parse_dp["attributes"]["confronts"][0], "Domui suum")
        self.assertEqual(json_parse_dp["links"]["self"], 'http://localhost/dp/2')
        seconde_requete_dp = self.client.get(json_parse_dp["links"]["self"])
        self.assertEqual(seconde_requete_dp.status_code, 200)
        #Tests pour la classe Détail Redevances
        response_dr = self.client.get("/api/dr/2")
        content_dr = response_dr.data.decode()
        self.assertEqual(
            response_dr.headers["Content-Type"], "application/json"
        )
        json_parse_dr = loads(content_dr)
        self.assertEqual(json_parse_dr["type"], "Redevance")
        self.assertEqual(
            json_parse_dr["attributes"]["reconnaissance"]["id"], 142)
        self.assertEqual(json_parse_dr["attributes"]["redevances_a_payer"]["avoine"]["valeur"], 4.875)
        self.assertEqual(json_parse_dr["links"]["self"], 'http://localhost/dr/2')
        seconde_requete_dr = self.client.get(json_parse_dr["links"]["self"])
        self.assertEqual(seconde_requete_dr.status_code, 200)
        #Tests pour la classe Personnes
        response_name = self.client.get("/api/name/2")
        content_name = response_name.data.decode()
        self.assertEqual(
            response_name.headers["Content-Type"], "application/json"
        )
        json_parse_name = loads(content_name)
        self.assertEqual(json_parse_name["type"], "Personne")
        self.assertEqual(
            json_parse_name["attributes"]["reconnaissance"]["id"], 1773)
        self.assertEqual(json_parse_name["links"]["self"], 'http://localhost/name/2')
        seconde_requete_name = self.client.get(json_parse_name["links"]["self"])
        self.assertEqual(seconde_requete_name.status_code, 200)
'''        #Tests pour la classe Reconnaissances (non-fonctionnel pour le moment)
        response_rec = self.client.get("/api/rec/162")
        content_rec = response_rec.data.decode()
        self.assertEqual(
            response_rec.headers["Content-Type"], "application/json"
        )
        json_parse_rec = loads(content_rec)
        self.assertEqual(json_parse_rec["type"], "Reconnaissance")
        self.assertEqual(
            json_parse_rec["attributes"]["id_reconnaissance"], 162)
        self.assertEqual(json_parse_rec["localisation_dans_le_terrier"], 82)
        self.assertEqual(json_parse_rec["date"]["anne"], 1342)
        self.assertEqual(json_parse_rec["biens_declares"]["domus"], "Oui"),
        self.assertEqual(json_parse_rec["attributes"]["redevances_a_payer"]["avoine"]["valeur"], 19.5)
        self.assertEqual(json_parse_rec["links"]["self"], 'http://localhost/rec/162')
        seconde_requete_rec = self.client.get(json_parse_rec["links"]["self"])
        self.assertEqual(seconde_requete_rec.status_code, 200)'''