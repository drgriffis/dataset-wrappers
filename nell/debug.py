'''
Miscellaneous debug methods for working with NELL data files
'''

def printLine(chnks):
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
    ) = chnks
    print('--- Base ---')
    print('Entity ID: %s' % entity)
    print('Relation: %s' % relation)
    print('Value ID: %s' % value)
    print('--- Entity ---')
    print('Entity canonical string: %s' % entity_canonical_string)
    print('Entity literal strings: %s' % entity_literal_strings)
    print('Entity categories: %s' % entity_categories)
    print('--- Value ---')
    print('Value canonical string: %s' % value_canonical_string)
    print('Value literal strings: %s' % value_literal_strings)
    print('Value categories: %s' % value_categories)
    print('--- Meta ---')
    print('Promote Iteration: %s' % promote_iteration)
    print('Confidence: %s' % confidence)
    print('Component Provenance: %s' % component_provenance)
    print('General Provenance: %s' % general_provenance)
    raw_input()

def testLiteralParsing():
    print(parseLiteralStrings('abc'))
    print(parseLiteralStrings('"abc"'))
    print(parseLiteralStrings('"abc" "def"  "ghi"'))
    print(parseLiteralStrings('"abc \\"def\\" ghi" "jkl" mno'))
