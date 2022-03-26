from whoosh.fields import *

PageWhoosh = Schema(
    id=STORED,
    nom=TEXT(stored=True),
    prenom=TEXT(stored=True),
)