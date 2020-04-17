from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from .models import match_invitation, match_scopa, games_notification


@login_required
def game_homepage(request):
    stuff = {}

    games_list = match_scopa.objects.filter(
        Q(player1=request.user) | Q(player2=request.user) | Q(player3=request.user) | Q(player4=request.user))

    prelist = []
    for j in games_list:
        if j.players_amount == 2:
            prelist.append([j.id, j.player1.username, j.player2.username])
        if j.players_amount == 3:
            prelist.append([j.id, j.player1.username, j.player2.username, j.player3.username])
        if j.players_amount == 4:
            prelist.append([j.id, j.player1.username, j.player2.username, j.player3.username, j.player4.username])

    stuff['games_list'] = prelist
    return render(request, "game_homepage.html", stuff)


@login_required
def match_view(request, match_id=0):
    if match_id == 0:
        return render(request, "match_error.html", {'error': "Non risultano partite con questo url"})
    mat = match_scopa.objects.filter(id=match_id)

    if len(mat) == 0:
        return render(request, "match_error.html", {'error': "Non risultano partite con questo url"})
    mat = mat.filter(
        Q(player1=request.user) | Q(player2=request.user) | Q(player3=request.user) | Q(player4=request.user))
    if len(mat) == 0:
        return render(request, "match_error.html", {'error': "Non risulti fra i giocatori di questa partita"})
    if not (mat := mat[0]).is_started_match:
        stuff = {
            'match': mat
        }
        return render(request, "match_preview.html", stuff)
    else:
        stuff = {'match_id': mat.id}

        return render(request, "match_play.html", stuff)


@login_required
def ajax_request_match_info(request) -> JsonResponse:
    """
    Requests info for a match. There is control over player permission to see the card.
    :param request:
    :return: A dict with only the scrictly neccessary data do play
    """
    if request.method != "POST":
        return JsonResponse({'state': "bad request"})
    match_id: int = request.POST.get('id')
    match_query = match_scopa.objects.filter(id=match_id)
    match_query = match_query.filter(
        Q(player1=request.user) | Q(player2=request.user) | Q(player3=request.user) | Q(player4=request.user))
    if len(match_query) == 0:
        return JsonResponse({'state': "match non trovato"})
    data = {}
    match: match_scopa = match_query[0]

    if not match.is_started_game:
        raise NotImplementedError("not implemented wait situation")

    temp_players = [match.player1.username, match.player2.username]
    temp_score = [match.player1_points, match.player2_points]
    if match.players_amount > 2:
        temp_players.append(match.player3.username)
        temp_score.append(match.player3_points)
    if match.players_amount > 3:
        temp_players.append(match.player4.username)
        temp_score.append(match.player4_points)
    data['player_list'] = temp_players
    data['score_list'] = temp_score
    if match.player1 == request.user:
        data['hand'] = match.player1_hand
    elif match.player2 == request.user:
        data['hand'] = match.player2_hand
    elif match.player3 == request.user:
        data['hand'] = match.player3_hand
    elif match.player4 == request.user:
        data['hand'] = match.player4_hand

    data['ground'] = match.ground
    data['state'] = "success"
    return JsonResponse(data)


@login_required()
def ajax_play_card(request):
    if request.method != "POST":
        return JsonResponse({'state': "Bad request"})

    match_id: int = request.POST.get('id')
    card_played: str = request.POST.get('card_played')
    card_taken: str = request.POST.get('card_taken')

    match_query = match_scopa.objects.filter(id=match_id)
    match_query = match_query.filter(
        Q(player1=request.user) | Q(player2=request.user) | Q(player3=request.user) | Q(player4=request.user))
    if len(match_query) == 0:
        return JsonResponse({'state': "match non trovato"})
    match: match_scopa = match_query[0]
    message = match.play_card(request.user, card_played, card_taken)
    return JsonResponse({'state': message})

