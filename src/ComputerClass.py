from src import PersonClass

class Computer(PersonClass.Person):
    """
    Klasa gracza-komputera
    """
    def __repr__(self):
        return 'Komputer %s' % self.name

    def sort_hand(self):
        """
        Poukładaj po kolei karty w ręce
        :return:
        """
        self.hand = sorted(self.hand, key=lambda item: item.value)

    def choose_cards_to_lay(self, game):
        """
        Wybiera karty najlepsze do zagrania
        :return: najmniejszą kartę możliwą do zagrania lub -1 jeśli takiej nie ma
        """
        for id in range(len(self.hand)):
            if self.hand[id].value >= game.stack[len(game.stack)-1].value:
                print('value;', self.hand[id].value)
                return [id]

        return -1
    
    #
    # def choose_cards_to_lay(self, game):
    #     """
    #     Wybiera karty najlepsze do zagrania
    #     :return: najmniejszą kartę możliwą do zagrania lub -1 jeśli takiej nie ma
    #     """
    #     cards_id=[]
    #     for id in range(len(self.hand)):
    #         if self.hand[id].value >= game.stack[len(game.stack)-1].value:
    #             print('value;', self.hand[id].value)
    #             if cards_id != []:
    #                 if self.hand[id].value == cards_id[0]:
    #                     cards_id.append(id)
    #             else:
    #                 cards_id.append(id)
    #     return cards_id
    #     # return -1