from helper_functions.phase_type import phazed_phase_type
from helper_functions.group_type import colour_check, run_check

VAL, SUIT = 0, 1
WILDS = ['AC', 'AD', 'AH', 'AS']
ACC_VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
              '0': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 1}
RUN_ORDER = ['2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K', '2',
             '', ''] 
COLOUR = {'D': 'red', 'H': 'red', 'C': 'black', 'S': 'black'}

PLAY_ORDER = {1: [5, None], 2: [5, None], 3: [1, 2], 4: [1, 2, 3, 4], 
              5: [1, 2, 3, 4]}  # {play_type: [valid prev_play_types], ...}
ACC_TOTALS = [34, 55, 68, 76, 81, 84, 86, 87, 88]

PHASE_GROUPS = {1: [[1], [1]], 2: [[2]], 3: [[6], [6]], 4: [[3], [3]], 
                5: [[4]], 6: [[6, 7], [6, 7]], 7: [[5], [3]]}
MAX_WILDS = 8

printing = True  # for debugging/displaying error messages

def table_acc_complete(table):
    '''Return True if all accumulations on table are complete, 
    and False otherwise'''
    # find accumulation phases on the table (phase 3 or 6)
    for phase in table:
        (phase_type, phase_content) = phase
        if phase_type in [3, 6]:

            # check if each accumulation group is incomplete/invalid
            for group in phase_content:
                acc_val_list = [ACC_VALUES[card[VAL]] for card in group]
                if acc_valid(acc_val_list) in [None, False]:
                    if printing: print("❌❌ acc not complete/surpassed")
                    return False  # incomplete/invalid phase

    # all accumualtion phases on table are complete
    return True

def acc_valid(table_group, card=''):
    '''
    Return True if accumulation is complete; False if it surpassed the next 
    accumulation goal (invalid); None if it is not complete yet.
    Arguments:
        table_group (list): list of cards in group on the table
        card (opt. string): card being added to table group
    Returns:
        bool: 
            -- True if accumulation is complete
            -- False if next accumulation goal surpassed (invalid)
            -- None if accumulation is not complete yet
    '''
    acc_val_list = [ACC_VALUES[c[VAL]] for c in table_group]
    acc_total = sum(acc_val_list)

    # find next accumulation goal
    i = 0
    while i < (len(ACC_TOTALS)):
        # goal reached
        if acc_total == ACC_TOTALS[i]:
            # -- card being added: increment to next goal
            if card: 
                i += 1
            # -- card not being added: declare acc_goal
            else:
                acc_goal = ACC_TOTALS[i]
                break
        # goal surpassed - increment to next goal
        elif acc_total >= ACC_TOTALS[i]:
            i += 1
        # goal not yet reached - declare acc_goal
        else:
            acc_goal = ACC_TOTALS[i]
            break
    
    # add card value to accumulation total
    if card:
        acc_total += ACC_VALUES[card[VAL]]

    # accumulation complete
    if acc_total == acc_goal:
        return True
    
    # accumulation goal not yet reached - accumulation incomplete
    elif acc_total < acc_goal:
        return None
    
    # accumulation goal surpassed - invalid
    else:
        return False

def phazed_is_valid_play(play, player_id, table, turn_history, phase_status, 
                        hand, discard, player_freq=4):
    '''Return True if `play` is valid relative to the current game state,
    and False otherwise.'''
    (play_type, play_content) = play

    # preventing magic numbers and assigning items to variables
    if turn_history:
        # prevent magic numbers when indexing (..._i means index variable)
        prev_turn_i, prev_plays_i = -1, -1
        prev_play_i, prev_player_id_i = -1, 0

        prev_play = turn_history[prev_turn_i][prev_plays_i][prev_play_i]
        (prev_play_type, _) = prev_play
        prev_player_id = turn_history[prev_turn_i][prev_player_id_i]
    else:
        prev_play_type, prev_player_id = None, None

    # check previous player has ended turn (type 5 play type)
    if prev_player_id not in [player_id, None] and prev_play_type != 5:
        if printing: print(f"prev_player_id: {prev_player_id}")
        if printing: print("❌ not player's turn - in the middle of previous player's turn")
        return False

    # check play type order and player id order
    if player_id == prev_player_id:  # continuing turn
        if prev_play_type not in PLAY_ORDER[play_type]:
            pass
    else:  # starting turn
        if prev_player_id:
            next_player_id = prev_player_id+1 if prev_player_id in \
                [i for i in range(player_freq-1)] else 0
        else:
            next_player_id = player_id
        
        # check if previous player has ended turn and play type is pick-up play
        if prev_play_type not in [5, None] or play_type not in [1, 2]:
            if printing: print("❌ previous player hasn't finished turn or supposed to be pick-up play")
            return False

        # check player id order
        elif player_id != next_player_id:
            if printing: print(f"❌ wrong player id order the\n    player id is {player_id} but next player id should be {next_player_id}")
            return False

    # check play type order
    if prev_play_type not in PLAY_ORDER[play_type]:
        if printing: print("❌ previous play not correct order")
        return False

    # play type [1]: pick a card from deck
    if play_type == 1:
        return True

    # play type [2]: pick a card from discard
    elif play_type == 2:

        # check if card being picked up from discard is actual card on 
        # discard pile
        if play_content == discard:
            return True
        if printing: print('❌ not actual discard')
        return False

    # play type [3]: place a phase
    elif play_type == 3:
        (phase_type, phase) = play_content

        # check if cards are in hand
        for group in phase:
            for card in group:
                if card not in hand:
                    if printing: print('❌ card not in hand')
                    return False

        # check if player already has a phase on the table
        # or if player's current phase matches phase status
        if table[player_id] != (None, []) \
            or phase_type != phase_status[player_id] + 1:
            if printing: print('❌ phase on table/current phase does not match phase status')
            return False

        # check phase play validity
        elif phase_type not in phazed_phase_type(phase):
            if printing: print('❌ phase validity')
            return False

        return True

    # play type [4]: add to table
    elif play_type == 4:
        (card, (table_player_id, group_num, card_index)) = play_content

        # check if card are in hand
        if card not in hand:
            if printing: print('❌ card not in hand')
            return False

        # check if player has a phase on the table yet
        if table[player_id] in [[None, []], (None, [])]:
            if printing: print('❌ no phase on table yet')
            return False

        table_phase = table[table_player_id][0]
        table_group = table[table_player_id][1][group_num]
        table_group_type = PHASE_GROUPS[table_phase][group_num][0]
        next_index = len(table_group)

        # check index
        # -- card can only be inserted to front/back of run (group 4 or 5)
        # -- card index must be within the range of [0, next index] inclusive
        if (table_group_type in [4, 5] and card_index not in [0, next_index]) \
            or not (0 <= card_index <= next_index):
            if printing: print("❌ incorrect index")
            return False

        val_list = [c[VAL] for c in table_group]
        suit_list = [c[SUIT] for c in table_group]
        
        # wild immediately passed for non-accumulation groups (groups 1-5)
        if table_group_type in [1, 2, 3, 4, 5] and card in WILDS:
            return True

        # group [1] or [3]: cards of the same value
        elif table_group_type in [1, 3]:
            if card[VAL] in val_list:
                return True
            if printing: print("❌ incorrect val")
            return False

        # group [2]: cards of the same suit
        elif table_group_type == 2:
            if card[SUIT] in suit_list:
                return True
            if printing: print("❌ incorrect suit")
            return False

        # group [4] or [5]: run of cards
        elif table_group_type in [4, 5]:

            # insert card in a copy of table_group (`new_group`)
            new_group = table_group[:]
            new_group.insert(card_index, card)

            # additional colour check for group [5]
            if table_group_type == 5:
                if not colour_check(new_group):
                    if printing: print("❌ not same colour")
                    return False

            # check if card already in run
            if card in table_group:
                if printing: print("❌ card already in run")
                return False

            # check if resulting run is valid
            if not run_check(new_group, MAX_WILDS):
                if printing: print("❌ resulting run not valid")
                return False

            # valid add to run
            return True

        # group [6] or [7]: 34-accumulation of cards
        elif table_group_type in [6, 7]:

            # additional colour check for group [7]
            if table_group_type == 7:

                # add card to group
                new_table_group = table_group.insert(card_index, card)

                # check if same colour
                if not colour_check(new_table_group):
                    if printing: print("❌ not same colour")
                    return False

            # check if new group total is surpasses goal total
            if acc_valid(table_group, card) is False:
                if printing: print("❌ new group total surpassed the goal total")
                return False

            # playing last card - check if new group is *complete*
            if len(hand) == 1:
                if not acc_valid(table_group, card):
                    if printing: print("❌ new group incomplete")
                    return False

        # valid add to accumulation
        return True

    # play type [5]: discard
    elif play_type == 5:

        # check if card in hand
        if play_content not in hand:
            if printing: print('❌ card not in hand')
            return False

        # check if all accumulations on table are complete
        for phase in table:
            (phase_type, phase_content) = phase

            # find accumulation phases on the table (phase 3 or 6)
            if phase_type in [3, 6]:

                # check if each accumulation group is incomplete/invalid
                for table_group in phase_content:
                    if not acc_valid(table_group):
                        if printing: print('❌ table accumulation not complete')
                        return False

        # valid discard
        return True

    # invalid play type
    return False