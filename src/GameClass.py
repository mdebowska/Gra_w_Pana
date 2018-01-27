from src import CardClass
class Game:


    def __init__(self):
        self.stack = []
        self.players = []
        self.restart()

    def __repr__(self):
        """
        Wyświetla karty ze stosu
        :return:
        """
        return 'gra0: '+','.join( [card.__repr__() for card in self.stack] )



    def restart(self):
        self.players = []
        CardClass.restart_cards()

    def add_to_stack(self, cards, player):
        """
        Połóż karty na stos i odejmij z ręki gracza
        :return:
        """
        print('Hand: ', player.hand)
        for card in cards:
            print('card: ', card)
            self.stack.append(card)
            player.hand.remove(card)
            player.layed_card.append(card)


    def take_from_stack(self, number_of_cards, player):
        """
        Zabierz karty ze stosu i daj je graczowi
        :return:
        """
        print(number_of_cards)
        print(self.stack[len(self.stack)-1])

        for i in range(number_of_cards):
            if len(self.stack) == 1:
                break
            card = self.stack[len(self.stack)-1]
            player.hand.append(card)
            self.stack.remove(card)



    def add_player(self, player):
        """
        Dodaj gracza do gry
        :return:
        """
        self.players.append(player)

    def add_players(self, players):
        """
        Dodaj graczy z listy (players) do gry (do self.players)
        :return:
        """
        for player in players:
            self.players.append(player)

    def take_cards_start(self):
        if self.players:
            for player in self.players:
                for i in range(1, int((24/len(self.players))+1)):
                    player.take_card()


    def find_active_player(self):
        """
        Znajduje aktywnego gracza
        :return: object type Person
        """
        for player in self.players:
            if player.active == 1:
                return player

    def swich_active_person(self, next_label = 0):
        """
        Zmień aktywnego gracza na kolejnego lub poprzedniego
        :return:
        """

        current_active = self.find_active_player()
        current_active.active = 0

        if next_label:  #jeśli ostatnie było "zakończ" (tzn poprzedni gacz rzucił karty na stos) to sprawdź czy to było wino
            if self.stack[len(self.stack)-1].color != 'w':
                id_next_active = (self.players.index(current_active)+1)%len(self.players)   #bierze indeks kolejnego gracza
                self.players[id_next_active].active = 1
            else:
                id_prev_active = (self.players.index(current_active)-1)%len(self.players)   #bierze indeks poprzedniego gracza
                self.players[id_prev_active].active = 1
        else:
            id_next_active = (self.players.index(current_active) + 1) % len(self.players)  # bierze indeks kolejnego gracza
            self.players[id_next_active].active = 1


    def check_if_good_to_add(self, cards):
        """
        Funkcja sprawdza, czy wybrane karty nadają się do zagrania
        :return bool
        """

        if len(cards) != 1 and len(cards) != 3 and len(cards) != 4: #bierzemy pod uwagę zagranie tylko 1, 3 lub 4 kartami
            # print('nie jest 1 ani 3 ani 4', len(cards))
            return False

        elif len(cards) == 3 or len(cards) == 4: # jeśli więcej niż 1, to sprawdź czy mają tę samą wartość
            for i in range(len(cards)-1):
                if cards[i].value != cards[i+1].value:
                    # print('nie jest takie samo')
                    return False

        if cards[0].value < self.stack[len(self.stack)-1].value:    # sprawdź, czy karta nie jest słabsza niż ostatnia na stosie
            # print('Nie jest rowna lub większa')
            return False

        return True



    def find_player_with_9s(self):
        """
        Funkcja znajdująca rozpoczynającego gracza
        :return: player
        """
        for player in self.players:
            for card in player.hand:
                if card.value == 9 and card.color == 's':
                    return player