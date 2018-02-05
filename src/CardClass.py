class Card:
    """
    Klasa kart w talii
    """
    def __init__(self, value, color, url=''):
        self.value = value
        self.color = color
        self.url = url
        self.useful = False

    def __repr__(self):
        """
        :return: nazwa grafiki bez rozszeżenia .png lub .jpg
        """
        return '%s' % (self.url[:3])


_9s = Card(9, 's', '9s.png')
_9d = Card(9, 'd', '9d.png')
_9z = Card(9, 'z', '9z.png')
_9w = Card(9, 'w', '9w.png')
_10s = Card(10, 's', '10s.png')
_10d = Card(10, 'd', '10d.png')
_10z = Card(10, 'z', '10z.png')
_10w = Card(10, 'w', '10w.png')
_Js = Card(11, 's', 'Js.png')
_Jd = Card(11, 'd', 'Jd.png')
_Jz = Card(11, 'z', 'Jz.png')
_Jw = Card(11, 'w', 'Jw.png')
_Ds = Card(12, 's', 'Ds.png')
_Dd = Card(12, 'd', 'Dd.png')
_Dz = Card(12, 'z', 'Dz.png')
_Dw = Card(12, 'w', 'Dw.png')
_Ks = Card(13, 's', 'Ks.png')
_Kd = Card(13, 'd', 'Kd.png')
_Kz = Card(13, 'z', 'Kz.png')
_Kw = Card(13, 'w', 'Kw.png')
_As = Card(14, 's', 'As.png')
_Ad = Card(14, 'd', 'Ad.png')
_Az = Card(14, 'z', 'Az.png')
_Aw = Card(14, 'w', 'Aw.png')


def restart_cards():
    """
    ustawia listę kard do rozdawania na początku gry
    :return:
    """
    global all_cards
    all_cards = [_9s, _9d, _9z, _9w, _10s, _10d, _10z, _10w, _Js, _Jd, _Jz, _Jw, _Ds, _Dd, _Dz, _Dw, _Ks, _Kd, _Kz, _Kw,
                 _As, _Ad, _Az, _Aw, ]

all_cards =[]
restart_cards()


def add_to_stack(cards):
    """
    dodawanie do stosu listy kart
    :param cards:
    :return:
    """
    global stack
    for card in cards:
        stack.append(card)

stack = []
