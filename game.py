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

# Can import up to 4 bots: bot0, bot1, bot2 and bot3 per game type
import player as bot0
import player_bonus as bot0

# HELPER FUNCTIONS
##############################################################################
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


    # 



# GAME SETUP
##############################################################################
# Default Settings: Normal Game with 4 players
bonus = False
player_freq = 4
player_names = ["human", "bot0", "bot0", "bot0", "bot0"]

# Check if user wants to use default settings
print(f'Default Settings: {"Bonus" if bonus else "Normal"} Game with \
    {player_freq} players: ')
default = yes_no_input("→ Use default settings?")

if not default:
    # Normal or Bonus Game
    bonus = yes_no_input("→ Bonus game?")

    # Number of players
    player_freq = numerical_input("→ Input Number of players")

    # Set players

print(f'default: {default}, bonus: {bonus}, players: {player_freq}')

# CALL GAME FUNCTION
