##################### NO LEAD ZEROS #####################

# --------------
# User Instructions
#
# Modify the function compile_formula so that the function
# it returns, f, does not allow numbers where the first digit
# is zero. So if the formula contained YOU, f would return
# False anytime that Y was 0

import re
import itertools
import string


def compile_formula(formula, verbose=False):
	"""Compile formula into a function. Also return letters found, as a str,
	in same order as parms of function. The first digit of a multi-digit
	number can't be 0. So if YOU is a word in the formula, and the function
	is called with Y eqal to 0, the function should return False."""

	# modify the code in this function.

	letters = ''.join(set(re.findall('[A-Z]', formula)))
	parms = ', '.join(letters)
	tokens = map(compile_word, re.split('([A-Z]+)', formula))
	body = ''.join(tokens)

	first_letters = set(re.findall(r'\b([A-Z])[A-Z]', formula))

	if first_letters:
		tests = ' and '.join(L+'!=0' for L in first_letters)
		body = '%s and (%s)' % (tests, body)

	f = 'lambda %s: %s' % (parms, body)
	if verbose:
		print(f)
	return eval(f), letters



def compile_word(word):
	"""Compile a word of uppercase letters as numeric digits.
	E.g., compile_word('YOU') => '(1*U+10*O+100*Y)'
	Non-uppercase words uncahanged: compile_word('+') => '+'"""
	if word.isupper():
		terms = [('%s*%s' % (10 ** i, d))
				 for (i, d) in enumerate(word[::-1])]
		return '(' + '+'.join(terms) + ')'
	else:
		return word


def faster_solve(formula):
	"""Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
	Input formula is a string; output is a digit-filled-in string or None.
	This version precompiles the formula; only one eval per formula."""
	f, letters = compile_formula(formula)
	for digits in itertools.permutations((1, 2, 3, 4, 5, 6, 7, 8, 9, 0), len(letters)):
		try:
			if f(*digits) is True:
				table = str.maketrans(letters, ''.join(map(str, digits)))
				return formula.translate(table)
		except ArithmeticError:
			pass


def test():
	assert faster_solve('A + B == BA') == None  # should NOT return '1 + 0 == 01'
	assert faster_solve('YOU == ME**2') == ('289 == 17**2' or '576 == 24**2' or '841 == 29**2')
	assert faster_solve('X / X == X') == '1 / 1 == 1'
	return 'tests pass'

print(test())


##################### FLOOR PUZZLE #####################

#------------------
# User Instructions
#
# Hopper, Kay, Liskov, Perlis, and Ritchie live on
# different floors of a five-floor apartment building.
#
# Hopper does not live on the top floor.
# Kay does not live on the bottom floor.
# Liskov does not live on either the top or the bottom floor.
# Perlis lives on a higher floor than does Kay.
# Ritchie does not live on a floor adjacent to Liskov's.
# Liskov does not live on a floor adjacent to Kay's.
#
# Where does everyone live?
#
# Write a function floor_puzzle() that returns a list of
# five floor numbers denoting the floor of Hopper, Kay,
# Liskov, Perlis, and Ritchie.

import itertools

def floor_puzzle():
	floors = bottom, _, _, _, top = [1, 2, 3, 4, 5]
	orderings = list(itertools.permutations(floors))

	solution = next((Hopper, Kay, Liskov, Perlis, Ritchie)
		for (Hopper, Kay, Liskov, Perlis, Ritchie) in orderings
		if not Hopper is top
		if not Kay is bottom
		if not (Liskov in [bottom, top])
		if Perlis > Kay
		if not abs(Ritchie - Liskov) is 1
		if not abs(Liskov - Kay) is 1
	)
	return list(solution)

print(floor_puzzle())



##################### SUBPALINDROME  #####################

# --------------
# User Instructions
#
# Write a function, longest_subpalindrome_slice(text) that takes
# a string as input and returns the i and j indices that
# correspond to the beginning and end indices of the longest
# palindrome in the string.
#
# Grading Notes:
#
# You will only be marked correct if your function runs
# efficiently enough. We will be measuring efficency by counting
# the number of times you access each string. That count must be
# below a certain threshold to be marked correct.
#
# Please do not use regular expressions to solve this quiz!



def longest_subpalindrome_slice(text):
	"Return (i, j) such that text[i:j] is the longest palindrome in text."
	if text == "":
		return (0, 0)

	candidates = [grow(text, start, end)
					for start in range(len(text))
					for end in (start, start+1)]
	return max(candidates, key = lambda x: x[1] - x[0])

def grow(text, start, end):
	while start>0 and end < len(text) and text[start-1].lower() == text[end].lower():
		start -= 1
		end   += 1
	return (start, end)

def test():
	L = longest_subpalindrome_slice
	assert L('racecar') == (0, 7)
	assert L('Racecar') == (0, 7)
	assert L('RacecarX') == (0, 7)
	assert L('Race carr') == (7, 9)
	assert L('') == (0, 0)
	assert L('something rac e car going') == (8,21)
	assert L('xxxxx') == (0, 5)
	assert L('Mad am I ma dam.') == (0, 15)
	return 'tests pass'

print (test())