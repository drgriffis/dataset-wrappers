'''
Library for parsing MySQL dumps from UMLS
(files dumped via SQL scripts in sql/ directory)
'''

import codecs
from umls.data import Entity, Relation, Triple
from denis.common.logging import log

def _parseRelationLine(line, cui_strings=None):
    ## parse out data
    (
        rel,
        rela,
        entity,
        value
    ) = [s.strip() for s in line.strip().split('\t')]

    ## grab entity string sets
    if cui_strings:
        e_string_set = cui_strings.get(entity, None)
        v_string_set = cui_strings.get(value, None)
    else:
        e_string_set = None
        v_string_set = None

    ## instantiate component objects
    ent = Entity(entity, e_string_set)
    val = Entity(value, v_string_set)
    rln = Relation(rel, rela)
    return Triple(ent, rln, val)

def parseRelations(fpath, cui_strings=None):
    '''Parses UMLS data and returns a list of Triple objects,
    the set of unique entities, and the set of unique relations.

    If cui_strings is passed in, will add the CUI's representative
    string mappings to the Triple.Entity objects.
    '''

    triples, entities, relations = [], {}, {}

    log.track(message='  >> Lines read: {0}', writeInterval=100)

    hook = codecs.open(fpath, 'r', 'utf-8')
    hook.readline() # skip headers
    for line in hook:
        triple = _parseRelationLine(line, cui_strings=cui_strings)

        entities[triple.entity.CUI] = triple.entity
        entities[triple.value.CUI] = triple.value
        relations['%s||%s' % (triple.relation.REL, triple.relation.RELA)] = triple.relation

        triples.append(triple)
        log.tick()
    log.writeln()
    hook.close()

    return triples, entities, relations

def _parseStringLine(line):
    (
        string,
        CUI
    ) = [s.strip() for s in line.strip().split('\t')]
    return (string, CUI)

def parseStrings(fpath, primary_only=True, filter_to=None):
    '''Reads a mapping of CUI->string(s)
    '''

    mapping = {}
    if filter_to:
        filter_set = set([cui.lower() for cui in filter_to])
        passes_filter = lambda cui: cui.lower() in filter_set
    else:
        passes_filter = lambda cui: True

    log.track(message='  >> Lines read: {0}', writeInterval=100)

    hook = codecs.open(fpath, 'r', 'utf-8')
    hook.readline() # skip headers
    for line in hook:
        (string, CUI) = _parseStringLine(line)
        # if filtering to specific CUIs, check for match
        if passes_filter(CUI):
            if primary_only:
                # keep only the first string encountered
                # (approach the UTS metathesaurus browser takes)
                if mapping.get(CUI, None) == None:
                    mapping[CUI] = [string]
            else:
                if mapping.get(CUI, None) == None: mapping[CUI] = []
                mapping[CUI].append(string)
        log.tick()
    log.writeln()
    hook.close()

    return mapping
