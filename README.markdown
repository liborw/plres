# A4M33AU: Resolution for Propositional Logic
This project is part of the [A4M33AU][a4m33au] course on [Faculty of Electrical Engineering][fee].

### Usage

    plres.py input_file

### Input format
The input must be in [Conjunctive Normal Form][cnf] one clause for line with three reserved symbols `~`, `|` and `#` for negation, disjunction and comment respectively.

Example (maya.cnf):

    # A claims that B tells truth and M is Maya
    # B claims that A tells lie and M is Maya
    # Formalised:
    #   A <=> (B & M)
    #   B <=> (~A & M)

    # CNF axioms:
    ~a|b
    ~a|m
    ~b|~m|a
    ~b|~a
    ~b|m
    b|a|~m

    # Negation of conjecture (not Maya)
    m




[fee]: http://www.fel.cvut.cz
[a4m33au]: https://cw.felk.cvut.cz/doku.php/courses/a4m33au/
[cnf]: http://en.wikipedia.org/wiki/Conjunctive_normal_form