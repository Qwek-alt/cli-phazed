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

bots = []
import importlib
bonus = False
filenames = [f'bonusbot{i}' for i in range(4)] if bonus else [f'normalbot{i}' for i in range(4)]
importnames = [f'bot{i}' for i in range(4)]
for i in range(4):
    filename = filenames[i]
    importname = importnames[i]
    try:
        importlib.import_module(filename)

    except ImportError:
        print(f"{filename} not found...")
    else:
        bots.append(f'Bot{i}')
print(f"Bots available: {', '.join(bots)}")


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

def numerical_input(question):
    '''Prompts user to give a numerical input. Returns the number as an integer
    or prompts for user again if an invalid input is given.'''
    try:
        reply = int(input(f'{question}: '))
        return reply
    except ValueError:
        return numerical_input("... Please input a number")

def choice_input(question, choices, returnvalues):
    reply = input(f"{question}: [{'/'.join(choices)}]: ").lower()
    for i in range(len(choices)):
        if reply in choices[i].lower():
            return returnvalues[i]
        if reply not in choices:
            return choice_input("... Please input either", choices, returnvalues)


# MAIN GAME FUNCTIONS
##############################################################################
def game(bonus, players):
    '''Main game loop - runs gameplay as described in gamespec.pdf'''
    pass

def round():
    '''Called at the beginning of each round. The round ends when (1) a player
    places all of their cards on the table, (2) the deck is exhausted or (3)
    each player has played 50 times. '''
    # Set initial values for the round
    pass
    # 

# GAME SETUP
##############################################################################
# Default Settings: Normal Game with 4 players
bonus = False
player_freq = 4
player_names = ["Human", "Bot0", "Bot0", "Bot0"]

# Check if user wants to use default settings
print(f"\nDefault Settings: {'Bonus' if bonus else 'Normal'} Game with automatic card handling and {player_freq} players: {nl}{nl.join(player_names)}")
default = yes_no_input("→ Use default settings?")

# Custom Settings
if not default:
    player_names = []

    # Normal or Bonus Game
    bonus = yes_no_input("→ Bonus game?")

    # Number of players
    player_freq = numerical_input("→ Input number of players")

    # Card handling
    #  automatic: auto-shuffle and handle cards | non-automatic: customise which card is in which hand and enter custom card inputs when handling cards
    handle = yes_no_input("→ Automatic card handling?")

    # Set player types
    for i in range(player_freq):
        name = choice_input(f"→ Input player type", ["Human"]+bots, ["Human"]+bots)
        player_names.append(name)
    
    print(f"\nCustom Settings: {'Bonus' if bonus else 'Normal'} Game {'with' if handle else 'without'} automatic card handling and {player_freq} players: {nl}{nl.join(player_names)}")

# CALL GAME FUNCTION
