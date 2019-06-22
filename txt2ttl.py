import sys
import uuid
import re
import yaml
from rdflib import Graph, Literal
from rdflib.namespace import SKOS, RDF, Namespace

namespace = Namespace('http://data.ub.uio.no/acm-ccs-ubo/')
IDS_FILE = sys.argv[1]
TXT_FILE = sys.argv[2]
TTL_FILE = sys.argv[3]

with open(IDS_FILE, 'r', encoding='utf-8') as fp:
    uuids = yaml.safe_load(fp) or {}

scheme = namespace['']
concept = None

g = Graph()
g.namespace_manager.bind('ccs', namespace)
g.namespace_manager.bind('skos', SKOS)


def get_id(notation):
    if notation in uuids:
        return uuids[notation]
    # Fixed prefix to avoid ids starting with a number
    uuids[notation] = 'c' + str(uuid.uuid4())
    return uuids[notation]


def get_uri(notation):
    return namespace[get_id(notation)]


def add_concept(concept):
    c = get_uri(concept['notation'])
    g.add((c, RDF.type, SKOS.Concept))
    g.add((c, SKOS.inScheme, scheme))
    g.add((c, SKOS.notation, Literal(concept['notation'])))
    g.add((c, SKOS.prefLabel, Literal(concept['pref'], 'en')))
    for alt in concept['alt']:
        g.add((c, SKOS.altLabel, Literal(alt, 'en')))
    if 'broader' in concept:
        b = get_uri(concept['broader'])
        g.add((c, SKOS.broader, b))
    else:
        g.add((c, SKOS.topConceptOf, scheme))


with open(TXT_FILE, 'r', encoding='utf-8') as fp:
    for line in fp:
        m = re.match(r'^([A-ZØ]\.([0-9m]\.?)*) (.+)$', line)
        if m:
            if concept is not None:
                add_concept(concept)

            notation = m.group(1).strip().rstrip('.')
            notation_parts = notation.split('.')
            broader = '.'.join(notation_parts[:-1])

            concept = {
                'notation': notation,
                'pref': m.group(3).strip(),
                'alt': [],
            }
            if len(broader) != 0:
                concept['broader'] = broader

        else:
            concept['alt'].append(line.strip())

if concept is not None:
    add_concept(concept)

print('Converted %d concepts' % len(g))

with open(IDS_FILE, 'w', encoding='utf-8') as fp:
    yaml.dump(uuids, fp)

g.serialize(TTL_FILE, format='turtle')
