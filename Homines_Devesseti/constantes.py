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

<<<<<<< HEAD
if SECRET_KEY == "JE SUIS UN SECRET !":
    warn("Le secret par défaut n'a pas été changé, vous devriez le faire", Warning)

class _TEST:
    SECRET_KEY = SECRET_KEY
    # On configure la base de données
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class _PRODUCTION:
    SECRET_KEY = SECRET_KEY
    # On configure la base de données
    SQLALCHEMY_DATABASE_URI = 'sqlite:///homines_devesseti.db?check_same_thread=False'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

CONFIG = {
    "test": _TEST,
    "production": _PRODUCTION
}
=======
CONFIG = {
    "test": _TEST,
    "production": _PRODUCTION
}
>>>>>>> tests
