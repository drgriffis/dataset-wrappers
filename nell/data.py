'''
Data structures for reading NELL-format data dumps
'''

class Entity:
    
    def __init__(self, ID, strings, canonical_string, categories):
        self.ID = ID
        self.strings = strings
        self.canonical_string = canonical_string
        self.categories = categories

    def __eq__(self, other):
        if not type(other) is type(self): return False
        if self.ID != other.ID: return False
        if self.canonical_string != other.canonical_string: return False
        for s in self.strings:
            if not s in other.strings: return False
        for s in other.strings:
            if not s in self.strings: return False
        for c in self.categories:
            if not c in other.categories: return False
        for c in other.categories:
            if not c in self.categories: return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '\n'.join([
            '{',
            '\tID: %s' % self.ID,
            '\tCanonical string: %s' % self.canonical_string,
            '\tString set: [%s]' % ','.join(self.strings),
            '\tCategories: [%s]' % ','.join(self.categories),
            '}'
        ])


class Triple:

    class Meta:
        promote_iter = 0
        confidence = 0.0
        provenance_component = None
        provenance_general = None

        def __init__(self, promote_iter, confidence, provenance_component, provenance_general):
            self.promote_iter = promote_iter
            self.confidence = confidence
            self.provenance_component = provenance_component
            self.provenance_general = provenance_general

    entity = None
    relation = None
    value = None
    meta = None
    
    def __init__(self, entity, relation, value, meta):
        self.entity = entity
        self.relation = relation
        self.value = value
        self.meta = meta
