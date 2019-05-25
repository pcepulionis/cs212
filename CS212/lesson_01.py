'''
8 - Straight Flush - (8,11)
7 - Four Cards - (7,14,2)
6 - Full House - (6,8,13)
5 - Flush - (5, [10,8,7,5,3])
4 - Straight - (4, 11)
3 - 3 Cards  - (3, 7, [7,7,7,5,2])
2 - Two Pairs - (2,11,3,[13,11,11,3,3])
1 - Pair of Twos - (1,2,[11,6,3,2,2])
0 - High Card - (0,[7,5,4,3,2])
'''

def poker(hands):
    "Return a list of winning hands: poker([hand,...]) => [hand,...]"
    return allmax(hands, key=hand_rank)

def allmax(iterable, key=None):
    "Return a list of all items equal to the max of the iterable."
    result, maxval = [], None
    key = key or (lambda x:x)
    for x in iterable:
        xval = key(x)
        if not result or xval > maxval:
            result, maxval = [x], xval
        elif xval == maxval:
            result.append(x)
    return result
    

def card_ranks(cards):
    "Return a list of the ranks, sorted with higher first."
    ''' 
    First solution. Changed based on teacher example.
    
    ranks = [r for r,s in cards]
    ranks = [10 if r=='T' else r for r in ranks]
    ranks = [11 if r=='J' else r for r in ranks]
    ranks = [12 if r=='Q' else r for r in ranks]
    ranks = [13 if r=='K' else r for r in ranks]
    ranks = [14 if r=='A' else r for r in ranks]
    ranks = [int(r) for r in ranks]
    '''
    ranks = ['--23456789TJQKA'.index(r) for r,s in cards]
    ranks.sort(reverse=True)
    return [5,4,3,2,1] if (ranks == [14,5,4,3,2]) else ranks

def hand_rank(hand):
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):            # straight flush
        return (8, max(ranks))
    elif kind(4, ranks):                           # 4 of a kind
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):        # full house
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):                              # flush
        return (5, ranks)
    elif straight(ranks):                          # straight
        return (4, max(ranks))
    elif kind(3, ranks):                           # 3 of a kind
        return (3, kind(3,ranks), ranks)
    elif two_pair(ranks):                          # 2 pair
        return (2, two_pair(ranks), ranks)   #### I think my solution here is better. 
    elif kind(2, ranks):                           # kind
        return (1, kind(2,ranks), ranks)
    else:                                          # high card
        return (0, ranks)

def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    return all(v == 1  for v in  [ranks[a] - ranks[a+1] for a , s  in enumerate(ranks[:-1])])
    ''' 
    Better solution from teacher
    return (max(ranks) - min(ranks) == 4) and len(set(ranks))==5
    '''

def kind(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == n:
            return r
    return None

def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [s for r, s in hand]
    return len(set(suits)) == 1 

def two_pair(ranks):
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None."""
    tup = ()
    for r in ranks:
        if ranks.count(r) == 2:
            tup = tup + (r,)
    if len(list(set(tup))) == 2:
        return list(set(tup))
    else:
        return None
    '''
    Another Solution:
    pair = kind(2,ranks)
    lowpair - kind(2,list(reversed(ranks)))
    if pair and lowpair != pair:
        return(pair, lowpair)
    else:
        return None
    '''
import random
mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC'] 
def deal(numhands, n=5, deck = mydeck):
    """ 
    Shuffle the deck and deal out numhands n-card hands
    This builds a deck of 52 cards. 
    """
    
    '''
    My Solution
    deal_back = []
    random.shuffle(deck)
    for i in range(numhands):
        deal_back.append(mydeck[i*n:i*n+n])
    return deal_back
    '''
    random.shuffle(deck)
    return [deck[n*i:n*(i+1)] for i in range(numhands)]

def test():
    "Test cases for the functions in poker program."
    sf = "6C 7C 8C 9C TC".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full House
    tp = "5S 5D 9H 9C 6S".split() # Two pairs
    assert straight([9, 8, 7, 6, 5]) == True
    assert straight([9, 8, 8, 6, 5]) == False
    assert flush(sf) == True
    assert flush(fk) == False
    assert card_ranks(sf) == [10, 9, 8, 7, 6]
    assert card_ranks(fk) == [9, 9, 9, 9, 7]
    assert card_ranks(fh) == [10, 10, 10, 7, 7]
    assert poker([sf, fk, fh]) == [sf]
    assert poker([fh, fk]) == [fk]
    assert poker([fh, fh]) == [fh, fh]
    assert poker([fh]) == [fh]
    assert poker([sf] + 99*[fh]) == [sf]
    assert hand_rank(sf) == (8,10)
    assert hand_rank(fk) == (7,9,7)
    assert hand_rank(fh) == (6,10,7)
    return "tests pass"


print(test())

'''
def hand_percentages(n=700):
    "Sample n random hands and print a table of percentages for each type of hand."
    counts = [0] * 9
    for i in range(int(n/10)):
        for hand in deal(10):
            ranking = hand_rank(hand)[0]
            counts[ranking] += 1
    for i in reversed(range(9)):
        print("%14s: %6.3f %%" (hand_names[i], 100.*counts[i]/n))
hand_percentages()
'''