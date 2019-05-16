###############################
# River Simulation ver.2
# Results
# By Iryna Chervachidze
# May 5, 2019
###############################

import matplotlib.pyplot as plt


def print_results(bear_count, fish_count, years):
    ''' Prints results of the simulation in a formatted table.'''
    print('Simulation results:')
    print('{:^8} {:^8} {:^8} {:^8} {:^8}'.format(
        'period', 'bears', 'diff', 'fish', 'diff'))
    print('{:-^8} {:-^8} {:-^8} {:-^8} {:-^8}'.format('', '', '', '', ''))

    # print the initial population of the river_simulation (year 0)
    print('{:^8} {:^8} {:^8} {:^8} {:^8}'.format(
        0, bear_count[0], '', fish_count[0], ''))
    # print population in the rest of the years (1 through end)
    for t in range(1, years + 1):
        print('{:^8} {:^8} {:^8} {:^8} {:^8}'.format(
            t, bear_count[t], bear_count[t] - bear_count[t - 1],
            fish_count[t], fish_count[t] - fish_count[t - 1]))


def chart(periods, bears, fish):
    '''Create a bar chart visualizing results of the simulation.'''

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
