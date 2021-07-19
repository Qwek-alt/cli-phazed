# Phazed Game
# ABRREVIATIONS:
# -- 'acc' means 'accumulation'
# -- 'val' means 'value'
# -- 'freq' means 'frequency'

# IMPORTS AND CONSTANTS
##############################################################################
YES_REPLIES = ["yes", "y"]
NO_REPLIES = ["no", "n"]
NUM_PHASES = 7
SUITS = ["D", "C", "H", "S"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "0", "J", "Q", "K", "A"]
HAND_SIZE = 10
nl = '\n  • '
MIN_PLAYERS = 2
MAX_PLAYERS = 4
NAME = 0,
PLACING = {1: 'st', 2: 'nd', 3: 'rd'}

# import importlib
from itertools import product
import random

from valid_play import phazed_is_valid_play
from score import phazed_score
from bot0 import rank

# Import Bots
from bot0 import phazed_play as bot0
# from bot1 import phazed_play as bot1
# from bot2 import phazed_play as bot2
# from bot3 import phazed_play as bot3

# Import Bonus Bots
from bonusbot0 import phazed_bonus as bonusbot0
# from bonusbot1 import phazed_bonus as bonusbot1
# from bonusbot2 import phazed_bonus as bonusbot2
# from bonusbot3 import phazed_bonus as bonusbot3

BOTS = {
    "Bot0": bot0,
    # "Bot1": bot1,
    # "Bot2": bot2,
    # "Bot3": bot3,
    "BonusBot0": bonusbot0 #,
    # "BonusBot1": bonusbot1,
    # "BonusBot2": bonusbot2,
    # "BonusBot3": bonusbot3
}

# HELPER FUNCTIONS
##############################################################################
def flatten(list_2d):
    '''Flattens 2 dimentional list to 1 dimentional list.'''
    list = []
    for group in list_2d:
        for card in group:
            list.append(card)
    return list

def yes_no_input(question):
    '''Prompts user to give a Yes or No input. Returns True if user's input is
    part of YES_REPLIES, False if user's input is part of NO_REPLIES and 
    prompts user again if input is not part of either reply type.'''
    reply = input(f'{question} [Yes/No]: ').lower()

    if reply in YES_REPLIES:
        return True
    elif reply in NO_REPLIES:
        return False
    else:
        return yes_no_input("... Please input either")

def numerical_input(question, min, max):
    '''Prompts user to give a numerical input. Returns the number as an integer
    or prompts for user again if an invalid input is given.'''
    span = [i for i in range(min, max+1)]
    try:
        reply = int(input(f"{question} [{'/'.join([str(n) for n in span])}]: "))
        if reply not in span:
            raise ValueError
        return reply
    except ValueError:
        return numerical_input(f"... Please input either", span)

def choice_input(question, choices, returnvalues):
    '''Prompts user to enter an input based on multiple choices, returns the
    appropriate output when a choice is selected and prompts the user again if
    an invalid input is given.'''
    reply = input(f"{question}: [{'/'.join(choices)}]: ").lower()
    choices = [c.lower() for c in choices]
    if reply not in choices:
        return choice_input("... Please input either", choices, 
        returnvalues)
    else:
        for i in range(len(choices)):
            if reply in choices[i]:
                return returnvalues[i]

def card_input(question):
    '''Promps user to enter a card input, returns a correctly formatted version
    or prompts user again if invalid input is given.'''
    reply = input(f"{question}")

# MAIN GAME FUNCTION
##############################################################################
def game(bonus, player_freq, handle, player_names, beginning):
    '''Main game loop - runs gameplay as described in gamespec.pdf'''
    if beginning:  # Game starting from the beginning
        # Set initial values
        hand_num, total_turns = 0, 0
        phase_status = [0 for i in range(player_freq)]
        total_scores = [0 for i in range(player_freq)]
    else:  # 'Loading' and existing game; not starting from the beggining
        hand_num = numerical_input("→ Input hand number", 0, player_freq**2)
        # total_turns = numerical_input("→ Input turn number", 0, 50) --> turn_count
        phase_status = []
        total_scores = []
        for i in range(player_freq):
            phase_status.append(numerical_input(f"→ Input Player {i}'s Current"
            + " Phase", 0, 6))
            total_scores.append(numerical_input(f"→ Input Player {i}'s Current"
            + " Score", 0, 500))

    dealer = hand_num % 4
    player_id = dealer+1 if dealer in [i for i in range(player_freq-1)] else 0

    ### START ROUND ###
    round_flag = True
    while round_flag:
        # Set initial round values
        table = [(None, []), (None, []), (None, []), (None, [])]
        turn_history = []
        turn_count = [0 for i in range(player_freq)]
        round_scores = [0 for i in range(player_freq)]

        if handle:  # Automatic Card Handling
            # Create and Shuffle the Deck
            deck = list(rank+suit for rank, suit in product(RANKS, SUITS))*2
            random.shuffle(deck)

            # Create hands and Distribute the cards
            hands = [[] for i in range(player_freq)]
            for i in range(HAND_SIZE):
                for j in range(player_freq):
                    hands[j].append(deck.pop())
            
            # Create initial discard
            discard = deck.pop()

        else:  # Manual card handling
            # Input hands and discard
            hands_input = input(f'→ Input Player hands: ').split()
            hands = []
            for j in range(player_freq):
                hand = []
                for i in range(HAND_SIZE):
                    hand.append(hands_input.pop(0))
                hands.append(hand)
            discard = input(f'→ Input Initial Discard: ')

        # Displaying starting hand information
        print(f"\n=== STARTING HAND NUMBER {hand_num} ===")
        for i in range(player_freq):
            print(f"Player {i} ({player_names[i]}) has completed phase {phase_status[i]}.")
        print(f"Player {dealer} deals and Player {player_id} starts.")
        for i in range(player_freq):
            print(f"Player {i} ({player_names[i]}) was dealt {hands[i]}")
        
        ### START OF TURN ###
        turn_flag = True
        
        print(f"--- Player {player_id} ({player_names[player_id]})'s " +
            f"{ turn_count[player_id]}"+
            f"{PLACING[turn_count[player_id]] if turn_count[player_id] in [1, 2, 3] else 'th'} turn ---")
        while turn_flag:
            # START OF PLAYER'S TURN
            hand = hands[player_id]
            phase_type = phase_status[player_id] + 1
            phase_on_table = False if table[player_id] in [(None, []), 
                [None, []]] else True
            name = player_names[player_id]
            
            # Check player type and ask for Input of Call bot function
            player = player_names[player_id]

            # human player
            if player[0].lower() == "h":

                if yes_no_input("→ Display game information?"):
                    # Rank the hand and display game information
                    _ , ranked_hand = rank(hand[:], phase_type, phase_on_table, table[:], player_id)
                    print(f"  • Hand: {ranked_hand}\n  • Table: {table}  \n  • Phase Status: {phase_status}\n  • Discard: {discard}")

                while True: 
                    try: 
                        player = input(f"→ Input play/bot[{'/'.join(list(BOTS.keys()))}]: ")
                        if player not in list(BOTS.keys()):
                            # Break down play format
                            play_content = player
                            play_content = play_content.strip("()")
                            play_type = int(play_content[0])
                            play_content = play_content[3:]
                            
                            if play_type in [3, 4]:
                                if play_type == 3:
                                    phase_type = int(play_content[1])
                                    text_phase_content = play_content[4:]
                                    characters = "',"
                                    for char in characters:
                                        text_phase_content = text_phase_content.replace(char, "") 
                                    text_phase_content = text_phase_content.strip("[]").split("] [")
                                    phase = []
                                    for group in text_phase_content:
                                        group = group.split()
                                        phase.append(group)

                                    play = (play_type, (phase_type, phase))
                                elif play_type == 4:
                                    card = play_content[2:4]
                                    table_player_id = int(play_content[8])
                                    group_num = int(play_content[11])
                                    card_index = int(play_content[14])

                                    play = (play_type, (card, (table_player_id, group_num, card_index)))
                            else:
                                card = None if play_type == 1 else play_content[1:3]
                                play = (play_type, card)
                            
                        break
                    except:
                        print("  Uh... Please try again. Make sure that your play is correctly formatted.")

            # bot player
            if player in list(BOTS.keys()):
                bot_func = BOTS[player]
                play = bot_func(player_id, table[:], turn_history, phase_status,
                    hand[:], discard)

                play_type, play_content = play

                # extract variables for later
                if play_type in [3, 4]:
                    if play_type == 3:
                        phase_type, phase = play_content
                    else:
                        card, (table_player_id, group_num, card_index) = play_content
                else:
                    card = play_content
            

            # VALIDATE PLAY
            if not phazed_is_valid_play(play, player_id, table[:], turn_history, 
                            phase_status, hand[:], discard, player_freq):
                print(f"❗ INVALID PLAY: {play}.")
                print(f"Function call: {(player_id, table[:], turn_history, phase_status, hand, discard)}")
                input(f"→ Press any key to exit the program.")

                return

            # PICK UP FROM DECK
            if play_type == 1:
                if handle:
                    card = deck.pop()
                    print(f"Player {player_id} ({name}) played {play}"
                    + f" and picked up {card}")
                else:
                    card = card_input(f"→ Player {player_id} ({name}) played {play}"
                    +" and picked up ")
            else:
                print(f"Player {player_id} ({name}) played {play}")
            
            # UPDATE HAND
            # -- add card(s) to hand (pick-up play)
            if play_type in [1, 2]:
                hand.append(card)
                if play_type == 2:
                    discard = None

            # -- removing card(s) from hand
            elif play_type in [4, 5, 6]:  # remove card
                hand.remove(card)
            else:  # remove phase
                for group in phase:
                    for card in group:
                        hand.remove(card)

            # UPDATE TURN HISTORY
            if turn_history:
                # prevent magic numbers when indexing (..._i means index variable)
                prev_turn_i, prev_plays_i = -1, -1
                prev_play_i = -1

                prev_play = turn_history[prev_turn_i][prev_plays_i][prev_play_i]
                (prev_play_type, _) = prev_play
            else:
                prev_play_type = None
            # -- starting turn - create turn array
            if not turn_history or prev_play_type == 5:
                turn_history.append((player_id, [play]))
            # -- continuing turn
            else:
                turn_history[prev_turn_i][prev_plays_i].append(play)

            # UPDATE table
            if play_type == 3:
                # UPDATE phase status
                table[player_id] = (phase_type, phase)
                phase_status[player_id] += 1
            elif play_type == 4:
                table[table_player_id][1][group_num].insert(card_index, card)

            # END ROUND
            # -- no more cards in hand or more than 30 turns dy == (infinite loop maybe)
            if (play_type in [3, 4, 5] and not hand) or (30 in turn_count) or \
                (handle and not deck):
                print(f"\n=== END OF HAND {hand_num} ===")

                # Update Turn Count
                for i in range(player_freq):
                    if not hands[i]:
                        print(f"Player {i} ({player_names[i]}) had no cards left in their hand. {total_scores[i]} + 0 = {total_scores[i]}")
                    else:
                        score = phazed_score(hands[i])
                        round_scores[i] = score
                        print(f"Player {i} had {hands[i]} left in their hand. {total_scores[i]} + {score} = {total_scores[i]+score}.")
                        total_scores[i] += score
                
                # Update Hand Number
                hand_num += 1

                # End Game if any player has reached the final phase
                if 7 in phase_status:
                    # Find the Winner
                    winner_i = ''
                    for i in range(player_freq):
                        status = phase_status[i]
                        if status == NUM_PHASES:
                            if winner_i == '':
                                winner_i = i
                            
                            # tie break with score
                            elif total_scores[i] < total_scores[winner_i]:
                                winner_i = i
                            
                            # tie break with turn
                            elif total_scores[i] == total_scores[winner_i]:
                                if turn_count[i] < turn_count[winner_i]:
                                    winner_i = i
                    
                    # Create Placing
                    placing = []  # 1st, 2nd, 3rd, 4th
                    placing.append(winner_i)
                    
                    total_scores_copy = total_scores[:]
                    total_scores_copy[winner_i] = 999  # change winner score to large val
                    sorted_total_scores_copy = sorted(total_scores_copy)
                    for i in range(player_freq-1):
                        placing.append(total_scores.index(sorted_total_scores_copy[i]))

                    print(f"\n=== End of Game ===\n🥳 Player {phase_status.index(NUM_PHASES)} won!")
                    return
                    
                turn_flag = False

                if round_flag: 
                    round_flag = yes_no_input("\n→ Next Hand?")

            # Discard Play
            if play_type in [5, 6]:
                # Update discard
                discard = card

                # Update turn count
                turn_count[player_id] += 1

                # Next player's turn
                player_id = player_id + 1 if player_id in [i for i in 
                                                range(player_freq-1)] else 0
                
                # Display turn info
                if turn_flag and round_flag:
                    print(f"--- Player {player_id} ({player_names[player_id]})'s " +
                        f"{ turn_count[player_id]}"+
                        f"{PLACING[turn_count[player_id]] if turn_count[player_id] in [1, 2, 3] else 'th'} turn ---")

# GAME SETUP
##############################################################################
# Default Settings
bonus = False
player_freq = 4
handle = True
player_names = ["Human", "Bot0", "Bot0", "Bot0"]
beginning = True

# Display default settings and Check if user wants to use defaults
print(f"\nDefault Settings: {'Bonus' if bonus else 'Normal'} Game " +
    f"{'with' if handle else 'without'} automatic card handling and " + 
    f"{player_freq} players: {nl}{nl.join(player_names)}")
default = yes_no_input("→ Use default settings?")

# Custom Setting Configuration
if not default:
    player_names = []

    # Set bonus, player frequency and card handling
    # bonus = yes_no_input("→ Bonus game?")
    player_freq = numerical_input("→ Input number of players", MIN_PLAYERS,
        MAX_PLAYERS)
    handle = yes_no_input("→ Automatic card handling?")

    # Set player types/names and whether to start from beginning
    for i in range(player_freq):
        name = choice_input(f"→ Input player type", ["Human"]+list(BOTS.keys()), 
            ["Human"]+list(BOTS.keys()))
        player_names.append(name)
    beginning = yes_no_input('→ Start from the beginning?')

    
    print(f"\nCustom Settings: {'Bonus' if bonus else 'Normal'} Game " +
    f"{'with' if handle else 'without'} automatic card handling and " + 
    f"{player_freq} players: {nl}{nl.join(player_names)}")

# CALL GAME FUNCTION
##############################################################################
game(bonus, player_freq, handle, player_names, beginning)
