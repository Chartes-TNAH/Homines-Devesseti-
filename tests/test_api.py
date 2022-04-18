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
        self.assertEqual(json_parse_dp["type"], "déclaration de bien")
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
        self.assertEqual(json_parse_dr["type"], "redevance")
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
        self.assertEqual(json_parse_name["type"], "personne")
        self.assertEqual(
            json_parse_name["attributes"]["reconnaissance"]["id"], 1773)
        self.assertEqual(json_parse_name["links"]["self"], 'http://localhost/name/2')
        seconde_requete_name = self.client.get(json_parse_name["links"]["self"])
        self.assertEqual(seconde_requete_name.status_code, 200)
        #Tests pour la classe Charte
        response_charte = self.client.get("/api/charte_homme/2")
        content_charte = response_charte.data.decode()
        self.assertEqual(
            response_charte.headers["Content-Type"], "application/json"
        )
        json_parse_charte = loads(content_charte)
        self.assertEqual(json_parse_charte["type"], "personne")
        self.assertEqual(
            json_parse_charte["attributes"]["source"]["nom"], "charte_de_devesset")
        self.assertEqual(json_parse_charte["links"]["self"], 'http://localhost/charte_homme/2')
        seconde_requete_charte = self.client.get(json_parse_charte["links"]["self"])
        self.assertEqual(seconde_requete_charte.status_code, 200)
        #Tests pour la classe Reconnaissances
        response_rec = self.client.get("/api/rec/162")
        content_rec = response_rec.data.decode()
        self.assertEqual(
            response_rec.headers["Content-Type"], "application/json"
        )
        json_parse_rec = loads(content_rec)["reconnaissance"]
        self.assertEqual(json_parse_rec["type"], "reconnaissance")
        self.assertEqual(
            json_parse_rec["attributes"]["id_reconnaissance"], 162)
        self.assertEqual(json_parse_rec["attributes"]["localisation_dans_le_terrier"]["page"], 82)
        self.assertEqual(json_parse_rec["attributes"]["date"]["annee"], 1342)
        self.assertEqual(json_parse_rec["attributes"]["biens_declares"]["domus"], "Oui"),
        self.assertEqual(json_parse_rec["attributes"]["redevances_a_payer"]["avoine"]["valeur"], 19.5)
        self.assertEqual(json_parse_rec["links"]["self"], 'http://localhost/rec/162')
        seconde_requete_rec = self.client.get(json_parse_rec["links"]["self"])
        self.assertEqual(seconde_requete_rec.status_code, 200)
        #Test portant sur les recherches
        response_search = self.client.get("/api/search?q=Albi")
        content_search = response_search.data.decode()
        self.assertEqual(
            response_search.headers["Content-Type"], "application/json"
        )
        json_parse_search = loads(content_search)["data"][0]
        self.assertEqual(json_parse_search["type"], "personne")
        self.assertEqual(
            json_parse_search["attributes"]["reconnaissance"]["id"], 1371)
        self.assertEqual(json_parse_search["links"]["self"], 'http://localhost/name/1')
        seconde_requete_search = self.client.get("/recherche?keyword=Albi")
        self.assertEqual(seconde_requete_search.status_code, 200)
