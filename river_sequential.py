import random
import animal
import matplotlib.pyplot as plt


def main():
    '''simulates habitat with two types of animals: bear and fish
    habitat = list populated randomly with either an animal object or None

    RULES:
    Every animal either moves into adjacent cell or stays in his cell, movement assigned 
    by random process. If the bear encounters fish, fish always dies. If two animals of the
    same type encounter each other, they, in case they are of different genders, 
    produce a new animal of their kind. If two animals of the same gender meet, 
    the stronger one wins.
    '''
    LENGTH = 2000  # length of river
    YEARS = 10  # number of years (periods) the simulation is to run

    # create and populate the river
    habitat = populate_river(LENGTH)

    all_fish = []
    all_bears = []
    # count initial number of fish and add to list
    all_fish.append(total_fish(habitat))
    # count initial number of bears and add to list
    all_bears.append(total_bear(habitat))
#     print()
#     print('Our river initially has {} fish and {} bears'.format(
#         all_fish[0], all_bears[0]))

    # create list of all empty cells
    available = find_empty(habitat)

    # run_simulation() for every animal in the river, sequentially
    bear_count, fish_count = run_simulation(habitat, available, YEARS)
    all_fish += fish_count
    all_bears += bear_count
    print('fish, years 0 through end', all_fish)
    print('bears, years 0 through end', all_bears)
    print()
    print_results(all_bears, all_fish, YEARS)
    chart(YEARS, all_bears, all_fish)


def chart(periods, bears, fish):

    # create plot

    index = list(range(periods + 1))
    bar_width = 0.47
    opacity = 0.8

    rects1 = plt.bar([t for t in range(periods + 1)], fish, bar_width,
                     alpha=opacity,
                     color=(0.3, 0.1, 0.4, 0.6),
                     label='fish')

    rects2 = plt.bar([t + bar_width for t in range(periods + 1)], bears, bar_width,
                     alpha=opacity,
                     color=(0.3, 0.5, 0.5, 0.6),
                     label='bear')

    plt.xlabel('Years')
    plt.ylabel('Total population')
    plt.title('Habitat with two animals')
    plt.xticks([t + bar_width / 2 for t in range(periods + 1)], index)
    plt.legend()

    plt.tight_layout()
    plt.show()


def run_simulation(habitat, available, years):
    '''runs simulation for the given habitat during specified number of periods'''

    bear_count = []
    fish_count = []
    for year in range(1, years + 1):
        # generate list of randomly selected moves for each animal in the river
        new_moves = populate_moves(len(habitat), [-1, 0, 1])
        for num in range(len(habitat)):
            habitat_1, available_1 = simulation(
                habitat, available, num, new_moves)

        bear_count.append(total_bear(habitat_1))
        fish_count.append(total_fish(habitat_1))

        print('Our river has {} fish and {} bears at the end of period {}'.format(
            fish_count[year - 1], bear_count[year - 1], year))

    return bear_count, fish_count


def print_results(bear_count, fish_count, years):
    print('Simulation results:')
    print('{:^8} {:^8} {:^8} {:^8} {:^8}'.format(
        'period', 'bears', 'diff', 'fish', 'diff'))
    print('{:-^8} {:-^8} {:-^8} {:-^8} {:-^8}'.format('', '', '', '', ''))

    # print the initial population of the river (year 0)
    print('{:^8} {:^8} {:^8} {:^8} {:^8}'.format(
        0, bear_count[0], '', fish_count[0], ''))
    # print population in the rest of the years (1 through end)
    for t in range(1, years + 1):
        print('{:^8} {:^8} {:^8} {:^8} {:^8}'.format(
            t, bear_count[t], bear_count[t] - bear_count[t - 1],
            fish_count[t], fish_count[t] - fish_count[t - 1]))


def populate_river(n):  # populate river of size n via function

    river = []
    for _ in range(1, n + 1):
        beast = random.choice(
            [None, animal.Animal('bear'), animal.Animal('fish')])
        river.append(beast)

    return river


def total_fish(water):
    '''count initial number of fish in a list (water)'''
    fish = 0
    for anim in water:
        if anim:
            if anim.animal == 'fish':
                fish += 1
    return fish


def total_bear(water):
    '''counts initial number of bears in a list (water)'''
    bears = 0
    for anim in water:
        if anim:
            if anim.animal == 'bear':
                bears += 1
    return bears


def find_empty(some_list):
    '''finds index of all None cells in the given list and saves them in a separate list'''
    empty = []
    for i in range(len(some_list)):
        if some_list[i] == None:
            empty.append(i)

    return empty


def populate_moves(length, choice_ofmoves):
    '''creates list of randomly selected moves for each animal'''
    moves = []
    for _ in range(length):
        moves.append(random.choice(choice_ofmoves))

    return moves


def encounter(river, available, stays, moves):
    '''simulates what happens when one animal stays in his cell and the other attempts 
        to move into it
        river = randomly populated list of animals and None entries
        available = list of None cells
        stays = index of the animal that stays
        moves = index of the animal that moves
    '''

    # bear stays and fish moves -->
    if river[stays].animal == 'bear' and river[moves].animal == 'fish':
        river[moves] = None
        # the fish is eaten and bear stays put
        print('one fish has been eaten')

        # update the available list (indexes of None cells)
        available.append(moves)
    # fish stays and bear moves -->
    elif river[stays].animal == 'fish' and river[moves].animal == 'bear':
        river[stays] = river[moves]
        # the fish is eaten and bear moves one cell
        river[moves] = None
        print('one fish has been eaten and bear moved')
        # update the available list (indexes of None cells)
        available.append(moves)
    # animals are of the same kind -->
    elif river[stays].animal == river[moves].animal:
        # if one is male and the other is female (not of the same gender)
        if river[stays].gender != river[moves].gender:
            # there is still space in the empty list
            if available:
                baby_cell = random.choice(available)
                # create new animal and place in random None cell
                river[baby_cell] = animal.Animal(river[stays].animal)
                # update the available list (indexes of None cells)
                available.remove(baby_cell)
                print('one new {} created at position {}'.format(
                    river[stays], baby_cell))

            else:
                print('no more space for babies')
        # both animals are of the same gender
        else:
            # the stronger one survives
            if river[stays].strength > river[moves].strength:
                print('{} lost and died'.format(river[moves]))
                river[moves] = None
                available.append(moves)
            elif river[stays].strength < river[moves].strength:
                print('{} lost and died'.format(river[stays]))
                river[stays] = None
                available.append(stays)

    return river, available


def simulation(river, available, current, moves):
    ''' simulates SEQUENTIAL movement of animals in the river, i.e. only the current animal's
    moves are considered, all other animals are held constant
    river = list of occupants in the habitat (bear, fish, or None)
    available = list of empty (None) cells in the habitat
    current = index of the animal in the current cell
    moves = randomly populated list of moves assigned to each animal in the river'''

    # THERE IS SOME ANIMAL IN THE CELL
    if river[current]:
        # animal does not move -->
        if moves[current] == 0:
            # nothing happens
            pass
        # animal moves one cell forward and is not last in the list-->
        elif moves[current] == 1 and current < (len(river) - 1):
            # and if there some animal in the next cell -->
            if river[current + 1]:
                # call encounter()
                river, available = encounter(
                    river, available, (current + 1), current)
            # and there is None in the next cell -->
            else:
                # current animal just moves into the next cell and
                # the current is None
                river[current + 1] = river[current]
                river[current] = None
                # update the list of empty cells
                available.remove(current + 1)
                available.append(current)

        # animal moves one cell backward and is not first in the list -->
        elif moves[current] == -1 and current >= 1:
            # and there is some animal in the previous cell -->
            if river[current - 1]:
                # call encounter()
                river, available = encounter(
                    river, available, (current - 1), current)
            # and there is None in the next cell -->
            else:
                # current animal just moves into the previou cell and
                # the current is None
                river[current - 1] = river[current]
                river[current] = None
                # update the list of empty cells
                available.remove(current - 1)
                available.append(current)

    # THERE IS NO ANIMAL IN THE CURRENT CELL (NONE cell)
    else:
        pass

    return river, available


main()
