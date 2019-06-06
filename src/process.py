import uuid
import re
from rdflib import Graph, Literal
from rdflib.namespace import SKOS, RDF, Namespace

g = Graph()
concept = None


uuids = {}

VOC = Namespace('http://data.ub.uio.no/ams-ccs-ubo/')

g.namespace_manager.bind('ccs', VOC)

def get_uuid(notation):
    if notation in uuids:
        return uuids[notation]
    uuids[notation] = str(uuid.uuid4())
    return uuids[notation]


def get_uri(notation):
    return VOC[get_uuid(notation)]


def add_concept(concept):
    c = get_uri(concept['notation'])
    b = get_uri('broader')
    g.add((c, RDF.type, SKOS.Concept))
    g.add((c, SKOS.notation, Literal(concept['notation'])))
    g.add((c, SKOS.prefLabel, Literal(concept['pref'], 'en')))
    for alt in concept['alt']:
        g.add((c, SKOS.altLabel, Literal(alt, 'en')))
    g.add((c, SKOS.broader, b))


with open('input.txt') as fp:
    for line in fp:
        m = re.match(r'^([A-Z]\.([0-9m]\.?)*) (.+)$', line)
        if m:
            if concept is not None:
                add_concept(concept)

            notation = m.group(1).rstrip('.')
            notation_parts = notation.split('.')
            concept = {
                'notation': notation,
                'pref': m.group(3).strip(),
                'alt': [],
                'broader': '.'.join(notation_parts[:-1])
            }
        else:
            concept['alt'].append(line.strip())

if concept is not None:
    add_concept(concept)

print(len(g))

g.serialize('acm-ccs-ubo.ttl', format='turtle')
