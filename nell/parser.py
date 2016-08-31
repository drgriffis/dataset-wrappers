'''
Library for parsing NELL-format data files into nell.data.Triple objects
'''

import codecs
from nell.data import Entity, Triple
from denis.common.storage import FreqPair
from denis.common.logging import log

__MAX_STRING_LEN__ = 10000

def parseLine(line):
    '''Parses a NELL-format line describing a relation triple into a Triple object
    
    Line components taken from http://rtw.ml.cmu.edu/rtw/faq
    '''
    ## parse out the line
    (
        entity,
        relation,
        value,
        promote_iteration,
        confidence,
        component_provenance,
        entity_literal_strings,
        value_literal_strings,
        entity_canonical_string,
        value_canonical_string,
        entity_categories,
        value_categories,
        general_provenance
    ) = [s.strip() for s in line.strip().split('\t')]

    ## instantiate component objects
    ent = Entity(entity, 
        parseLiteralStrings(entity_literal_strings),
        entity_canonical_string,
        parseCategories(entity_categories))
    val = Entity(value, 
        parseLiteralStrings(value_literal_strings), 
        value_canonical_string,
        parseCategories(value_categories))

    return Triple(
        ent,
        relation,
        val,
        Triple.Meta(
            int(promote_iteration),
            float(confidence),
            component_provenance,
            general_provenance
        )
    )

def truncate(string):
    if len(string) > __MAX_STRING_LEN__:
        return '%s!!TRUNCATED!!' % string[:__MAX_STRING_LEN__]
    else:
        return string

def parse(fpath, include_freqs=False):
    '''Parses NELL data and returns a list of Triple objects,
    the set of unique entities (optionally with frequencies), and the
    set of unique relations (optionally with frequencies).
    
    Line components taken from http://rtw.ml.cmu.edu/rtw/faq
    '''

    entities = {}
    relations = {}
    triples = []

    log.track(message='  >> Lines read: {0}', writeInterval=100)

    hook = open(fpath, 'r')
    hook.readline() # skip headers
    for line in hook:
        triple = parseLine(line)

        # increment the entity frequencies
        old_ent_fp = entities.get(triple.entity.ID, None)
        old_val_fp = entities.get(triple.value.ID, None)
        if old_ent_fp != None: old_ent_fp.increment()
        else: entities[triple.entity.ID] = FreqPair(triple.entity, freq=1)
        if old_val_fp != None: old_val_fp.increment()
        else: entities[triple.value.ID] = FreqPair(triple.value, freq=1)

        # increment the relation frequency
        relations[triple.relation] = relations.get(triple.relation, 0) + 1

        # store the triple
        triples.append(triple)

        log.tick()
    log.writeln()

    # convert tracking dictionaries to lists
    entities = list(entities.values())
    relations = [FreqPair(k,v) for (k,v) in relations.items()]

    # if not including frequency information, reduce to core objects
    if not include_freqs:
        entities = [e.item for e in entities]
        relations = [r.item for r in relations]

    return triples, entities, relations

def parseLiteralStrings(raw):
    '''Converts a string in the format '"string 1" "string 2"' to
    a list ["string 1", "string 2"]
    '''
    strings = []

    remaining, in_string, next_quote = raw, False, 0
    try:
        while len(remaining) > 0:
            if not in_string:
                start = remaining.index('"')
                remaining = remaining[start+1:]
                in_string = True
                next_quote = 0
            else:
                next_quote += remaining[next_quote:].index('"')
                # ignore escaped quotes
                if remaining[next_quote-1] == '\\':
                    next_quote += 1
                else:
                    strings.append(remaining[:next_quote])
                    remaining = remaining[next_quote+1:]
                    in_string = False
    except ValueError:
        ## " was not found; done parsing
        pass

    return strings

def parseCategories(raw):
    '''Converts a string in the format 'cat:subcat1 cat:sub:subsubcat2'
    to a list ["cat:subcat1", "cat:sub:subsubcat2"]
    '''
    return [s.strip() for s in raw.split(' ')]

if __name__ == '__main__':
    parse('/data/data5/scratch/griffisd/nell-iter995/NELL.08m.995.esv.csv')
    #parse('/data/data5/scratch/griffisd/nell-iter995/wut.csv')
