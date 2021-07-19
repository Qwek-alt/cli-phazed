from group_type import phazed_group_type

printing = False  # for debugging

def phazed_phase_type(phase):
    '''Given a list of card groups, `phase`, return a sorted list of integers 
    indicating card group combination types.'''
    result_list = []
    group_list =[]
    
    # find the card combination type of each group and add to `group_list`
    for group in phase:
        if printing: print(f'group: {group}')
        group_list.append(phazed_group_type(group))
    if printing: print(f' grouplist: {group_list}')

    # phases with 2 groups
    if len(group_list) == 2:
        group_1 = group_list[0]
        group_2 = group_list[1]

        # [phase 1] two sets of three cards of the same value [[1], [1]]
        if 1 in group_1 and 1 in group_2:
            result_list.append(1)

        # [phase 3] two 34-accumulations [[6], [6]]
        if 6 in group_1 and 6 in group_2:
            result_list.append(3)

        # [phase 4] two sets of four cards of the same value [[3], [3]]
        if 3 in group_1 and 3 in group_2:
            result_list.append(4)

        # [phase 6] two 34-accumulations of the same colour [[7], [7]]
        if 7 in group_1 and 7 in group_2:
            result_list.append(6)

        # [phase 7] one run of four cards of the same colour + a set of four 
        # cards of the same value [[5], [3]]
        if 5 in group_1 and 3 in group_2:
            result_list.append(7)

    # phases with 1 group
    elif len(group_list) == 1:
        group_1 = group_list[0]

        # [phase 2] one set of 7 cards of the same suit [[2]]
        if 2 in group_1:
            result_list.append(2)

        # [phase 5] one run of eight cards [[4]]
        if 4 in group_1:
            result_list.append(5)

    return sorted(result_list)