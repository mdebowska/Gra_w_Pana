﻿from flask import render_template, request, redirect, url_for, session
from src import app
from src import PersonClass
from src import ComputerClass
from src import CardClass
from src import GameClass
import random



#secret_key for session



@app.route('/')
def index():
    """
    Index page
    :return:
    """
    session.clear()
    return render_template('index.html')



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

    # if request.form.get('card'):
    #     session['card'] = request.form.get('card')
    #     print(session)
    #
    #     game.stack.append(session['card'])
    #     return redirect(url_for('game_human'), code=302)




    #początek gry - resetowanie ustawień: ustawienie tablicy do losowania kart
# ja = PersonClass.Person('Gosia')
# computer = PersonClass.Person('Komputer')
    # ja.take_cards_start()
    # computer.take_cards_start()


#players = [ja, computer] #game.players
#game.add_players(players)


    #----------------

    # game.add_to_stack(ja.hand, ja)
    global game
    game = GameClass.Game()
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


@app.route('/game/human', methods=['GET','POST'])
def play_human():
    """
    Human turn page
    :return:
    """

    active_player = game.find_active_player()

    if game.stack == []:
        game.add_to_stack([CardClass._9s], active_player)
        if active_player.layed_card:
            next_label = 1
            print("położyłem kartę, patrz: ", active_player.layed_card)
        else:
            print("nic nie dałem")
    else:
        next_label = 0 #nie wiadomo, czy ktoś rzucił już kartami, więc domyślnie jest 0


    if request.form.getlist('card'):    #jeśli pobrano listę kart do zagrania to:
        cards = []

        for id in request.form.getlist('card'):
            cards.append(active_player.hand[int(id)])
        print('Cards: ', cards)

        check_cards = []
        check_cards.extend(cards)
        check_cards.extend(active_player.layed_card)
        print('Sprawdź te karty:', check_cards)
        if game.check_if_good_to_add(check_cards):
            game.add_to_stack(cards, active_player)
        else:
            print('NIE ZGADZAM SIĘ!')

    if active_player.layed_card != []:
        next_label = 1  # informacja, że karty zostały rzucone => można wyświetlić przycisk "zakończ"


    return render_template('game.html', players=game.players, a_player = active_player, stack = game.stack, next_label = next_label)

@app.route('/game/human/next', methods=['GET','POST'])
def play_human_next():
    """
    Human turn page
    :return:
    """

    active_player = game.find_active_player()

    if active_player.check_if_winner():
        return redirect(url_for('end'))

    active_player.layed_card = []
    game.swich_active_person(1)

    return redirect(url_for('play_human'))


@app.route('/game/take', methods=['GET','POST'])
def play_take_from_stack():
    """
    Human turn page
    :return:
    """

    if request.form.get('from_stack'):
        game.take_from_stack(int(request.form.get('from_stack')), game.find_active_player())
        game.swich_active_person()
    else:
        print('coś poszło nie tak')


    return redirect(url_for('play_human'))

@app.route('/game/end')
def end():

    return render_template('end.html', winner = game.find_active_player())