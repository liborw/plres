#!/usr/bin/python

# Simple python script performing reselution method.

import getopt
import cnf
import sys
from collections import deque


__version__ = '0.1'
__author__  = "Libor Wagner (liborwagner[at]centrum.cz)"
__date__    = "2011-02-25"


# Constants

# Globals
verbose = False
silent  = False
fsubsum = False
bsubsum = False

# Resolution ==================================================================

def resolvent(c1, c2, elit):
    pos = (c1.positive | c2.positive) & ~elit
    neg = (c1.negative | c2.negative) & ~elit
    return cnf.Clause(pos, neg)

def issubsumpsion(c1, c2):
    return c1.positive & c2.positive == c1.positive and \
            c1.negative & c2.negative == c1.negative

def complement(c1, c2):
    """Find complements in the two clauses."""
    return (c1.positive & c2.negative) | (c1.negative & c2.positive)

def count_ones(elit):
    binary = bin(elit)
    return binary.count('1')


class Node(object):

    def __init__(self, index, clause, source=None, masked=None):
        self.index = index
        self.clause = clause
        self.source = source
        self.masked = masked

    def ismasked(self):
        return not self.masked is None

    def isaxiom(self):
        return self.source is None

    def mask(self, index):
        if not self.masked:
            self.masked = list()
        self.masked.append(index)

    def __str__(self):
        s = "[{0: 3}] : {1}".format(self.index + 1, str(self.clause))

        if self.isaxiom():
            s = s+"; axiom"
        else:
            s = s+"; resolvent {0},{1}".format(self.source[0]+1, self.source[1]+1)

        if self.ismasked():
            s = s+"; masked by "+",".join(str(n+1) for n in self.masked)
        return s

    def __repr__(self):
        return "Node({0}, {1}, {2}, {3})" \
                .format(self.index, str(self.clause), self.source, self.masked)

class Resolution(object):

    def __init__(self, axioms=set(), conjectures=set()):
        self.axioms = axioms
        self.conjectures = conjectures
        self.state = list()

        self.counter = 0
        self.clauses = dict()

    def infer_bfs(self):
        clauses = self.axioms.union(self.conjectures)
        state = self._make_state(clauses)
        i = 0

        while i < len(state):

            for j in range(i, len(state)):
                comp = complement(state[i].clause, state[j].clause)
                if count_ones(comp) == 1:
                    c = resolvent(state[i].clause, state[j].clause, comp)
                    if not c.tantologi() and not c in clauses and \
                            not self._forward_subsumption(clauses, c):
                        clauses.add(c)
                        self._backward_subsumption(state, c, len(state))
                        state.append(self._make_node(len(state), c, [i, j]))
                    if c.empty():
                        self.state = state
                        return
            i = i + 1
            while  i < len(state) and state[i].ismasked():
                i = i + 1
        self.state = state
        return

    def _forward_subsumption(self, clauses, clause):
        for c in clauses:
            if issubsumpsion(c, clause):
                return True
        return False

    def _backward_subsumption(self, state, clause, index):
        if not clause.empty():
            for node in state:
                if issubsumpsion(clause, node.clause):
                    node.mask(index)

    def _make_state(self, clauses):
        i = 0
        state = list()
        for c in clauses:
            if not c.empty() and not c.tantologi():
                state.append(self._make_node(i, c))
                i = i + 1
        return state

    def _make_node(self, index, clause, source=None):
        return Node(index, clause, source)

    def print_result(self):
        if not self.state[-1].clause.empty():
            self._print_steps(self.state)
        else:
            self._print_steps(self.state)

    def _print_steps(self, steps):
        for n in steps:
            print n

# Main ========================================================================

help_message = """ [options] infile

Options:
    -h --help                   Show this message
    -v --verbose                More output
    -s --silent                 Less output
    -f --forward-subsumption    Enable forward subsumption
    -b --backward-subsumption   Enable backward subsumption
"""

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    global verbose, silent, fsubsum, bsubsum
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hvsfb", ["help",
                                                           "verbose",
                                                           "silent",
                                                           "forward-subsumption",
                                                           "backward-subsumption"])
        except getopt.error, msg:
            raise Usage(msg)

        # option processing
        for option, value in opts:
            if option in ("-v", "--verbose"):
                verbose = True
            if option in ("-s", "--silent"):
                silent = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-f", "--forward-subsumption"):
                fsubsum = True
            if option in ("-b", "--backward-subsumption"):
                bsubsum = True

        if not len(args) == 1:
            raise Usage("No input file specified!")
        elif args[0] == "--":
            infile = sys.stdin
        else:
            infile = open(args[0])

    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


    clauses = cnf.parse(infile)
    resolution = Resolution(clauses)
    resolution.infer_bfs()
    resolution.print_result()


if __name__ == '__main__':
    sys.exit(main())
