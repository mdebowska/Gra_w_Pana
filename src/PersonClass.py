import random
from src import CardClass
from src import GameClass

names = ['Ada', 'Justyna', 'Gosia', 'Maciej', 'Wiesław', 'Krysia', 'Marian', 'John', 'Jane']

class Person:
    def say_hello(self):
        print('I say hello!')

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.active = 0
        self.layed_card = []
        # add_player(self)

    def __repr__(self):
        return self.name

    def say_about_yourself(self):
        return 'Jestem %s, a w ręce trzymam %d kart. Są to: ' % (self.name, len(self.hand))#, str(self.hand))


    def take_card(self):
        card = random.choice(CardClass.all_cards)
        CardClass.all_cards.remove(card)
        self.hand.append(card)

    def check_if_winner(self):
        if len(self.hand) == 0:
            return True