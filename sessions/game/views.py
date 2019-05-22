from django.shortcuts import render
from .models import Player, Game, PlayerGameInfo
from .forms import AnswerForm

import random


def show_home(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)

        if request.session.get('player_game_info'):

            if form.is_valid():
                answer = form.cleaned_data['answer']
                player_game_info = PlayerGameInfo.objects.get(id=request.session['player_game_info'])
                value = player_game_info.game.value
                player_game_info.counter += 1
                player_game_info.save()

                if value < answer:
                    message = f'Загаданное число меньше {answer}'

                elif value > answer:
                    message = f'Загаданное число больше {answer}'

                else:
                    # Удаляем информацию об игре из кук и еще как-то нужно предать сообщение ведущему.
                    message = f'Вы угадали с {player_game_info.counter} попыток'
                    player_game_info.game.game_over = True
                    player_game_info.game.save()
                    del request.session['player_game_info']
                    form = AnswerForm()

                return render(
                    request,
                    'home.html',
                    {'player_game_info': player_game_info,
                     'form': form,
                     'message': message}
                )

    form = AnswerForm()
    # создаю нового игрока при входе в браузер записываю его в сессию
    if not request.session.get('player', None):
        player = Player.objects.create()
        request.session['player'] = player.id

    # если нет игры в сессии
    if not request.session.get('game', None):
        games_list = list(Game.objects.all())

        # еcли игры созданы, берем последнюю
        if games_list:
            last_game = games_list[-1]

            # если последняя игра завершена, создаем новую
            if last_game.game_over:
                player_id = request.session['player']
                context = create_game(player_id, request)
                request.session['player_game_info'] = context['player_game_info'].id
                request.session['status'] = 'creator'

                return render(
                    request,
                    'home.html',
                    context
                )

            # если последняя игра не завершена добавляем в игру игрока
            else:
                player_game_info = list(PlayerGameInfo.objects.all())[-1]
                request.session['player_game_info'] = player_game_info.id
                player_id = request.session['player']
                player = Player.objects.get(id=player_id)

                if not player_game_info.player:
                    player_game_info.player = player
                    player_game_info.save()
                    request.session['status'] = 'player'

                context = {'player_game_info': player_game_info,
                           'form': form}

                return render(
                    request,
                    'home.html',
                    context
                )

        # если список пуст создаем новую игру
        else:
            player_id = request.session['player']
            request.session['status'] = 'creator'
            context = create_game(player_id, request)
            return render(
                request,
                'home.html',
                context
            )

    # делаем контекст для разных пользователей, если он обновил страницу
    if request.session.get('player_game_info'):
        player_game_info_id = request.session['player_game_info']
        player_game_info = PlayerGameInfo.objects.get(id=player_game_info_id)

        if player_game_info.game.game_over:
            del request.session['player_game_info']
            del request.session['game']

        return render(
            request,
            'home.html',
            {'player_game_info': player_game_info,
             'form': form}
        )

    return render(
        request,
        'home.html',
        {'form': form}
    )


def create_game(player_id, request):
    player = Player.objects.get(id=player_id)

    game = Game(value=random.randint(1, 10))
    game.save()

    player_game_info = PlayerGameInfo(creator=player, game=game)
    player_game_info.save()

    request.session['player_game_info'] = player_game_info.id
    request.session['game'] = game.id
    context = {'player_game_info': player_game_info}

    return context
