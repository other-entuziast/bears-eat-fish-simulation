
import simulation_functions as sf
import results


def main():
    '''Simulates river with two types of animals: bear and fish.

    RULES:
    Each time period (year) every animal either moves into adjacent cell or stays in his cell, 
    movement assigned by random process. If the bear encounters fish, fish always dies. 
    If two animals of the same type encounter each other, they, in case they are of different genders, 
    produce a new animal of their kind. If two animals of the same gender meet, 
    the stronger one wins.
    '''

    # Set length of the river and number of years the simulation is to run.
    LENGTH = 5000
    YEARS = 10

    river = sf.populate_river(LENGTH)
    empty_space = sf.find_empty(river)

    all_fish = []
    all_bears = []

    # count initial number of fish and bears and add to lists
    all_fish.append(sf.total_fish(river))
    all_bears.append(sf.total_bear(river))

    # run simulation for every animal in the river, sequentially
    bear_count, fish_count = sf.run_simulation(river, empty_space, YEARS)
    all_fish += fish_count
    all_bears += bear_count

    # display results
    results.print_results(all_bears, all_fish, YEARS)
    results.chart(YEARS, all_bears, all_fish)


main()
