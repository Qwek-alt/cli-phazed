from question3 import phazed_is_valid_play 
from bot59 import rank
from question4 import phazed_score
from q5_dumb_bot import dumb_bot_phazed_play
from q6_submission_5 import phazed_bonus
from bot60 import phazed_play_60
from bot59 import phazed_play_59

from itertools import product
import random
# from tabulate import tabulate
import csv

DATAFILES = ['data_games.csv', 'data_rounds.csv', 'data_scores.csv']
NUM_PHASES = 7
SUITS = ["D", "C", "H", "S"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "0", "J", "Q", "K", "A"]
NUM_PLAYERS = 4  # can't change for now - because of validator
HAND_SIZE = 10
BOTS = {'46': phazed_play_46, 
        '47': phazed_play_47, 
        '49': phazed_play_49,
        '51': phazed_play,
        '5': phazed_bonus,
        '0': dumb_bot_phazed_play,
        '59': phazed_play_59,
        '60': phazed_play_60}
        # '48': phazed_play_48,

printing = False  # for debugging
min_printing = False
ROUND = 0
SCORE = 1


def game(PLAYER, self_play, beginning, player_names, game_number):
    placing = []
    GAME_DATA = []
    error_flag = False
    if beginning:
        hand_num = 0
        # SET INITIAL VALUES
        phase_status = [0 for i in range(NUM_PLAYERS)]
        total_scores = [0 for i in range(NUM_PLAYERS)]
    else:
        # INPUT hand number
        hand_num = int(input(f'➡️ Input hand number: '))
        # INPUT phase statuses
        phase_status = [int(input(f'➡️ Input Player {i} phase status: ')) for i in
            range(NUM_PLAYERS)]
        total_scores = [0 for i in range(NUM_PLAYERS)] #TODO: input
    # # GETTING GAME NUMBER
    # with open('data_games.csv', 'r') as fp:
    #     reader = csv.reader(fp)
    #     for last_line in reader:
    #         pass
    #     _, exist_game_number, _, _, _, _ = last_line
    #     if not exist_game_number.isdigit():
    #         game_number = 0
    #     else:
    #         game_number = int(exist_game_number) + 1

    print(f'=== STARTING GAME #{game_number} ===')

    dealer = hand_num % 4
    player_id = dealer + 1 if dealer in [i for i in range(NUM_PLAYERS-1)] else 0

    # with open('data_phase.csv', 'r') as fp:
    #     data_reader = csv.reader(fp)
    #     for name in player_names:
    #         for row in data_reader:
    #             if row[0] == name:
    #                 existing_data = []
    #                 for i, j in [[2, 3], [4, 5], [6, 7], [8, 9], [10, 11], [12, 13], [14, 15]]:
    #                     existing_data.append([int(row[i]), int(row[j])])
    #                 player_data = [row[0], int(row[1])+1] + existing_data
    #                 PHASE_DATA.append(player_data)
    #                 break  # move onto next row
            
    #         # name not found in csv - create new entry
    #         player_data = [name, 1] + [[0, 0] for i in range(NUM_PHASES)]
    #         PHASE_DATA.append(player_data)
    
    round_flag = True
    while round_flag:
        # SET INITIAL VALUES
        table = [(None, []), (None, []), (None, []), (None, [])]
        turn_history = []
        turn_count = [0 for i in range(NUM_PLAYERS)]
        round_scores = [0 for i in range(NUM_PLAYERS)]

        # START ROUND
        if not self_play:
            # INPUT hands
            # hands = [input(f'➡️ Input Player {i} hand: ').split() for i in range(NUM_PLAYERS)]
            hands_input = input(f'➡️ Input Player hands: ').split()
            hands = []
            for j in range(NUM_PLAYERS):
                hand = []
                for i in range(10):
                    hand.append(hands_input.pop(0))
                hands.append(hand)
            # INPUT initial discard
            discard = input(f'➡️ Input Initial Discard: ')

        else:
            # create deck
            deck = list(rank+suit for rank, suit in product(RANKS, SUITS))*2 
            # shuffle deck
            random.shuffle(deck) 
            # create hands
            hands = [[], [], [], []]
            for i in range(HAND_SIZE):
                for j in range(NUM_PLAYERS):
                    hands[j].append(deck.pop())
            # initial discard
            discard = deck.pop()
        
        dealer = hand_num % 4

        # DISPLAY
        print(f'\n=== Starting hand number {hand_num} ===')
        for i in range (NUM_PLAYERS):
            print(f'Player {i} has completed {phase_status[i]}.')
        if printing_yes: print(f'Player {dealer} deals and Player {player_id} starts.')
        for i in range(NUM_PLAYERS):
            print(f'Player {i} was dealt {hands[i]}')
        
        # START OF TURNS IN ROUND
        turn_flag = True
        print(f"--- Player {player_id}'s {turn_count[player_id]} turn ---")
        while turn_flag:
            # START OF 1 PLAYER'S TURN
            if printing: print(f'  {player_id}')
            if printing: print(f'  {table}')
            if printing: print(f'  {turn_history}')
            if printing: print(f'  {phase_status}')
            if printing: print(f'  {discard}')

            # assign variables
            hand = hands[player_id]
            phase_type = phase_status[player_id] + 1
            phase_on_table = False if table[player_id] in [(None, []), 
                [None, []]] else True

            # RANK HAND
            if min_printing: print('ranking...')
            if min_printing: ranked_dict, ranked_list = rank(hand[:], phase_type, phase_on_table, table[:])
            if min_printing: print(f'  ranked_list: {ranked_list}')
            if printing: print(f' ranked_dict: {ranked_dict}')

            # WHAT WOULD BOT #46/#47 DO?
            if min_printing: play_46 = phazed_play_46(player_id, table[:], turn_history, phase_status, hand[:], discard)
            # play_47 = phazed_play_47(player_id, table[:], turn_history, phase_status, hand[:], discard)
            # play_49 = phazed_play_49(player_id, table[:], turn_history, phase_status, hand[:], discard)
            # play_51 = phazed_play(player_id, table[:], turn_history, phase_status, hand[:], discard)
            # play_0 = dumb_bot_phazed_play(player_id, table[:], turn_history, phase_status, hand[:], discard)
            # print(f'  #47 would play: {play_47}')
            # print(f'  #49 would play: {play_49}')
            # print(f'  #51 would play: {play_51}')
            # print(f'  #0 would play: {play_0}')
            #print(f'  #46/47 would play: {play_46}') if play_46 == play_47 else print(f'  #46: {play_46} and #47: {play_47}')

            # CALL PLAYER FUNCTION
            agent = PLAYER[player_id]
            if agent == 'h':
                agent = input(f'➡️ Input agent [46/47/48/49/i]: ')
                if agent == 'i':
                    print(f'    hand: {hand}')
                    _, ranked_list = rank(hand[:], phase_type, phase_on_table, table[:])
                    print(f'    ranked: {ranked_list}\n')
                    print(f'    player_id: {player_id}')
                    print(f'    table: {table}')
                    print(f'    most recent turn history: {turn_history[-1] if turn_history else turn_history}')
                    print(f'    phase_status: {phase_status}')
                    print(f'    discard: {discard}')
                    print(f'    function call: {player_id, table[:], turn_history, phase_status, hand[:], discard}')
                    agent = input(f'➡️ Input agent [46/47/49/i]: ')
            if agent in list(BOTS.keys()):
                player_func = BOTS[agent]
                play = player_func(player_id, table[:], turn_history, phase_status, 
                    hand[:], discard)
                play_type, play_content = play
                if play_type in [3, 4]:
                    if play_type == 3:
                        phase_type, phase = play_content
                    else:
                        card, (table_player_id, group_num, card_index) = play_content
                else:
                    card = play_content
            else:
                play_content = input(f'➡️ Input play content: ')
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
            plays = []
            plays.append([player_names[player_id], play])
            # # DIFFERENCE
            
            # for bot, bot_func in list(BOTS.items()):
            #     if agent == 'h' or (agent != 'h' and bot_func != player_func):
            #         player = "Bot" + str(bot)
            #         bot_play = [player, bot_func(player_id, table, turn_history, phase_status, 
            #         hand[:], discard)]
            #         plays.append(bot_play)
            # # match every play with each other and spot differences
            # for play_x, play_y in combinations(plays, 2):
            #     player_x = play_x[0]
            #     player_y = play_y[0]
            #     if play_x[1] != play_y[1]:
            #         data = [game_number, player_x, player_y, play_x, play_y, [player_id, table, turn_history, phase_status, 
            #         hand[:], discard]]
            #         DIFFERENCE_DATA.append(data)

            # VALIDATE PLAY
            if not phazed_is_valid_play(play, player_id, table[:], turn_history, 
                            phase_status, hand[:], discard):
                input(f"❗ INVALID PLAY: {play}.")
                error_data = [game_number, hand_num, play, (player_id, table[:], turn_history, 
                            phase_status, hand[:], discard)]
                print(f'function call: {(player_id, table[:], turn_history, phase_status, hand, discard)}')
                ERROR_DATA.append(error_data)
                cont = input(f'➡️ Try again? [Y/N/i]: ')
                if cont == 'i':
                    # DISPLAY information
                    print(f'    {player_id}')
                    print(f'    {table}')
                    print(f'    {turn_history}')
                    print(f'    {phase_status}')
                    print(f'    {hand}')
                    print(f'    {discard}')
                
                    error_flag = player_id
                    cont = input(f'➡️ Try again? [Y/N/i]: ')
                if cont in ['y', 'Y']:
                    continue
            
            # PICK UP FROM DECK
            if play_type == 1:
                if self_play:

                    card = deck.pop()
                else:
                    card = input(f'[{player_id}-{turn_count[player_id]}] Player {player_id} played {play} and picked up ')
            else:
                print(f'[{player_id}-{turn_count[player_id]}] Player {player_id} played {play}')

            # UPDATE hand
            # -- adding cards to hand
            if play_type in [1, 2]:
                hand.append(card)
                if play_type == 2:
                    discard = None
            # -- removing cards from hand
            elif play_type in [4, 5]:  # remove card
                hand.remove(card)
            else:  # remove phase
                for group in phase:
                    for card in group:
                        hand.remove(card)

            if printing: print(f'  updated hand: {hand}')

            # UPDATE turn history
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
            if (play_type in [3, 4, 5] and not hand) or (30 in turn_count) or (self_play and not deck):

                # UPDATE turn count
                for i in range(NUM_PLAYERS):
                    if not hands[i]:
                        if printing_yes: print(f'Player {i} had no cards left in their hand. {total_scores[i]} + 0 = {total_scores[i]}')
                    else:
                        score = phazed_score(hands[i])
                        round_scores[i] = score
                        if printing_yes: print(f'Player {i} had {hands[i]} left in their hand. {total_scores[i]} + {score} = {total_scores[i]+score}.')
                        total_scores[i] += score
                # print(f'phase_status: {phase_status}')
                if 7 in phase_status:
                    winner_i = ''
                    # find winner
                    for i in range(NUM_PLAYERS):
                        status = phase_status[i]
                        if status == 7:
                            if winner_i == '':
                                winner_i = i
                            
                            # tie break with score
                            elif total_scores[i] < total_scores[winner_i]:
                                winner_i = i
                            
                            # tie break with turn
                            elif total_scores[i] == total_scores[winner_i]:
                                if turn_count[i] < turn_count[winner_i]:
                                    winner_i = i
                    # create placing
                    placing = []  # 1st, 2nd, 3rd, 4th
                    placing.append(winner_i)
                    
                    total_scores_copy = total_scores[:]
                    total_scores_copy[winner_i] = 999  # change winner score to large val
                    sorted_total_scores_copy = sorted(total_scores_copy)
                    for i in range(NUM_PLAYERS-1):
                        placing.append(total_scores.index(sorted_total_scores_copy[i]))
                    
                    PLACING_DATA.append(placing)
                    print(f'🥳 Player {phase_status.index(NUM_PHASES)} has won')
                    round_flag = False
                    
                turn_flag = False

            # UPDATE discard
            if play_type == 5:
                discard = card
                # UPDATE turn count
                turn_count[player_id] += 1
                if printing: print(f'    {player_id}')
                if printing: print(f'    {table}')
                if printing: print(f'    {turn_history}')
                if printing: print(f'    {phase_status}')
                if printing: print(f'    {discard}')

                # NEXT PLAYER'S TURN
                player_id = player_id + 1 if player_id in [i for i in 
                                                range(NUM_PLAYERS-1)] else 0
                
                if printing_yes: print(f"\n--- Player {player_id}'s {turn_count[player_id]} turn ---")

                # Human support
                #turn_flag = True if input(f'➡️ Next Player Turn? ') == '' \
                #    else False
        if display_data:
            print(f'\n📈 Hand number {hand_num} stats 📈')
            head = ["#", "Name", "Phase #", "Turn Count", "Score", "Round Score"]
            players = []
            for i in range(NUM_PLAYERS):
                # update round and score data
                data = PHASE_DATA[i][1+phase_status[i]]
                if type(data) == int:
                    PHASE_DATA[i][2+phase_status[i]][ROUND] += 1
                    PHASE_DATA[i][2+phase_status[i]][SCORE] += round_scores[i]
                else:
                    data[ROUND] += 1
                    data[SCORE] += round_scores[i]

                cell = []
                cell.append(i)
                cell.append('Human' if PLAYER[i] == 'h' else 'Bot '+PLAYER[i])
                cell.append(phase_status[i])
                cell.append(turn_count[i])
                cell.append(total_scores[i])
                cell.append(round_scores[i])
                players.append(cell)
            
            data = [player_names, game_number, hand_num, phase_status, turn_count, total_scores]
            GAME_DATA.append(data)
            

            print(tabulate(players, headers=head, tablefmt="grid"))
        # A player has completed all phases - end game
        if 7 in phase_status:
            return None
        

        # NEXT ROUND?
        # round_flag = True if input(f'➡️ Continue to Next Round? [Y/N]: ') in ['Y', 'y'] \
        #     else False
        
        # UPDATE hand number
        hand_num += 1
    
    # END OF ROUND
    if printing_yes: print('\n=== GAME DATA ===')
    if printing_yes: print(f'gamedata: {GAME_DATA}')
    if printing_yes: print(f'phasedata: {PHASE_DATA}')
    # print(f'difference: {DIFFERENCE_DATA}')
    if printing_yes: print(f'errors: {ERROR_DATA}')
    record_data = False
    #record_data = True if input(f'➡️ Record game data? [Y/N]: ') in ['Y', 'y'] else False
    if record_data:
        # GAME DATA
        with open('data_games.csv', 'a', newline='') as fp:
            data_writer = csv.writer(fp)
            data_writer.writerows(GAME_DATA)

        # LINK DATA
        with open('data_links.csv', 'a', newline='') as fp:
            data_writer = csv.writer(fp)
            game_link = ['self-play' if self_play else input('➡️ Enter game link: ')]
            if error_flag or not placing:
                placing = []
                for i in range(NUM_PLAYERS):
                    if i == error_flag:
                        placing.append('ERROR')
                    else:
                        placing.append('-')
                data = [game_number] + player_names + placing + game_link
            else:
                data = [game_number] + player_names + placing + game_link
            data_writer.writerow(data)

        # PHASE DATA
        phase_data = []
        for i in range(NUM_PLAYERS):
            player_data = []
            row = PHASE_DATA[i]
            for data in row:
                if type(data) == list:
                    player_data.append(data[0])
                    player_data.append(data[1])
                else:
                    player_data.append(data)
            phase_data.append(player_data)
        if printing_yes: print(phase_data)
        with open('data_phase.csv', 'a', newline='') as fp:
        
            data_writer = csv.writer(fp)
            data_writer.writerows(phase_data)

        # # DIFFERENCE DATA
        # if DIFFERENCE_DATA:
        #     with open('data_difference.csv', 'a', newline='') as fp:
        #         data_writer = csv.writer(fp)
        #         data_writer.writerows(DIFFERENCE_DATA)

        # ERROR DATA
        if ERROR_DATA:
            with open('data_difference.csv', 'a', newline='') as fp:
                data_writer = csv.writer(fp)
                data_writer.writerows(ERROR_DATA)



ERROR_DATA = []
PLACING_DATA = []
PHASE_DATA = []

display_data = True

total_games = int(input(f'NUMBER OF GAMES TO PLAY: '))

# INPUT self play or no
# self_play = True
self_play = True if input(f'➡️ Self Play? [Y/N]: ') in ['Y', 'y'] else False

# CHOOSE players
PLAYER = []
for i in range(NUM_PLAYERS):
    p = ''
    while p not in list(BOTS.keys())+['h']:
        p = input(f'➡️ Choose Player {i} [h/46/47/48/49]: ')
    PLAYER.append(p)
# beginning = True
beginning = True if input(f'➡️ Start from beginning?') in ['Y', 'y'] else False

# DISPLAY players
head = ["Player #", "Name"]
players = []
player_names = []
# Generate table
for i in range(NUM_PLAYERS):
    player_names.append('Bot '+ PLAYER[i] if PLAYER[i].isdigit() else input(f'➡️ Enter Human Name: '))
    cell = (['Player' + str(i), 'Human' if PLAYER[i] == 'h' else 'Bot '+ PLAYER[i]])
    players.append(cell)
# print(f'=== Players ===')
# print(tabulate(players, headers=head, tablefmt="grid"))

for name in player_names:
    player_data = [name, 1] + [[0, 0] for i in range(NUM_PHASES)]
    PHASE_DATA.append(player_data)

for i in range(total_games):
    printing_yes = False
    program_flag = True
    # program_flag = True if input(f'➡️ Play again?') in ["Y", "y"]else False
    if program_flag:
        game(PLAYER, self_play, beginning, player_names, i)

winning_list = [0, 0, 0, 0]

print(f'================== ERROR DATA =======================')
for error in ERROR_DATA:
    print(f'-- {error}')
print(f'================== PHASE DATA =======================')
for data in PHASE_DATA:
    print(f'-- {data}')
print(f'================== PLACING DATA =======================')
for data in PLACING_DATA:
    winning_list[data.index(0)] += 1
    print(f'-- {data}')
print(f'================== WINNDER DATA =======================')
for i in range(NUM_PLAYERS):
    print(f'{player_names[i]} won {winning_list[i]} times.')