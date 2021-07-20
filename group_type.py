from collections import defaultdict as dd

VAL, SUIT = 0, 1
WILDS = ['AC', 'AD', 'AH', 'AS']
ACC_VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
              '0': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 1}
RUN_ORDER = ['2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K', '2', 
             '', '']
COLOUR = {'D': 'red', 'H': 'red', 'C': 'black', 'S': 'black'}
MIN_NATURAL = 2
ACC_TOTALS = [34, 55, 68, 76, 81, 84, 86, 87, 88]

def set_check(group, mode):
    '''
    Check if `group` is a set of cards of the same value/suit, depending on the
    `mode`.
    -- VAL mode: Return True if group is of the same value and False otherwise.
    -- SUIT mode: Return True if group is of the same suit and False otherwise.
    '''
    num_cards = len(group)

    # store frequency counts of value/suit in `freq_dict`
    freq_dict = dd(int)  # {val: freq, ...} // {suit: freq, ...}
    for card in group:
        if card in WILDS:  # wilds have their own frequency
            freq_dict['wilds'] += 1
        else:
            freq_dict[card[mode]] += 1

    # check if value/suit has at least two natural cards
    # check if the natural and wild cards make up the correct total
    for key in freq_dict.copy():
        if key != 'wilds' and freq_dict[key] >= MIN_NATURAL \
            and freq_dict[key] + freq_dict['wilds'] == num_cards:
            return True
    return False

def colour_check(group, aces_check=False):
    '''
    Check if `group` is a set of cards of the same colour.
    Arguments:
        group(list): list of cards
        aces_check(bool, opt): checks if aces are the same colour too
        -- for phase 6: accumulation of cards of same colour
    Returns:
        bool: True if group is a set of cards of the same colour and False 
            otherwise.
    '''
    num_cards = len(group)
    colour_dict = dd(int)
    
    # store frequency counts of value/suit/colour in `freq_dict`
    for card in group:
        if card in WILDS and not aces_check:
            colour_dict['wilds'] += 1
        else:
            colour_dict[COLOUR[card[SUIT]]] += 1
            
    # check if the natural and wild cards make up the correct total
    if colour_dict['red'] + colour_dict['wilds'] == num_cards \
        or colour_dict['black'] + colour_dict['wilds'] == num_cards:
        return True
    return False

def run_check(group, max_wild, ref='', wild_count=0):
    '''
    Check if `group` is a valid run of cards. [Recursive Function]
    Arguments:
        group(list): list of cards
        max_wild(int): maximum number of wild cards allowed in the run
    Local variables:
        ref(str): reference value for next card
        wild_count(int): number of wild cards in run
    Returns:
        bool: True if group is a run of card; False otherwise
    '''
    # BASE: finished checking whole group
    if not group:
        return True
    else:
        curr_card = group[0]

    # BASE: maximum wild count exceeded
    if wild_count > max_wild:
        return False

    # wild card 
    # -- increment wild card count and update reference value
    if curr_card in WILDS:
        return run_check(group[1:], max_wild,
            RUN_ORDER[RUN_ORDER.index(ref) + 1], wild_count + 1)

    # card follows sequence // first natural card in group
    # -- update reference value for the next card
    if curr_card[VAL] == ref or ref == '':
        return run_check(group[1:], max_wild,
            RUN_ORDER[RUN_ORDER.index(curr_card[VAL]) + 1], wild_count)

    # BASE: card no longer follows the run sequence
    return False

def acc_34_check(group):
    '''Return True if `group` is an accumulation of cards totalling 34 in 
    value.'''
    acc_values = [ACC_VALUES[card[VAL]] for card in group]

    if sum(acc_values) == ACC_TOTALS[0]:
        return True
    return False

def phazed_group_type(group):
    '''Given a list of cards, `group`, return a sorted list of integers 
    indicating card combination types.'''
    result_list = []
    num_cards = len(group)

    # [1] three cards of the same value
    if num_cards == 3 and set_check(group, VAL):
        result_list.append(1)

    # [2] seven cards of the same suit
    if num_cards == 7 and set_check(group, SUIT):
        result_list.append(2)

    # [3] four cards of the same value
    if num_cards == 4 and set_check(group, VAL):
        result_list.append(3)

    # [4] run of eight cards
    if num_cards == 8 and run_check(group, 6):
        result_list.append(4)

    # [5] run of four cards of the same colour
    if num_cards == 4 and run_check(group, 2) and colour_check(group):
        result_list.append(5)

    # [6] 34-accumulation cards
    if acc_34_check(group):
        result_list.append(6)

    # [7] 34-accumulation cards of the same colour
    if acc_34_check(group) and colour_check(group, True):
        result_list.append(7)
    
    return sorted(result_list)

