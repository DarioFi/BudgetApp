from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from games.database.models import GameRoom


# Create your views here.


# todo: write views in order to have slug valdiation and joining/creation system

@login_required
def open_room(request, room_id=-1):
    if request.method != "GET":
        return HttpResponse("Ricchione sarebbe gradito tu facessi richieste per bene")

    try:  # using try because of future slug change
        room: GameRoom = GameRoom.objects.get(id=room_id)
    except Exception as e:
        print("Get exception at open_room")
        print(e)
        return HttpResponse("Usa un url buono per l'amor del cielo")

    room.players.add(request.user)  # this automatically checks if it already exist because of m2m unique property

    data = {
        "room": room,
        "players": [x for x in room.player_room_related.all()],
        "self_player": room.player_room_related.get(player_id=request.user.id)
    }

    return render(request, 'games_templates/room_view.html', data)
