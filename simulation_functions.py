import animal
import random


def populate_river(n):
    '''Randomly populate river of size n with two animals and empty spaces.'''
    river = []
    for _ in range(1, n + 1):
        occupant = random.choice(
            [None, animal.Animal('bear'), animal.Animal('fish')])
        river.append(occupant)
    return river


def populate_moves(length, choice_ofmoves):
    '''Create a list of randomly selected moves for each animal.'''
    moves = []
    for _ in range(length):
        moves.append(random.choice(choice_ofmoves))
    return moves


def find_empty(some_list):
    '''Finds index of all None cells in the given list and saves them in a separate list.'''
    empty = []
    for i in range(len(some_list)):
        if some_list[i] == None:
            empty.append(i)
    return empty


def total_fish(river):
    '''Count number of fish in a list.'''
    fish = 0
    for anim in river:
        if anim:
            if anim.animal == 'fish':
                fish += 1
    return fish


def total_bear(river):
    '''Count number of bears in a list.'''
    bears = 0
    for anim in river:
        if anim:
            if anim.animal == 'bear':
                bears += 1
    return bears


def bear_stays_fish_moves(river, available, moves):
    '''If bear stays in its cell and fish moves into bear's cell, 
    then fish is eaten and bear stays put.'''
    river[moves] = None
    # Update the list of None cells.
    available.append(moves)


def fish_stays_bear_moves(river, available, stays, moves):
    '''If fish stays in its cell and bear moves into fish's cell, 
        then fish is eaten and bear moves into fish's cell.
    '''
    # The fish is eaten and bear moves one cell.
    river[stays] = river[moves]
    river[moves] = None
    # Update the list of None cells.
    available.append(moves)


def male_female(river, available, stays):
    '''If animals are of the same kind and one is male and other is female,
    they produce a baby animal of their kind.'''
    baby_cell = random.choice(available)
    # Create baby animal and place in random None cell.
    river[baby_cell] = animal.Animal(river[stays].animal)

    # Update the list of None cells.
    available.remove(baby_cell)


def stronger_wins(river, available, weak):
    '''If animals are of the same kind and gender, then the stronger one survives.
        weak = index of the weaker animal
    '''
    river[weak] = None
    available.append(weak)


def same_type(river, available, stays, moves):
    '''Models interaction of animals of the same kind.'''
    # Animals are of different genders.
    if river[stays].gender != river[moves].gender:
        # There is still space in the empty list.
        if available:
            male_female(river, available, stays)
    # Animals are of same gender.
    else:
        if river[stays].strength > river[moves].strength:
            stronger_wins(river, available, moves)
        elif river[stays].strength < river[moves].strength:
            stronger_wins(river, available, stays)


def encounter(river, available, stays, moves):
    '''Simulates what happens when one animal stays in his cell and the other attempts 
        to move into it.
        river = randomly populated list of animals and None entries
        available = list of None cells
        stays = index of the animal that stays
        moves = index of the animal that moves
    '''
    # Bear stays and fish moves.
    if river[stays].animal == 'bear' and river[moves].animal == 'fish':
        bear_stays_fish_moves(river, available, moves)

    # Fish stays and bear moves.
    elif river[stays].animal == 'fish' and river[moves].animal == 'bear':
        fish_stays_bear_moves(river, available, stays, moves)

    # Animals are of the same type.
    elif river[stays].animal == river[moves].animal:
        same_type(river, available, stays, moves)

    return river, available


def move_forward(river, available, current):
    # There is an animal in the next cell.
    if river[current + 1]:
        river, available = encounter(
            river, available, (current + 1), current)
    # There is None in the next cell.
    else:
        # Current animal just moves into the next cell
        # and the current cell becomes None.
        river[current + 1] = river[current]
        river[current] = None
        # Update the list of empty cells.
        available.remove(current + 1)
        available.append(current)


def move_backward(river, available, current):
    # There is an animal in the previous cell.
    if river[current - 1]:
        river, available = encounter(
            river, available, (current - 1), current)
    # There is None in the next cell.
    else:
        # Current animal just moves into the previou cell and
        # the current cell becomes None
        river[current - 1] = river[current]
        river[current] = None
        # update the list of empty cells
        available.remove(current - 1)
        available.append(current)


def simulation(river, available, current, moves):
    ''' Simulates sequential movement of animals in the river, i.e. only the current animal's
    moves are considered, all other animals are held constant.
    river = randomly populated list of animals and None entries
    available = list of None cells
    current = index of the current animal
    moves = list of randomly generated moves for each animal, can be (-1, 0, 1)
    '''

    # THERE IS SOME ANIMAL IN THE CELL
    if river[current]:
        if moves[current] == 0:  # Animal does not move.
            pass
        # Animal moves one cell forward and is not last in the list.
        elif moves[current] == 1 and current < (len(river) - 1):
            move_forward(river, available, current)

        # Animal moves one cell backward and is not first in the list.
        elif moves[current] == -1 and current >= 1:
            move_backward(river, available, current)

    # THERE IS NO ANIMAL IN THE CURRENT CELL (NONE cell)
    else:
        pass

    return river, available


def run_simulation(habitat, available, years):
    '''Runs simulation for the given habitat during specified number of periods.'''

    bear_count = []
    fish_count = []
    for year in range(1, years + 1):
        # Generate a list of randomly selected moves for each animal.
        moves = populate_moves(len(habitat), [-1, 0, 1])
        for num in range(len(habitat)):
            habitat_1, available_1 = simulation(
                habitat, available, num, moves)

        bear_count.append(total_bear(habitat_1))
        fish_count.append(total_fish(habitat_1))
    return bear_count, fish_count
