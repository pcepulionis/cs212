"""
UNIT 1: Bowling:

You will write the function bowling(balls), which returns an integer indicating
the score of a ten-pin bowling game.  balls is a list of integers indicating
how many pins are knocked down with each ball.  For example, a perfect game of
bowling would be described with:

    >>> bowling([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
    300

The rules of bowling are as follows:

(1) A game consists of 10 frames. In each frame you roll one or two balls,
except for the tenth frame, where you roll one, two, or three.  Your total
score is the sum of your scores for the ten frames.
(2) If you knock down fewer than ten pins with your two balls in the frame,
you score the total knocked down.  For example, bowling([8, 1, 7, ...]) means
that you knocked down a total of 9 pins in the first frame.  You score 9 point
for the frame, and you used up two balls in the frame. The second frame will
start with the 7.
(3) If you knock down all ten pins on your second ball it is called a 'spare'
and you score 10 points plus a bonus: whatever you roll with your next ball.
The next ball will also count in the next frame, so the next ball counts twice
(except in the tenth frame, in which case the bonus ball counts only once).
For example, bowling([8, 2, 7, ...]) means you get a spare in the first frame.
You score 10 + 7 for the frame; the second frame starts with the 7.
(4) If you knock down all ten pins on your first ball it is called a 'strike'
and you score 10 points plus a bonus of your score on the next two balls.
(The next two balls also count in the next frame, except in the tenth frame.)
For example, bowling([10, 7, 3, ...]) means that you get a strike, you score
10 + 7 + 3 = 20 in the first frame; the second frame starts with the 7.

"""

def bowling(balls):
    "Compute the total score for a player's game of bowling."
    ## bowling([int, ...]) -> int
    total = 0
	for i in range(10):
		score, balls = score_frame(balls)
		total += score
	return total

def score_frame(balls):
	n_used, n_scoring = ((1, 3) if balls[0] is 10
						else (2, 3) if sum(balls[:2]) is 10
						else (2, 2))

	return sum(balls[:n_scoring]), balls[n_used:]


def test_bowling():
    assert   0 == bowling([0] * 20)
    assert  20 == bowling([1] * 20)
    assert  80 == bowling([4] * 20)
    assert 190 == bowling([9,1] * 10 + [9])
    assert 300 == bowling([10] * 12)
    assert 200 == bowling([10, 5,5] * 5 + [10])
    assert  11 == bowling([0,0] * 9 + [10,1,0])
    assert  12 == bowling([0,0] * 8 + [10, 1,0])

test_bowling()

"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming. 
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""

import itertools


def logic_puzzle():
    "Return a list of the names of the people, in the order they arrive."
    days = (mon, tue, wed, thu, fri) = (1, 2, 3, 4, 5)
    possible_days = list(itertools.permutations(days))
    return next(answer(Wilkes=Wilkes, Hamming=Hamming, Minsky=Minsky,
                       Knuth=Knuth, Simon=Simon)
                for (Wilkes, Hamming, Minsky, Knuth, Simon) in possible_days
                if Knuth == Simon + 1  # 6
                for (programmer, writer, manager, designer, _) in possible_days
                if Knuth == manager + 1  # 10
                and thu != designer  # 7
                and programmer != Wilkes and writer != Minsky  # 2, 4
                for (laptop, droid, tablet, iphone, _) in possible_days
                if set([laptop, Wilkes]) == set([mon, writer])  # 11
                and set([programmer, droid]) == set([Wilkes, Hamming])  # 3
                and (iphone == tue or tablet == tue)  # 12
                and designer != droid  # 9
                and Knuth != manager and tablet != manager  # 5
                and wed == laptop  # 1
                and fri != tablet  # 8
                )


def answer(**names):
    "Given a dict of {name:day}, return a list of names sorted by day."
    return sorted(names, key=lambda name: names[name])


assert logic_puzzle() == ['Wilkes', 'Simon', 'Knuth', 'Hamming', 'Minsky']


"""
UNIT 3: Functions and APIs: Polynomials
A polynomial is a mathematical formula like:
	30 * x**2 + 20 * x + 10
More formally, it involves a single variable (here 'x'), and the sum of one
or more terms, where each term is a real number multiplied by the variable
raised to a non-negative integer power. (Remember that x**0 is 1 and x**1 is x,
so 'x' is short for '1 * x**1' and '10' is short for '10 * x**0'.)
We will represent a polynomial as a Python function which computes the formula
when applied to a numeric value x.  The function will be created with the call:
	p1 = poly((10, 20, 30))
where the nth element of the input tuple is the coefficient of the nth power of x.
(Note the order of coefficients has the x**n coefficient neatly in position n of
the list, but this is the reversed order from how we usually write polynomials.)
poly returns a function, so we can now apply p1 to some value of x:
	p1(0) == 10
Our representation of a polynomial is as a callable function, but in addition,
we will store the coefficients in the .coefs attribute of the function, so we have:
	p1.coefs == (10, 20, 30)
And finally, the name of the function will be the formula given above, so you should
have something like this:
	>>> p1
	<function 30 * x**2 + 20 * x + 10 at 0x100d71c08>
	>>> p1.__name__
	'30 * x**2 + 20 * x + 10'
Make sure the formula used for function names is simplified properly.
No '0 * x**n' terms; just drop these. Simplify '1 * x**n' to 'x**n'.
Simplify '5 * x**0' to '5'.  Similarly, simplify 'x**1' to 'x'.
For negative coefficients, like -5, you can use '... + -5 * ...' or
'... - 5 * ...'; your choice. I'd recommend no spaces around '**'
and spaces around '+' and '*', but you are free to use your preferences.
Your task is to write the function poly and the following additional functions:
	is_poly, add, sub, mul, power, deriv, integral
They are described below; see the test_poly function for examples.
"""
from collections import defaultdict

def decorator(d):
	"Make function d a decorator: d wraps a function fn."
	import functools
	def _d(fn):
		return functools.update_wrapper(d(fn), fn)
	functools.update_wrapper(_d, d)
	return _d

@decorator
def memo(f):
	"""Decorator that caches the return value for each call to f(*args).
	Then when called again with same args, we can just look it up."""
	cache = {}
	def _f(*args):
		try:
			return cache[args]
		except KeyError:
			result = f(*args)
			try:
				cache[args] = result
			except TypeError: # args refuses to be a dict key
				pass
			return result
	_f.cache = cache
	return _f

def poly(coefs):
	"""Return a function that is the polynomial with these coefficients.
	For example if coefs=(10, 20, 30) return the function of x that computes
	'30 * x**2 + 20 * x + 10'.  Also store coefs on the .coefs attribute of
	the function, and the str of the formula on the .__name__ attribute.'"""
	return polynomial(canonical(coefs))

@memo
def polynomial(coefs):
	"""Return a polynomial function with these attributes.  Memoized, so any
	two polys with the same coefficients will be identical polys."""
	# Build a function by evaluating a lambda in the empty environment.
	# Horner's rule involves fewer multiplications than the normal formula...
	p = eval('lambda x: ' + horner_formula(coefs), {})
	p.__name__ = polynomial_formula(coefs)
	p.coefs = coefs
	return p

def horner_formula(coefs):
	"""A relatively efficient form to evaluate a polynomial.
	E.g.:  horner_formula((10, 20, 30, 0, -50))
		   == '(10 + x * (20 + x * (30 + x * x * -50)))',
	which is 4 multiplies and 3 adds."""
	c = coefs[0]
	if len(coefs) == 1:
		return str(c)
	else:
		factor = 'x * ' + horner_formula(coefs[1:])
		return factor if c == 0 else '(%s + %s)' % (c, factor)

def polynomial_formula(coefs):
	"""A simple human-readable form for a polynomial.
	E.g.:  polynomial_formula((10, 20, 30, 0, -50))
		   == '-50 * x**4 + 30 * x**2 + 20 * x + 10',
	which is 7 multiplies and 3 adds."""
	terms = [term(c, n) for (n, c) in reversed(list(enumerate(coefs))) if c != 0]
	return ' + '.join(terms)

def term(c, n):
	"Return a string representing 'c * x**n' in simplified form."
	if n == 0:
		return str(c)
	xn = 'x' if (n == 1) else ('x**' + str(n))
	return xn if (c == 1) else '-' + xn if (c == -1) else str(c) + ' * ' + xn

def canonical(coefs):
	"Canonicalize coefs by dropping trailing zeros and converting to a tuple."
	if not coefs: coefs = [0]
	elif isinstance(coefs, (int, float)): coefs = [coefs]
	else: coefs = list(coefs)
	while coefs[-1] == 0 and len(coefs) > 1:
		del coefs[-1]
	return tuple(coefs)

def is_poly(x):
	"Return true if x is a poly (polynomial)."
	## For examples, see the test_poly function
	return callable(x) and hasattr(x, 'coefs')

def add(p1, p2):
	"Return a new polynomial which is the sum of polynomials p1 and p2."
	coefs = [0] * max(len(p1.coefs), len(p2.coefs))
	for (n, c) in enumerate(p1.coefs): coefs[n] = c
	for (n, c) in enumerate(p2.coefs): coefs[n] += c
	return poly(coefs)

def sub(p1, p2):
	"Return a new polynomial which is p1 - p2."
	coefs = [0] * max(len(p1.coefs), len(p2.coefs))
	for (n, c) in enumerate(p1.coefs): coefs[n] = c
	for (n, c) in enumerate(p2.coefs): coefs[n] -= c
	return poly(coefs)

def mul(p1, p2):
	"Return a new polynomial which is the product of polynomials p1 and p2."
	# Given terms a*x**n and b*x**m, accumulate a*b in results[n+m]
	results = defaultdict(int)
	for (n, a) in enumerate(p1.coefs):
		for (m, b) in enumerate(p2.coefs):
			results[n + m] += a * b
	return poly([results[i] for i in range(max(results)+1)])

def power(p, n):
	"Return a poly which is p to the nth power (n a non-negative integer)."
	if n == 0:
		return poly((1,))
	if n % 2 == 0:
		return power(mul(p, p), n//2)
	else:
		return mul(p, power(p, n-1))

def deriv(p):
	"Return the derivative of a function p (with respect to its argument)."
	return poly([n*c for (n, c) in enumerate(p.coefs) if n > 0])

def integral(p, C=0):
	"Return the integral of a function p (with respect to its argument)."
	return poly([C] + [float(c)/(n+1) for (n, c) in enumerate(p.coefs)])

def test_poly():
	global p1, p2, p3, p4, p5, p9
	# global to ease debugging in an interactive session

	p1 = poly((10, 20, 30))
	assert p1(0) == 10
	for x in (1, 2, 3, 4, 5, 1234.5):
		assert p1(x) == 30 * x**2 + 20 * x + 10
	assert same_name(p1.__name__, '30 * x**2 + 20 * x + 10')

	assert is_poly(p1)
	assert not is_poly(abs) and not is_poly(42) and not is_poly('cracker')

	p3 = poly((0, 0, 0, 1))
	assert p3.__name__ == 'x**3'
	p9 = mul(p3, mul(p3, p3))
	#assert p9 == poly([0,0,0,0,0,0,0,0,0,1])
	assert p9(2) == 512
	p4 =  add(p1, p3)
	assert same_name(p4.__name__, 'x**3 + 30 * x**2 + 20 * x + 10')

	assert same_name(poly((1, 1)).__name__, 'x + 1')
	assert (power(poly((1, 1)), 10).__name__ ==
			'x**10 + 10 * x**9 + 45 * x**8 + 120 * x**7 + 210 * x**6 + 252 ' +
			'* x**5 + 210 * x**4 + 120 * x**3 + 45 * x**2 + 10 * x + 1')

	assert add(poly((10, 20, 30)), poly((1, 2, 3))) == poly((11, 22, 33))
	assert sub(poly((10, 20, 30)), poly((1, 2, 3))) == poly((9, 18, 27))
	assert (mul(poly((10, 20, 30)), poly((1, 2, 3)))
			== poly((10, 40, 100, 120, 90)))
	assert power(poly((1, 1)), 2) == poly((1, 2, 1))
	assert (power(poly((1, 1)), 10)
			== poly((1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1)))

	assert deriv(p1) == poly((20, 60))
	assert integral(poly((20, 60))) == poly((0, 20, 30))
	p5 = poly((0, 1, 2, 3, 4, 5))
	assert same_name(p5.__name__,
					 '5 * x**5 + 4 * x**4 + 3 * x**3 + 2 * x**2 + x')
	assert p5(1) == 15
	assert p5(2) == 258
	assert same_name(deriv(p5).__name__,
					 '25 * x**4 + 16 * x**3 + 9 * x**2 + 4 * x + 1')
	assert deriv(p5)(1) == 55
	assert deriv(p5)(2) == 573
	#Additional Test Case:
	p6 = poly((1,))
	assert integral(p6)(10) == 10

def same_name(name1, name2):
	"""Use same_name rather than name1 == name2 to allow for some
	variation in naming conventions."""
	def canonical_name(name): return name.replace(' ', '').replace('+-', '-')
	return canonical_name(name1) == canonical_name(name2)

class poly(object):
	"""poly objects are like the poly functions we defined earlier, but are
	objects of a class. We coerce arguments to poly, so you can do (x + 1)
	and the 1 will be converted to a poly first."""

	def __init__(self, coefs):
		coefs = canonical(coefs)
		self.fn = eval('lambda x: ' + horner_formula(coefs), {})
		self.__name__ = polynomial_formula(coefs)
		self.coefs = coefs

	def __call__(self, x): return self.fn(x)

	def __eq__(self, other):
		return isinstance(other, poly) and self.coefs == other.coefs

	def __add__(self, p2): return add(self, coerce_poly(p2)) # p + p2
	def __sub__(self, p2): return sub(self, coerce_poly(p2)) # p - p2
	def __mul__(self, p2): return mul(self, coerce_poly(p2)) # p * p2
	def __pow__(self, n): return power(self, n)              # p ^ n
	def __neg__(self): return poly((-c for c in self.coefs)) # - p
	def __pos__(self): return self                           # + p

	# A need the _r methods so that 1 + x works as well as x + 1.

	def __rmul__(self, p2): return mul(self, coerce_poly(p2)) # 5 * x
	def __radd__(self, p2): return add(self, coerce_poly(p2)) # 1 + x

	# I added a __hash__ method after a suggestion by Jeffrey Tratner

	def __hash__(self): return hash(self.coefs)

	def __repr__(self):
		return ''

def coerce_poly(p):
	"Make this into a poly if it isn't already."
	return p if isinstance(p, poly) else poly(p)

def is_poly(p): return isinstance(p, poly)

def Poly(formula):
	"Parse the formula using eval in an environment where x is a poly."
	return eval(formula, {'x': poly((0, 1))})

"""
Now for an extra credit challenge: arrange to describe polynomials with an
expression like '3 * x**2 + 5 * x + 9' rather than (9, 5, 3).  You can do this
in one (or both) of two ways:
(1) By defining poly as a class rather than a function, and overloading the
__add__, __sub__, __mul__, and __pow__ operators, etc.  If you choose this,
call the function test_poly1().  Make sure that poly objects can still be called.
(2) Using the grammar parsing techniques we learned in Unit 5. For this
approach, define a new function, Poly, which takes one argument, a string,
as in Poly('30 * x**2 + 20 * x + 10').  Call test_poly2().
"""

def test_poly1():
	# I define x as the polynomial 1*x + 0.
	x = poly((0, 1))
	# From here on I can create polynomials by + and * operations on x.
	newp1 =  30 * x**2 + 20 * x + 10 # This is a poly object, not a number!
	assert p1(100) == newp1(100) # The new poly objects are still callable.
	assert same_name(p1.__name__,newp1.__name__)
	assert (x + 1) * (x - 1) == x**2 - 1 == poly((-1, 0, 1))

def test_poly2():
	newp1 = Poly('30 * x**2 + 20 * x + 10')
	assert p1(100) == newp1(100)
	assert same_name(p1.__name__,newp1.__name__)


test_poly()
test_poly1()
test_poly2()
print("tests pass")




Lesson 22:
Practice Exam
 1. Quiz: Bowling
 2. Quiz: Logic Puzzle
 3. Quiz: Polynomials
 4. Quiz: Parking Lot Search
 5. Quiz: Darts Probability
 6. Quiz: Portmanteau
 7. Congratulations
Toggle Sidebar
Parking Lot Search
"""
UNIT 4: Search
Your task is to maneuver a car in a crowded parking lot. This is a kind of
puzzle, which can be represented with a diagram like this:
| | | | | | | |
| G G . . . Y |
| P . . B . Y |
| P * * B . Y @
| P . . B . . |
| O . . . A A |
| O . S S S . |
| | | | | | | |
A '|' represents a wall around the parking lot, a '.' represents an empty square,
and a letter or asterisk represents a car.  '@' marks a goal square.
Note that there are long (3 spot) and short (2 spot) cars.
Your task is to get the car that is represented by '**' out of the parking lot
(on to a goal square).  Cars can move only in the direction they are pointing.
In this diagram, the cars GG, AA, SSS, and ** are pointed right-left,
so they can move any number of squares right or left, as long as they don't
bump into another car or wall.  In this diagram, GG could move 1, 2, or 3 spots
to the right; AA could move 1, 2, or 3 spots to the left, and ** cannot move
at all. In the up-down direction, BBB can move one up or down, YYY can move
one down, and PPP and OO cannot move.
You should solve this puzzle (and ones like it) using search.  You will be
given an initial state like this diagram and a goal location for the ** car;
in this puzzle the goal is the '.' empty spot in the wall on the right side.
You should return a path -- an alternation of states and actions -- that leads
to a state where the car overlaps the goal.
An action is a move by one car in one direction (by any number of spaces).
For example, here is a successor state where the AA car moves 3 to the left:
| | | | | | | |
| G G . . . Y |
| P . . B . Y |
| P * * B . Y @
| P . . B . . |
| O A A . . . |
| O . . . . . |
| | | | | | | |
And then after BBB moves 2 down and YYY moves 3 down, we can solve the puzzle
by moving ** 4 spaces to the right:
| | | | | | | |
| G G . . . . |
| P . . . . . |
| P . . . . * *
| P . . B . Y |
| O A A B . Y |
| O . . B . Y |
| | | | | | | |
You will write the function
	solve_parking_puzzle(start, N=N)
where 'start' is the initial state of the puzzle and 'N' is the length of a side
of the square that encloses the pieces (including the walls, so N=8 here).
We will represent the grid with integer indexes. Here we see the
non-wall index numbers (with the goal at index 31):
 |  |  |  |  |  |  |  |
 |  9 10 11 12 13 14  |
 | 17 18 19 20 21 22  |
 | 25 26 27 28 29 30 31
 | 33 34 35 36 37 38  |
 | 41 42 43 44 45 46  |
 | 49 50 51 52 53 54  |
 |  |  |  |  |  |  |  |
The wall in the upper left has index 0 and the one in the lower right has 63.
We represent a state of the problem with one big tuple of (object, locations)
pairs, where each pair is a tuple and the locations are a tuple.  Here is the
initial state for the problem above in this format:
"""

puzzle1 = (
 ('@', (31,)),
 ('*', (26, 27)),
 ('G', (9, 10)),
 ('Y', (14, 22, 30)),
 ('P', (17, 25, 33)),
 ('O', (41, 49)),
 ('B', (20, 28, 36)),
 ('A', (45, 46)),
 ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39,
		40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)))

# A solution to this puzzle is as follows:

#     path = solve_parking_puzzle(puzzle1, N=8)
#     path_actions(path) == [('A', -3), ('B', 16), ('Y', 24), ('*', 4)]

# That is, move car 'A' 3 spaces left, then 'B' 2 down, then 'Y' 3 down,
# and finally '*' moves 4 spaces right to the goal.

# Your task is to define solve_parking_puzzle:

N = 8

def solve_parking_puzzle(start, N=N):
	"""Solve the puzzle described by the starting position (a tuple
	of (object, locations) pairs).  Return a path of [state, action, ...]
	alternating items; an action is a pair (object, distance_moved),
	such as ('B', 16) to move 'B' two squares down on the N=8 grid."""
	return shortest_path_search(start, psuccessors, is_goal)

def is_goal(state):
	"Goal is when the car (*) overlaps a goal square (@)."
	d = dict(state)
	return set(d['*']) & set(d['@'])

def psuccessors(state):
	"""State is a tuple of (('c': sqs),...); return a {state:action} dict
	where action is of form ('c', dir), where dir is +/-1 or +/-N."""

	def _update(car, new_loc):
		"Return a new (car, new_loc) tuple, dropping old value of car and adding new."
		# Sort the keys to make sure the result is canonical.
		d = dict(state)
		d[car] = new_loc
		return tuple(sorted(d.items()))

	state = set(state)
	results = {}
	occupied = {s for (c, sqs) in state for s in sqs if c != '@'}
	for (c, sqs) in state:
		if c not in '|@': # Walls and goals can't move
			step = sqs[1]-sqs[0]
			# Either move the max of sqs up, or the min of sqs down
			for (d, loc) in [(step, max(sqs)), (-step, min(sqs))]:
				for i in range(0, N)[1: -1]: # Might take a step of n unit
					if loc+d*i in occupied:
						break # Stop when you hit something
					results[_update(c, tuple(q+d*i for q in sqs))] = (c, d*i)
	return results

# But it would also be nice to have a simpler format to describe puzzles,
# and a way to visualize states.
# You will do that by defining the following two functions:

def locs(start, n, incr=1):
	"Return a tuple of n locations, starting at start and incrementing by incr."
	return tuple(start+incr*i for i in range(n))

def grid(cars, N=N):
	"""Return a tuple of (object, locations) pairs -- the format expected for
	this puzzle.  This function includes a wall pair, ('|', (0, ...)) to
	indicate there are walls all around the NxN grid, except at the goal
	location, which is the middle of the right-hand wall; there is a goal
	pair, like ('@', (31,)), to indicate this. The variable 'cars'  is a
	tuple of pairs like ('*', (26, 27)). The return result is a big tuple
	of the 'cars' pairs along with the walls and goal pairs."""
	goals = ((N**2)//2 - 1,)
	walls = (locs(0, N) + locs(N*(N-1), N) + locs(N, N-2, N) + locs(2*N-1, N-2, N))
	walls = tuple(w for w in walls if w not in goals)
	return cars + (('|', walls), ('@', goals))


def show(state, N=N):
	"Print a representation of a state as an NxN grid."
	# Initialize and fill in the board.
	board = ['.'] * N**2
	for (c, squares) in state:
		for s in squares:
			board[s] = c
	# Now print it out
	for i,s in enumerate(board):
		print s,
		if i % N == N - 1: print

# Here we see the grid and locs functions in use:

puzzle1 = grid((
	('*', locs(26, 2)),
	('G', locs(9, 2)),
	('Y', locs(14, 3, N)),
	('P', locs(17, 3, N)),
	('O', locs(41, 2, N)),
	('B', locs(20, 3, N)),
	('A', locs(45, 2))))

puzzle2 = grid((
	('*', locs(26, 2)),
	('B', locs(20, 3, N)),
	('P', locs(33, 3)),
	('O', locs(41, 2, N)),
	('Y', locs(51, 3))))

puzzle3 = grid((
	('*', locs(25, 2)),
	('B', locs(19, 3, N)),
	('P', locs(36, 3)),
	('O', locs(45, 2, N)),
	('Y', locs(49, 3))))


# Here are the shortest_path_search and path_actions functions from the unit.
# You may use these if you want, but you don't have to.

def shortest_path_search(start, successors, is_goal):
	"""Find the shortest path from start state to a state
	such that is_goal(state) is true."""
	if is_goal(start):
		return [start]
	explored = set() # set of states we have visited
	frontier = [ [start] ] # ordered list of paths we have blazed
	while frontier:
		path = frontier.pop(0)
		s = path[-1]
		for (state, action) in successors(s).items():
			if state not in explored:
				explored.add(state)
				path2 = path + [action, state]
				if is_goal(state):
					return path2
				else:
					frontier.append(path2)
	return []

def path_actions(path):
	"Return a list of actions in this path."
	return path[1::2]

def test_parking():
	assert valid_solution(puzzle1, 4)
	assert valid_solution(puzzle2, 7)
	assert valid_solution(puzzle3, 7)
	assert valid_solution(puzzle4, 8)
	assert locs(26, 2) == (26, 27)
	assert locs(20, 3, 8) == (20, 28, 36)
	assert same_state(
		grid((('*', locs(25, 2)),
			  ('B', locs(19, 3, N)),
			  ('P', locs(36, 3)),
			  ('O', locs(45, 2, N)),
			  ('Y', locs(49, 3)))),
		(('*', (25, 26)), ('B', (19, 27, 35)), ('P', (36, 37, 38)),
		 ('O', (45, 53)), ('Y', (49, 50, 51)),
		 ('|', (0, 1, 2, 3, 4, 5, 6, 7, 56, 57, 58, 59, 60, 61, 62, 63,
				8, 16, 24, 32, 40, 48, 15, 23, 39, 47, 55)),
			('@', (31,))))
	return "tests pass"

puzzle4 = grid((
	('*', locs(26, 2)),
	('G', locs(9, 2)),
	('Y', locs(14, 3, N)),
	('P', locs(17, 3, N)),
	('O', locs(41, 2, N)),
	('B', locs(20, 3, N)),
	('A', locs(45, 2)),
	('S', locs(51, 3))))

def valid_solution(puzzle, length):
	"Does solve_parking_puzzle solve this puzzle in length steps?"
	path = solve_parking_puzzle(puzzle)
	return (len(path_actions(path)) == length and
			same_state(path[0], puzzle) and
			is_goal(path[-1]) and
			all(legal_step(path[i:i+3]) for i in range(0,len(path)-2, 2)))

def legal_step(path):
	"A legal step has an action that leads to a valid successor state."
	# Here the path must be of the form [s0, a, s1].
	state1, action, state2 = path
	succs = psuccessors(state1)
	return state2 in succs and succs[state2] == action

def same_state(state1, state2):
	"Two states are the same if all corresponding sets of locs are the same."
	d1, d2 = dict(state1), dict(state2)
	return all(set(d1[key]) == set(d2[key]) for key in set(d1) | set(d2))

  
Your code displayed no output
Solution:

We can use shortest_path_search if we can define a successor and goal test function. That's what I'll do:

N = 8

def solve_parking_puzzle(start, N=N):
    """Solve the puzzle described by the starting position (a tuple
    of (object, locations) pairs).  Return a path of [state, action, ...]
    alternating items; an action is a pair (object, distance_moved),
    such as ('B', 16) to move 'B' two squares down on the N=8 grid."""
    return shortest_path_search(grid(start, N), psuccessors, is_goal)

def is_goal(state):
    "Goal is when the car (*) overlaps a goal square (@)."
    d = dict(state)
    return set(d['*']) & set(d['@'])

def psuccessors(state):
    """State is a tuple of (('c': sqs),...); return a {state:action} dict
    where action is of form ('c', dir), where dir is +/-1 or +/-N."""
    results = {}
    occupied = set(s for (c, sqs) in state for s in sqs if c != '@')
    for (c, sqs) in state:
        if c not in '|@': # Walls and goals can't move
            diff = sqs[1]-sqs[0]
            # Either move the max of sqs up, or the min of sqs down
            for (d, start) in [(diff, max(sqs)), (-diff, min(sqs))]:
                for i in range(1, N-2):
                    s = start + d*i
                    if s in occupied:
                        break # Stop when you hit something
                    results[update(state,c,tuple(q+d*i for q in sqs))]=(c,d*i)
    return results

def update(tuples, key, val):
    "Return a new (key, val) tuple, dropping old value of key and adding new."
    # Sort the keys to make sure the result is canonical.
    d = dict(tuples)
    d[key] = val
    return tuple(sorted(d.items()))
That's basically it. But we also need to define locs and grid:

def locs(start, n, incr=1):
    "Return a tuple of n locations, starting at start and go up by incr."
    return tuple(start+i*incr for i in range(n))

def grid(cars, N=N):
    """Return a tuple of (object, locations) pairs -- the format expected for
    this puzzle.  This function includes a wall pair, ('|', (0, ...)) to
    indicate there are walls all around the NxN grid, except at the goal
    location, which is the middle of the right-hand wall; there is a goal
    pair, like ('@', (31,)), to indicate this. The variable 'cars'  is a
    tuple of pairs like ('*', (26, 27)). The return result is a big tuple
    of the 'cars' pairs along with the walls and goal pairs."""
    goals = ((N**2)//2 - 1,)
    walls = (locs(0, N) + locs(N*(N-1), N) + locs(N, N-2, N)
             + locs(2*N-1, N-2, N))
    walls = tuple(w for w in walls if w not in goals)
    return cars + (('|', walls), ('@', goals))
Here is a test suite:

def test_parking():
    assert valid_solution(puzzle1, 4)
    assert valid_solution(puzzle2, 7)
    assert valid_solution(puzzle3, 7)
    assert valid_solution(puzzle4, 8)
    assert locs(26, 2) == (26, 27)
    assert locs(20, 3, 8) == (20, 28, 36)
    assert same_state(
        grid((('*', locs(25, 2)),
              ('B', locs(19, 3, N)),
              ('P', locs(36, 3)),
              ('O', locs(45, 2, N)),
              ('Y', locs(49, 3)))),
        (('*', (25, 26)), ('B', (19, 27, 35)), ('P', (36, 37, 38)),
         ('O', (45, 53)), ('Y', (49, 50, 51)),
         ('|', (0, 1, 2, 3, 4, 5, 6, 7, 56, 57, 58, 59, 60, 61, 62, 63,
                8, 16, 24, 32, 40, 48, 15, 23, 39, 47, 55)),
            ('@', (31,))))

puzzle4 = grid((
    ('*', locs(26, 2)),
    ('G', locs(9, 2)),
    ('Y', locs(14, 3, N)),
    ('P', locs(17, 3, N)),
    ('O', locs(41, 2, N)),
    ('B', locs(20, 3, N)),
    ('A', locs(45, 2)),
    ('S', locs(51, 3))))

def valid_solution(puzzle, length):
    "Does solve_parking_puzzle solve this puzzle in length steps?"
    path = solve_parking_puzzle(puzzle)
    return (len(path_actions(path)) == length and
            same_state(path[0], puzzle) and
            is_goal(path[-1]) and
            all(legal_step(path[i:i+3]) for i in range(0,len(path)-2, 2)))

def legal_step(path):
    "A legal step has an action that leads to a valid successor state."
    # Here the path must be of the form [s0, a, s1].
    state1, action, state2 = path
    succs = psuccessors(state1)
    return state2 in succs and succs[state2] == action

def same_state(state1, state2):
    "Two states are the same if all corresponding sets of locs are the same."
    d1, d2 = dict(state1), dict(state2)
    return all(set(d1[key]) == set(d2[key]) for key in set(d1) | set(d2))




# Unit 5: Probability in the game of Darts

"""
In the game of darts, players throw darts at a board to score points.
The circular board has a 'bulls-eye' in the center and 20 slices
called sections, numbered 1 to 20, radiating out from the bulls-eye.
The board is also divided into concentric rings.  The bulls-eye has
two rings: an outer 'single' ring and an inner 'double' ring.  Each
section is divided into 4 rings: starting at the center we have a
thick single ring, a thin triple ring, another thick single ring, and
a thin double ring.  A ring/section combination is called a 'target';
they have names like 'S20', 'D20' and 'T20' for single, double, and
triple 20, respectively; these score 20, 40, and 60 points. The
bulls-eyes are named 'SB' and 'DB', worth 25 and 50 points
respectively. Illustration (png image): http://goo.gl/i7XJ9
There are several variants of darts play; in the game called '501',
each player throws three darts per turn, adding up points until they
total exactly 501. However, the final dart must be in a double ring.
Your first task is to write the function double_out(total), which will
output a list of 1 to 3 darts that add up to total, with the
restriction that the final dart is a double. See test_darts() for
examples. Return None if there is no list that achieves the total.
Often there are several ways to achieve a total.  You must return a
shortest possible list, but you have your choice of which one. For
example, for total=100, you can choose ['T20', 'D20'] or ['DB', 'DB']
but you cannot choose ['T20', 'D10', 'D10'].
"""

from collections import defaultdict

def test_darts():
	"Test the double_out function."
	assert double_out(170) == ['T20', 'T20', 'DB']
	assert double_out(171) == None
	assert double_out(100) in (['T20', 'D20'], ['DB', 'DB'])
	for total in range(2, 159) + [160, 161, 164, 167, 170]:
		assert valid_out(double_out(total), total)
	for total in [0, 1, 159, 162, 163, 165, 166, 168, 169, 171, 200]:
		assert double_out(total) == None

def valid_out(darts, total):
	"Does this list of targets achieve the total, and end with a double?"
	return (0 < len(darts) <= 3 and darts[-1].startswith('D')
			and sum(map(value, darts)) == total)

def value(target):
	"The numeric value of a target."
	if target == 'OFF': return 0
	ring, section = target[0], target[1:]
	r = 'OSDT'.index(target[0])
	s = 25 if section == 'B' else int(section)
	return r * s

"""
My strategy: I decided to choose the result that has the highest valued
target(s) first, e.g. always take T20 on the first dart if we can achieve
a solution that way.  If not, try T19 first, and so on. At first I thought
I would need three passes: first try to solve with one dart, then with two,
then with three.  But I realized that if we include 0 as a possible dart
value, and always try the 0 first, then we get the effect of having three
passes, but we only have to code one pass.  So I creted ordered_points as
a list of all possible scores that a single dart can achieve, with 0 first,
and then descending: [0, 60, 57, ..., 1].  I iterate dart1 and dart2 over
that; then dart3 must be whatever is left over to add up to total.  If
dart3 is a valid element of points, then we have a solution.  But the
solution, is a list of numbers, like [0, 60, 40]; we need to transform that
into a list of target names, like ['T20', 'D20'], we do that by defining name(d)
to get the name of a target that scores d.  When there are several choices,
we must choose a double for the last dart, but for the others I prefer the
easiest targets first: 'S' is easiest, then 'T', then 'D'.
"""

singles = range(1, 21) + [25]
points  = set(m*s for s in singles for m in (1, 2, 3) if m*s != 75)
doubles = set(2*s for s in singles)
ordered_points = [0] + sorted(points, reverse=True)

def double_out(total):
	"""Return a shortest possible list of targets that add to total,
	where the length <= 3 and the final element is a double.
	If there is no solution, return None."""
	if total > sum(sorted(points, reverse=True)[:3]):
		return None

	for dart1 in ordered_points:
		for dart2 in ordered_points:
			dart3 = total - dart1 - dart2
			if dart3 in doubles:
				solution = [name(dart1), name(dart2), name(dart3, 'D')]
				return [t for t in solution if t != 'OFF']
	return None

def name(d, double=False):
	"""Given an int, d, return the name of a target that scores d.
	If double is true, the name must start with 'D', otherwise,
	prefer the order 'S', then 'T', then 'D'."""
	return ('OFF' if d == 0  else
			'DB'  if d == 50 else
			'SB'  if d == 25 else
			'D' + str(d//2) if (d in doubles and double) else
			'S' + str(d)    if  d in singles else
			'T' + str(d//3) if (d % 3 == 0)  else
			'D' + str(d//2))

"""
It is easy enough to say "170 points? Easy! Just hit T20, T20, DB."
But, at least for me, it is much harder to actually execute the plan
and hit each target.  In this second half of the question, we
investigate what happens if the dart-thrower is not 100% accurate.
We will use a wrong (but still useful) model of inaccuracy. A player
has a single number from 0 to 1 that characterizes his/her miss rate.
If miss=0.0, that means the player hits the target every time.
But if miss is, say, 0.1, then the player misses the section s/he
is aiming at 10% of the time, and also (independently) misses the thin
double or triple ring 10% of the time. Where do the misses go?
Here's the model:
First, for ring accuracy.  If you aim for the triple ring, all the
misses go to a single ring (some to the inner one, some to the outer
one, but the model doesn't distinguish between these). If you aim for
the double ring (at the edge of the board), half the misses (e.g. 0.05
if miss=0.1) go to the single ring, and half off the board. (We will
agree to call the off-the-board 'target' by the name 'OFF'.) If you
aim for a thick single ring, it is about 5 times thicker than the thin
rings, so your miss ratio is reduced to 1/5th, and of these, half go to
the double ring and half to the triple.  So with miss=0.1, 0.01 will go
to each of the double and triple ring.  Finally, for the bulls-eyes. If
you aim for the single bull, 1/4 of your misses go to the double bull and
3/4 to the single ring.  If you aim for the double bull, it is tiny, so
your miss rate is tripled; of that, 2/3 goes to the single ring and 1/3
to the single bull ring.
Now, for section accuracy.  Half your miss rate goes one section clockwise
and half one section counter-clockwise from your target. The clockwise
order of sections is:
	20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5
If you aim for the bull (single or double) and miss on rings, then the
section you end up on is equally possible among all 20 sections.  But
independent of that you can also miss on sections; again such a miss
is equally likely to go to any section and should be recorded as being
in the single ring.
You will need to build a model for these probabilities, and define the
function outcome(target, miss), which takes a target (like 'T20') and
a miss ration (like 0.1) and returns a dict of {target: probability}
pairs indicating the possible outcomes.  You will also define
best_target(miss) which, for a given miss ratio, returns the target
with the highest expected score.
If you are very ambitious, you can try to find the optimal strategy for
accuracy-limited darts: given a state defined by your total score
needed and the number of darts remaining in your 3-dart turn, return
the target that minimizes the expected number of total 3-dart turns
(not the number of darts) required to reach the total.  This is harder
than Pig for several reasons: there are many outcomes, so the search space
is large; also, it is always possible to miss a double, and thus there is
no guarantee that the game will end in a finite number of moves.
"""

def best_target(miss):
    "Return the target that maximizes the expected score."
    return max(targets, key=lambda t: expected_value(t, miss))

def expected_value(target, miss):
    "The expected score of aiming at target with a given miss ratio."
    return sum(value(t)*p for (t, p) in outcome(target, miss).items())

def outcome(target, miss):
    "Return a probability distribution of [(target, probability)] pairs."
    results = defaultdict(float)
    for (ring, ring_prob) in ring_outcome(target, miss):
        for (sect, sect_prob) in section_outcome(target, miss):
            if ring == 'S' and sect.endswith('B'):
                # If sect hits bull, but ring misses out to S ring,
                # then spread the results over all sections.
                for s in sections:
                    results[Target(ring, s)] += (ring_prob * sect_prob) / 20.
            else:
                results[Target(ring, sect)] += (ring_prob * sect_prob)
    return dict(results)

def ring_outcome(target, miss):
    "Return a probability distribution of [(ring, probability)] pairs."
    hit = 1. - miss
    r = target[0]
    if target == 'DB': # misses tripled; can miss to SB or to S
        miss = min(3*miss, 1.)
        hit = 1. - miss
        return [('DB', hit), ('SB', miss/3.), ('S', 2./3.*miss)]
    elif target == 'SB': # Bull can miss in either S or DB direction
        return [('SB', hit), ('DB', miss/4.), ('S', 3/4.*miss)]
    elif r == 'S': # miss ratio cut to miss/5
        return [(r, 1. - miss/5.), ('D', miss/10.), ('T', miss/10.)]
    elif r == 'D': # Double can miss either on board or off
        return [(r, hit), ('S', miss/2), ('OFF', miss/2)]
    elif r == 'T': # Triple can miss in either direction, but both are S
        return [(r, hit), ('S', miss)]

def section_outcome(target, miss):
    "Return a probability distribution of [(section, probability)] pairs."
    hit = 1. - miss
    if target in ('SB', 'DB'):
        misses = [(s, miss/20.) for s in sections]
    else:
        i = sections.index(target[1:])
        misses = [(sections[i-1], miss/2), (sections[(i+1)%20], miss/2)]
    return  [(target[1:], hit)] + misses

def Target(ring, section):
    "Construct a target name from a ring and section."
    if ring == 'OFF':
        return 'OFF'
    elif ring in ('SB', 'DB'):
        return ring if (section == 'B') else ('S' + section)
    else:
        return ring + section

sections = "20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5".split()
targets = set(r+s for r in 'SDT' for s in sections) | set(['SB', 'DB'])

def same_outcome(dict1, dict2):
	"Two states are the same if all corresponding sets of locs are the same."
	return all(abs(dict1.get(key, 0) - dict2.get(key, 0)) <= 0.0001
			   for key in set(dict1) | set(dict2))

def test_darts2():
	assert best_target(0.0) == 'T20'
	assert best_target(0.1) == 'T20'
	assert best_target(0.4) == 'T19'
	assert same_outcome(outcome('T20', 0.0), {'T20': 1.0})
	assert same_outcome(outcome('T20', 0.1),
						{'T20': 0.81, 'S1': 0.005, 'T5': 0.045,
						 'S5': 0.005, 'T1': 0.045, 'S20': 0.09})
	assert (same_outcome(
			outcome('SB', 0.2),
			{'S9': 0.016, 'S8': 0.016, 'S3': 0.016, 'S2': 0.016, 'S1': 0.016,
			 'DB': 0.04, 'S6': 0.016, 'S5': 0.016, 'S4': 0.016, 'S20': 0.016,
			 'S19': 0.016, 'S18': 0.016, 'S13': 0.016, 'S12': 0.016, 'S11': 0.016,
			 'S10': 0.016, 'S17': 0.016, 'S16': 0.016, 'S15': 0.016, 'S14': 0.016,
			 'S7': 0.016, 'SB': 0.64}))


# Unit 6: Fun with Words

"""
A portmanteau word is a blend of two or more words, like 'mathelete',
which comes from 'math' and 'athelete'.  You will write a function to
find the 'best' portmanteau word from a list of dictionary words.
Because 'portmanteau' is so easy to misspell, we will call our
function 'natalie' instead:
	natalie(['word', ...]) == 'portmanteauword'
In this exercise the rules are: a portmanteau must be composed of
three non-empty pieces, start+mid+end, where both start+mid and
mid+end are among the list of words passed in.  For example,
'adolescented' comes from 'adolescent' and 'scented', with
start+mid+end='adole'+'scent'+'ed'. A portmanteau must be composed
of two different words (not the same word twice).
That defines an allowable combination, but which is best? Intuitively,
a longer word is better, and a word is well-balanced if the mid is
about half the total length while start and end are about 1/4 each.
To make that specific, the score for a word w is the number of letters
in w minus the difference between the actual and ideal lengths of
start, mid, and end. (For the example word w='adole'+'scent'+'ed', the
start,mid,end lengths are 5,5,2 and the total length is 12.  The ideal
start,mid,end lengths are 12/4,12/2,12/4 = 3,6,3. So the final score
is
	12 - abs(5-3) - abs(5-6) - abs(2-3) = 8.
yielding a score of 12 - abs(5-(12/4)) - abs(5-(12/2)) -
abs(2-(12/4)) = 8.
The output of natalie(words) should be the best portmanteau, or None
if there is none.
Note (1): I got the idea for this question from
Darius Bacon.  Note (2): In real life, many portmanteaux omit letters,
for example 'smoke' + 'fog' = 'smog'; we aren't considering those.
Note (3): The word 'portmanteau' is itself a portmanteau; it comes
from the French "porter" (to carry) + "manteau" (cloak), and in
English meant "suitcase" in 1871 when Lewis Carroll used it in
'Through the Looking Glass' to mean two words packed into one. Note
(4): the rules for 'best' are certainly subjective, and certainly
should depend on more things than just letter length.  In addition to
programming the solution described here, you are welcome to explore
your own definition of best, and use your own word lists to come up
with interesting new results.  Post your best ones in the discussion
forum. Note (5) The test examples will involve no more than a dozen or so
input words. But you could implement a method that is efficient with a
larger list of words.
"""

import itertools


def natalie(words):
    "Find the best Portmanteau word formed from any two of the list of words."

    def _overlap(a, b):
        anchor = 0
        for i in range(1, min(len(a), len(b))):
            if a[:i] == b[-i:]:
                anchor = i
        if anchor > 0:
            return b[:-anchor], a[:anchor], a[anchor:]

    def _score(P_word):
        start, mid, end = map(len, P_word)
        total = start + mid + end

        return total - (abs(start - total / 4.0) + abs(mid - total / 2.0) + abs(end - total / 4.0))

    Portmanteau_words = [_overlap(a, b) for (a, b) in itertools.permutations(words, 2) if _overlap(a, b)]

    if Portmanteau_words:
        return "".join(max(Portmanteau_words, key=_score))


def test_natalie():
    "Some test cases for natalie"
    assert (natalie(['eskimo', 'escort', 'kimchee', 'kimono', 'cheese'])
            == 'eskimono')
    assert (natalie(['kimono', 'kimchee', 'cheese', 'serious', 'us', 'usage'])
            == 'kimcheese')
    assert (natalie(['circus', 'elephant', 'lion', 'opera', 'phantom'])
            == 'elephantom')
    assert (natalie(['adolescent', 'scented', 'centennial', 'always',
                     'ado', 'centipede'])
            in ('adolescented', 'adolescentennial', 'adolescentipede'))
    assert (natalie(['programmer', 'coder', 'partying', 'merrymaking'])
            == 'programmerrymaking')
    assert (natalie(['int', 'intimate', 'hinter', 'hint', 'winter'])
            == 'hintimate')
    assert (natalie(['morass', 'moral', 'assassination'])
            == 'morassassination')
    assert (natalie(['entrepreneur', 'academic', 'doctor',
                     'neuropsychologist', 'neurotoxin', 'scientist', 'gist'])
            in ('entrepreneuropsychologist', 'entrepreneurotoxin'))
    assert (natalie(['perspicacity', 'cityslicker', 'capability', 'capable'])
            == 'perspicacityslicker')
    assert (natalie(['backfire', 'fireproof', 'backflow', 'flowchart',
                     'background', 'groundhog'])
            == 'backgroundhog')
    assert (natalie(['streaker', 'nudist', 'hippie', 'protestor',
                     'disturbance', 'cops'])
            == 'nudisturbance')
    assert (natalie(['night', 'day']) == None)
    assert (natalie(['dog', 'dogs']) == None)
    assert (natalie(['test']) == None)
    assert (natalie(['']) == None)
    assert (natalie(['ABC', '123']) == None)
    assert (natalie([]) == None)
    assert (natalie(['pedestrian', 'pedigree', 'green', 'greenery'])
            == 'pedigreenery')
    assert (natalie(['armageddon', 'pharma', 'karma', 'donald', 'donut'])
            == 'pharmageddon')
    assert (natalie(['lagniappe', 'appendectomy', 'append', 'lapin'])
            == 'lagniappendectomy')
    assert (natalie(['angler', 'fisherman', 'boomerang', 'frisbee', 'rangler',
                     'ranger', 'rangefinder'])
            in ('boomerangler', 'boomerangefinder'))
    assert (natalie(['freud', 'raelian', 'dianetics', 'jonestown', 'moonies'])
            == 'freudianetics')
    assert (natalie(['atheist', 'math', 'athlete', 'psychopath'])
            in ('psychopatheist', 'psychopathlete'))
    assert (natalie(['hippo', 'hippodrome', 'potato', 'dromedary'])
            == 'hippodromedary')
    assert (natalie(['taxi', 'taxicab', 'cabinet', 'cabin',
                     'cabriolet', 'axe'])
            in ('taxicabinet', 'taxicabriolet'))
    assert (natalie(['pocketbook', 'bookmark', 'bookkeeper', 'goalkeeper'])
            in ('pocketbookmark', 'pocketbookkeeper'))
    assert (natalie(['athlete', 'psychopath', 'athletic', 'axmurderer'])
            in ('psychopathlete', 'psychopathletic'))
    assert (natalie(['info', 'foibles', 'follicles'])
            == 'infoibles')
    assert (natalie(['moribund', 'bundlers', 'bundt'])
            == 'moribundlers')

    return 'tests pass'


print(test_natalie())





