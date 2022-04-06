from typing import List
from collections import namedtuple
import lxml.etree as ET

#Ceci est un essai, absolument pas fonctionnel pour le moment. Je pense que je vais me concentrer sur la recherche
#avant de voir comment y intégrer les données de ma charte...

'''
NAMESPACES = {
    "tei": "http://www.tei-c.org/ns/1.0"
}
Line = namedtuple("Line", ["text", "type", "regionId"])
'''

def get_personnes(filepath: str) -> List[Personne]:
    xml = ET.parse(filepath)
    contenu = xml.getroot()
    return contenu

    '''regions = {
        region.attrib["ID"]: region.attrib["LABEL"]
        for region in xml.xpath("/a:alto/a:Tags/a:OtherTag", namespaces=NAMESPACES)
    }
    lines = []
    for tb in xml.xpath("//a:TextBlock[.//a:TextLine]", namespaces=NAMESPACES):
        rType = regions.get(tb.attrib["TAGREFS"], "Inconnue")
        rId = tb.attrib["ID"]
        for line in tb.xpath(".//a:TextLine//a:String/@CONTENT", namespaces=NAMESPACES):
            lines.append(Line(str(line), rType, rId))
    return lines'''
