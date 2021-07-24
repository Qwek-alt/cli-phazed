VAL = 0
SCORE_VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                '0': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 25}

def phazed_score(hand):
    '''Return the score for the hand.'''
    score = 0
    
    # add score value of each card to the score
    for card in hand:
        card_score = SCORE_VALUES[card[VAL]]
        score += card_score
        
    return score