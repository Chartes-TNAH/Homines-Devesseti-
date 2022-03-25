from whoosh.fields import *

PageWhoosh = Schema(
    content=TEXT(stored=True),
    prenom=TEXT(stored=True),
)