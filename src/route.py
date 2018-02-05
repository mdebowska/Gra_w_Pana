from flask import render_template, request, redirect, url_for, session
from src import app
from src import PersonClass
from src import ComputerClass
from src import CardClass
from src import GameClass
import random
import datetime
from time import gmtime, strftime
import sess

@app.route('/')
def index():
    """
    Index page
    :return:
    """
    session.clear()
    # if game in globals():
    #     bool_game = 1
    # else:
    #     bool_game = 0

    try:
        if game and game.time!= 0:
            game_duration = datetime.datetime.now() - game.time #w przypadku zakończenia gry czas jest ustawiany na 0, więc nawet jeśli tu wejdziemy, to zwrócimy to samo co w wypadku, gdy gry nigdy nie było
            game_duration = str(game_duration)[:7]
        else:
            game_duration = 0
    except NameError:
        game_duration = 0

    return render_template('index.html', game_time = game_duration)



@app.route('/game/settings', methods=['GET','POST'])
def settings():
    """
    Game settings page
    :return:
    """

    if request.form.get('n_people'):
        session['n_people'] = int(request.form['n_people'])
        return render_template('settings.html', n_people=session['n_people'])
    elif request.form.get('computers') and session['n_people']:
        session['computers'] = int(request.form['computers'])

        return redirect(url_for('play'))
    return render_template('settings.html')



@app.route('/game', methods=['GET','POST'])
def play():
    """
    Start game page
    :return:
    """

    
    
    global game
    game = GameClass.Game()
    # game.time = strftime("godziny: %H:%M:%S, dnia: %d.%m.%Y", gmtime())
    game.time = datetime.datetime.now()
    h_players = []
    for x in range(session['n_people']):
        person = PersonClass.Person('Player%d'%(x+1))
        #h_players[x] = person
        h_players.append(person)
    c_players = []
    for x in range(session['computers']):
        computer = ComputerClass.Computer(random.choice(PersonClass.names))
        c_players.append(computer)
    # game.players.extend(h_players)
    # game.players.extend(c_players)
    game.add_players(h_players)
    game.add_players(c_players)
    game.take_cards_start()
    print('game: ', game)

    start_player = game.find_player_with_9s()
    start_player.active = 1

    return render_template('game_start.html', players=game.players)


@app.route('/game/play', methods=['GET','POST'])
def play_game():
    """
    Turn page
    :return:
    """

    active_player = game.find_active_player()

    if game.stack == []:    #sam początek gry
        game.add_to_stack([CardClass._9s], active_player)
        if active_player.layed_card:
            next_label = 1
            # print("położyłem kartę, patrz: ", active_player.layed_card)
        # else:
            # print("nic nie dałem")
    else:
        next_label = 0 #nie wiadomo, czy ktoś rzucił już kartami, więc domyślnie jest 0

    active_player.set_useful_cards(game)
    card_useful_list = active_player.make_useful_list()
    print(card_useful_list)
    if request.form.getlist('card'):    #jeśli pobrano listę kart do zagrania to:
        cards = []

        for id in request.form.getlist('card'):
            cards.append(active_player.hand[int(id)])
        # print('Cards: ', cards)

        check_cards = []
        check_cards.extend(cards)
        check_cards.extend(active_player.layed_card)
        # print('Sprawdź te karty:', check_cards)
        if game.check_if_good_to_add(check_cards):
            game.add_to_stack(cards, active_player)
            return redirect(url_for('play_next'))
        # else:
        #     print('NIE ZGADZAM SIĘ!')

    if active_player.layed_card != []:
        next_label = 1  # informacja, że karty zostały rzucone => można wyświetlić przycisk "zakończ"



    return render_template('game.html', players=game.players, a_player = active_player, stack = game.stack, next_label = next_label, card_useful = card_useful_list)

@app.route('/game/human/next', methods=['GET','POST'])
def play_next():
    """
    Page to change player
    :return:
    """

    active_player = game.find_active_player()

    if active_player.check_if_winner():
        return redirect(url_for('end'))

    active_player.layed_card = []
    game.swich_active_person(1)

    return redirect(url_for('play_game'))

@app.route('/game/play/add', methods=['GET','POST'])
def play_game_add():
    """
    Human turn page after adding card to stack
    :return:
    """
    return redirect(url_for('settings'))

@app.route('/game/take', methods=['GET','POST'])
def play_take_from_stack():
    """
    Page to take cards from stack
    :return:
    """

    if request.form.get('from_stack'):
        game.take_from_stack(int(request.form.get('from_stack')), game.find_active_player())
        game.swich_active_person()
    # else:
        # print('coś poszło nie tak')


    return redirect(url_for('play_game'))

@app.route('/game/last/card', methods=['GET','POST'])
def play_last():
    """
    Page to set last card in hand
    :return:
    """

    if request.form.get('last_card'):
        active_player = game.find_active_player()
        last_card = active_player.hand[int(request.form.get('last_card'))]
        active_player.set_last_card(last_card)

    return redirect(url_for('play_game'))

@app.route('/game/end')
def end():
    game.time = 0
    return render_template('end.html', winner = game.find_active_player())