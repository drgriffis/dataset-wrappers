'''
Tests for validating a NELL-format data dump
'''

import nell.parser as parser
from denis.common.logging import log


### Validation tests ####################

def wellFormed(fpath):
    '''Tests file for well-formed data by checking
    for successful parses on each line
    '''
    _start('Well-formedness of data')

    def _action(line, _):
        try:
            parser.parseLine(line)
            return True
        except Exception as e:
            print('-- Parsing error --')
            print('Offending line:')
            print('  %s' % line)
            print('Error: %s' % repr(e))
            return False

    valid = _readLines(fpath, _action, None)
    _stop(valid)

def entityInfoConsistent(fpath):
    '''Tests file to ensure that each occurrence of an
    entity always contains the same information
    '''
    _start('Entity info consistent across all occurrences')

    def _action(line, args):
        (entities,) = args
        triple = parser.parseLine(line)

        old_ent = entities.get(triple.entity.ID, None)
        old_val = entities.get(triple.value.ID, None)

        try:
            if old_ent != None: assert old_ent == triple.entity
        except AssertionError as e:
            print('-- Entity difference detected --')
            print('Old entity info')
            print(old_ent)
            print('New entity info')
            print(triple.entity)
            raise e

        try:
            if old_val != None: assert old_val == triple.value
        except AssertionError as e:
            print('-- Entity difference detected --')
            print('Old entity info')
            print(old_val)
            print('New entity info')
            print(triple.value)
            raise e

        return True

    entities = {}
    valid = _readLines(fpath, _action, (entities,))
    _stop(valid)


### Utility methods #####################

def _start(msg):
    print('VALIDATION: %s' % msg)

def _stop(valid):
    res = 'Valid' if valid else 'Invalid'
    print('RESULT: %s' % res)

def _readLines(fpath, action, action_args):
    valid = True
    log.track(message='  >> Lines validated: {0}', writeInterval=100)
    hook = open(fpath, 'r')
    try:
        hook.readline() # skip headers
        for line in hook:
            if not action(line, action_args):
                valid = False
            log.tick()
    # quietly handle exceptions (individual methods show errors)
    except Exception:
        valid = False
    finally:
        log.writeln()
        hook.close()
    return valid


### CLI #################################

def _cli():
    import optparse
    parser = optparse.OptionParser(usage='Usage: %prog NELL_FILE')
    parser.add_option('-w', '--well-formed', dest='wellformed',
            help='test for well-formedness',
            action='store_true', default=False)
    parser.add_option('-e', '--entity', dest='entity',
            help='test for entity consistency',
            action='store_true', default=False)
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.print_help()
        exit()
    return args[0], options.wellformed, options.entity

if __name__ == '__main__':
    fpath, wellformed, entity = _cli()
    if wellformed:
        wellFormed(fpath)
    if entity:
        entityInfoConsistent(fpath)
