
# Constants
NEGATION    = '~'
DISJUNCTION = '|'
COMMENT     = '#'

# Atom dictionary
atoms = {}

def encode_atom(atom):
    """a -> 0b1, b -> 0b10, ..."""
    global atoms
    if atom in atoms:
        i = atoms[atom]
    else:
        i = len(atoms)
        atoms[atom] = i
        atoms = atoms
    return 2**i

def encode_clause(literals):
    """('a', '~b') -> Clause(0b01, 0b10)"""
    pos = 0
    neg = 0
    for lit in literals:
        if lit[0] == NEGATION:
            neg = neg | encode_atom(lit[1:])
        else:
            pos = pos | encode_atom(lit)
    return Clause(pos, neg)

def decode_clause(clause):
    """Clause(0b01, 0b10) -> ('a', '~b')"""
    literals = list()
    for key in sorted(atoms):
        code = encode_atom(key)
        if clause.positive & code:
            literals.append(key)
        if clause.negative & code:
            literals.append(NEGATION+key)
    return literals

class Clause(object):
    """
    Clause representation, by two binary numbers positive and negative.
    Each bit represents logic variable with specific polarity.
    """
    def __init__(self, positive=0, negative=0):
        self.positive = positive
        self.negative = negative

    def __str__(self):
        return '(' + DISJUNCTION.join(str(n) for n in self._literals()) + ')'

    def __repr__(self):
        return "Clause("+str(bin(self.positive))+","+str(bin(self.negative))+")"

    def _literals(self):
        return decode_clause(self)

    def tantologi(self):
        return self.positive & self.negative

    def empty(self):
        return self.positive == 0 and self.negative == 0

    def __eq__(self, other):
         return (self.positive & other.positive) == (self.positive | other.positive) and \
            (self.negative & other.negative) == (self.negative | other.negative)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.positive^self.negative

def parse_line(line):
    """Parse line of input file."""
    literals = line.split(DISJUNCTION)
    clause = encode_clause(literals)
    return encode_clause(literals)

def file_input_filter(stream, comment='#'):
    """Parse input file."""
    for line in stream:
        # Remove end of line
        if line[-1] == '\n':
            line = line[:-1]
        # Remove comments
        try:
            ind = line.index(comment)
            line = line[:ind]
        except:
            pass
        # Remove trainling whitespaces
        line = line.strip(' ')
        # Pass only if not empty
        if len(line) > 0:
            yield line

def parse(infile):
    """Parse file into set of clauses."""
    clauses = set()
    for line in file_input_filter(infile):
        try:
            clause = parse_line(line)
            clauses.add(clause)
        except Exception as info:
            print "Warning: Error when parsing \"{0}\"".format(line), info
    return clauses
    