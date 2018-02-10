from random import choice


class diceManager:

    def __init__(self):
        self.red = ['f', 'f', 'c', 'c', 'h', 'h', 'b', 'b']
        self.green = ['f', 'f', 'b', 'b', 'b', 'e', 'e', 'e']

    def rollRed(self, numDice):
        return [choice(self.red) for i in range(0, numDice)]

    def rollGreen(self, numDice):
        return [choice(self.green) for i in range(0, numDice)]
