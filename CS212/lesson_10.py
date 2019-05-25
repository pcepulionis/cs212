#########################################  JSON PARSER #########################################


# ---------------
# User Instructions
#
# In this problem, you will be using many of the tools and techniques
# that you developed in unit 3 to write a grammar that will allow
# us to write a parser for the JSON language.
#
# You will have to visit json.org to see the JSON grammar. It is not
# presented in the correct format for our grammar function, so you
# will need to translate it.

# ---------------
# Provided functions
#
# These are all functions that were built in unit 3. They will help
# you as you write the grammar.  Add your code at line 102.

from functools import update_wrapper
# from string import split
import re


def grammar(description, whitespace=r'\s*'):
    """Convert a description to a grammar.  Each line is a rule for a
    non-terminal symbol; it looks like this:
        Symbol =>  A1 A2 ... | B1 B2 ... | C1 C2 ...
    where the right-hand side is one or more alternatives, separated by
    the '|' sign.  Each alternative is a sequence of atoms, separated by
    spaces.  An atom is either a symbol on some left-hand side, or it is
    a regular expression that will be passed to re.match to match a token.

    Notation for *, +, or ? not allowed in a rule alternative (but ok
    within a token). Use '\' to continue long lines.  You must include spaces
    or tabs around '=>' and '|'. That's within the grammar description itself.
    The grammar that gets defined allows whitespace between tokens by default;
    specify '' as the second argument to grammar() to disallow this (or supply
    any regular expression to describe allowable whitespace between tokens)."""
    G = {' ': whitespace}
    description = description.replace('\t', ' ')  # no tabs!
    for line in str.split(description, '\n'):
        lhs, rhs = str.split(line, ' => ', 1)
        alternatives = str.split(rhs, ' | ')
        G[lhs] = tuple(map(str.split, alternatives))
    return G


def decorator(d):
    "Make function d a decorator: d wraps a function fn."

    def _d(fn):
        return update_wrapper(d(fn), fn)

    update_wrapper(_d, d)
    return _d


@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}

    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(args)

    return _f


def parse(start_symbol, text, grammar):
    """Example call: parse('Exp', '3*x + b', G).
    Returns a (tree, remainder) pair. If remainder is '', it parsed the whole
    string. Failure iff remainder is None. This is a deterministic PEG parser,
    so rule order (left-to-right) matters. Do 'E => T op E | T', putting the
    longest parse first; don't do 'E => T | T op E'
    Also, no left recursion allowed: don't do 'E => E op T'"""

    tokenizer = grammar[' '] + '(%s)'

    def parse_sequence(sequence, text):
        result = []
        for atom in sequence:
            tree, text = parse_atom(atom, text)
            if text is None: return Fail
            result.append(tree)
        return result, text

    @memo
    def parse_atom(atom, text):
        if atom in grammar:  # Non-Terminal: tuple of alternatives
            for alternative in grammar[atom]:
                tree, rem = parse_sequence(alternative, text)
                if rem is not None: return [atom] + tree, rem
            return Fail
        else:  # Terminal: match characters against start of text
            m = re.match(tokenizer % atom, text)
            return Fail if (not m) else (m.group(1), text[m.end():])

    # Body of parse:
    return parse_atom(start_symbol, text)


Fail = (None, None)


JSON = grammar("""
object => { } | { members }
members => pair , members | pair
pair => string : value
array => [[] []] | [[] elements []]
elements => value , elements | value
value => string | number | object | array | true | false | null
string => "[^"]*"
number => int frac exp | int frac | int exp | int
int => -?[1-9][0-9]*
frac => [.][0-9]+
exp => [eE][-+]?[0-9]+
""", whitespace='\s*')

def json_parse(text):
    return parse('value', text, JSON)


def test():
    assert json_parse('["testing", 1, 2, 3]') == (
        ['value', ['array', '[', ['elements', ['value',
                                               ['string', '"testing"']], ',', ['elements', ['value', ['number',
                                                                                                      ['int', '1']]],
                                                                               ',', ['elements', ['value', ['number',
                                                                                                            ['int',
                                                                                                             '2']]],
                                                                                     ',',
                                                                                     ['elements', ['value', ['number',
                                                                                                             ['int',
                                                                                                              '3']]]]]]],
                   ']']], '')

    assert json_parse('-123.456e+789') == (
        ['value', ['number', ['int', '-123'], ['frac', '.456'], ['exp', 'e+789']]], '')

    assert json_parse('{"age": 21, "state":"CO","occupation":"rides the rodeo"}') == (
        ['value', ['object', '{', ['members', ['pair', ['string', '"age"'],
                                               ':', ['value', ['number', ['int', '21']]]], ',', ['members',
                                                                                                 ['pair',
                                                                                                  ['string', '"state"'],
                                                                                                  ':', ['value',
                                                                                                        ['string',
                                                                                                         '"CO"']]],
                                                                                                 ',', ['members',
                                                                                                       ['pair',
                                                                                                        ['string',
                                                                                                         '"occupation"'],
                                                                                                        ':',
                                                                                                        ['value',
                                                                                                         ['string',
                                                                                                          '"rides the rodeo"']]]]]],
                   '}']], '')
    return 'tests pass'


print(test())



#########################################  INVERSE FUNCTIONS  #########################################


# --------------
# User Instructions
#
# Write a function, inverse, which takes as input a monotonically
# increasing (always increasing) function that is defined on the
# non-negative numbers. The runtime of your program should be
# proportional to the LOGARITHM of the input. You may want to
# do some research into binary search and Newton's method to
# help you out.
#
# This function should return another function which computes the
# inverse of the input function.
#
# Your inverse function should also take an optional parameter,
# delta, as input so that the computed value of the inverse will
# be within delta of the true value.

# -------------
# Grading Notes
#
# Your function will be called with three test cases. The
# input numbers will be large enough that your submission
# will only terminate in the allotted time if it is
# efficient enough.

def slow_inverse(f, delta=1 / 128.):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""

    def f_1(y):
        x = 0
        while f(x) < y:
            x += delta
        # Now x is too big, x-delta is too small; pick the closest to y
        return x if (f(x) - y < y - f(x - delta)) else x - delta

    return f_1


def inverse(f, delta=1/128.):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""
    def _f(y):
        low, high = get_bounds(f, y)
        return bin_search(low, high, f, y, delta)
    return _f


def get_bounds(f, x):
    low, high = 0, 1

    def in_between(x, l, h): return x >= f(l) and x <= f(h)

    while not in_between(x, low, high):
        low, high = high, 2 * high
    return (low, high)


def bin_search(low, high, f, y, delta):
    mid = (low + high) / 2.0
    lower_bound, upper_bound = y-delta, y+delta

    def good_enough(x): return x >= lower_bound and x <= upper_bound

    value = f(mid)
    while not good_enough(value):
        if value > y: high = mid
        else: low = mid
        mid = (low + high) / 2.0
        value = f(mid)

    return mid

def square(x): return x * x


sqrt = slow_inverse(square)

print(sqrt(1000000000))

#########################################  FIND HTML TAGS  #########################################

# ---------------
# User Instructions
#
# Write a function, findtags(text), that takes a string of text
# as input and returns a list of all the html start tags in the
# text. It may be helpful to use regular expressions to solve
# this problem.

import re

def findtags(text):
    regex = r'<[ ]*[a-zA-Z]+[ ]*(?:[a-zA-Z]+[ ]*=[ ]*".+[ ]*")*/?>'   # couldn't solve it without help.
    pat = re.compile(regex)
    return re.findall(pat, text)


testtext1 = """
My favorite website in the world is probably 
<a href="www.udacity.com">Udacity</a>. If you want 
that link to open in a <b>new tab</b> by default, you should
write <a href="www.udacity.com"target="_blank">Udacity</a>
instead!
"""

testtext2 = """
Okay, so you passed the first test case. <let's see> how you 
handle this one. Did you know that 2 < 3 should return True? 
So should 3 > 2. But 2 > 3 is always False.
"""

testtext3 = """
It's not common, but we can put a LOT of whitespace into 
our HTML tags. For example, we can make something bold by
doing <         b           > this <   /b    >, Though I 
don't know why you would ever want to.
"""

def test():
    assert findtags(testtext1) == ['<a href="www.udacity.com">',
                                   '<b>',
                                   '<a href="www.udacity.com"target="_blank">']
    assert findtags(testtext2) == []
    assert findtags(testtext3) == ['<         b           >']
    return 'tests pass'

print (test())


