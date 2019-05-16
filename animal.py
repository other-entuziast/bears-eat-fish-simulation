import random


class Animal():

    def __init__(self, animal):
        self.animal = animal
        self.gender = random.choice('MF')
        self.strength = random.random()

    def __str__(self):
        return self.animal


if __name__ == '__main__':
    bear = Animal('bear')
    print(bear)
    print(bear.__dict__)
    print('bear strength:', bear.strength)
    print('bear is: ', bear.gender)

    print()
    fish = Animal('fish')
    print(fish)
    print(fish.__dict__)
    print('fish strength:', fish.strength)
    print('fish is: ', fish.gender)
