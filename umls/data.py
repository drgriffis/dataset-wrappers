class Entity:
    CUI = None
    strings = None

    def __init__(self, cui, strings=None):
        self.CUI = cui
        self.strings = strings

    def primaryString(self, filter_to=None):
        '''Get the primary string used to represent this entity;
        Prefers first in string list, following example of UMLS
        Metathesaurus browser.

        If filter_to is input, returns the first string in the
        set of strings that is present in the filter set.
        '''
        if type(self.strings) == list and len(self.strings) > 0:
            if filter_to:
                for s in self.strings:
                    if s in filter_to: return s
            else:
                return self.strings[0]
        return None

class Relation:
    REL = None
    RELA = None

    def __init__(self, rel, rela):
        self.REL = rel
        self.RELA = rela

class Triple:
    
    entity = None
    relation = None
    value = None

    def __init__(self, entity, relation, value):
        self.entity = entity
        self.relation = relation
        self.value = value
