PERSONNES_PAR_PAGE = 18
SECRET_KEY = "JE SUIS UN SECRET !"
API_ROUTE = "/api"
NAMESPACES = {
    "tei": "http://www.tei-c.org/ns/1.0"
}

#Configuration des bases :
class _TEST:
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class _PRODUCTION:
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = 'sqlite:///homines_devesseti.db?check_same_thread=False'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

CONFIG = {
    "test": _TEST,
    "production": _PRODUCTION
}