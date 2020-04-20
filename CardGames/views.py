from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from .models import match_scopa, match_invite


@login_required
def game_homepage(request):
    stuff = {}

    games_list = match_scopa.objects.filter(
        Q(player1=request.user) | Q(player2=request.user) | Q(player3=request.user) | Q(player4=request.user))

    prelist = []
    glist = []
    for j in games_list:
        glist.append(j)
        # t = []
        # if j.player1 == request.user:
        #     t.append(True)  #t0
        # else:
        #     t.append(False)
        # t.append(j.is_started_game)  #t1
        # t.append(j.id)  # t2
        # t.append(j.player1.username) # t3
        # t.append(j.player2.username) # t4
        # if j.players_amount > 2:
        #     t.append(j.player3.username)
        # if j.players_amount > 3:
        #     t.append(j.player4.username)
        # prelist.append(t)
    #
    # stuff['games_list'] = prelist
    stuff['games_set'] = glist
    return render(request, "game_homepage.html", stuff)


@login_required
def match_view(request, match_id=-1):
    if match_id == -1:
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
        if not mat.is_started_game:
            stuff = {
                'match': mat
            }
            return render(request, "match_preview.html", stuff)

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
        return JsonResponse({'state': "success", 'redirect': 'true'})

    temp_players = [match.player1.username, match.player2.username]
    temp_score = [match.player1_points, match.player2_points]
    if match.players_amount > 2:
        temp_players.append(match.player3.username)
        temp_score.append(match.player3_points)
    else:
        temp_players.append("")
        temp_score.append(0)
    if match.players_amount > 3:
        temp_players.append(match.player4.username)
        temp_score.append(match.player4_points)
    else:
        temp_players.append("")
        temp_score.append(0)
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

    if match.player1 == request.user:
        data['player_num'] = 1
    elif match.player2 == request.user:
        data['player_num'] = 2
    elif match.player3 == request.user:
        data['player_num'] = 3
    elif match.player4 == request.user:
        data['player_num'] = 4

    data['last_move'] = ""

    data['player_to_play'] = match.player_to_play

    data['state'] = "success"
    data['redirect'] = "false"
    data['last_plays'] = match.last_plays.split("||")
    return JsonResponse(data)


@login_required()
def ajax_play_card(request) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({'state': "Bad request"})

    match_id: int = request.POST.get('id')
    card_played: str = request.POST.get('card_played')
    card_taken: str = request.POST.get('card_taken')

    if len(card_played) != 2:
        return JsonResponse({'state': "Played card is not actually playable"})

    match_query = match_scopa.objects.filter(id=match_id)
    match_query = match_query.filter(
        Q(player1=request.user) | Q(player2=request.user) | Q(player3=request.user) | Q(player4=request.user))
    if len(match_query) == 0:
        return JsonResponse({'state': "match non trovato"})
    match: match_scopa = match_query[0]
    message = match.play_card(request.user, card_played, card_taken)
    return JsonResponse({'state': message})


@login_required
def start_match(request, match_id=0):
    if match_id == 0:
        return render(request, 'match_error.html', {'errore': 'no match found'})
    mat = match_scopa.objects.filter(id=match_id)[0]
    if mat.player1 == request.user:
        mess = mat.initiate_new_game()
        if mess:
            return match_view(request, match_id=match_id)
        return render(request, 'match_error.html', {'errore': 'unable to start the match'})


@login_required
def join_match(request, id=-1, password=-1):
    if id == -1 or password == -1:
        return render(request, "match_error.html", {'errore': "Link di invito non valido :("})
    inv = match_invite.objects.filter(joining_id=id, joining_passwd=password)
    if len(inv) == 0:
        return render(request, "match_error.html",
                      {'errore': "Link di invito non valido"})
    i: match_invite = inv[0]
    if i.match_scopa.is_started_match:
        return render(request, "match_error.html",
                      {'errore': "La partita è già inziata :("})
    if i.match_scopa.players_amount == 1:
        if i.match_scopa.player1 == request.user:
            return render(request, "match_error.html",
                          {'errore': "Fai già parte di questo match"})
        i.match_scopa.player2 = request.user
        i.match_scopa.players_amount = 2
    elif i.match_scopa.players_amount == 2:
        if i.match_scopa.player1 == request.user or i.match_scopa.player2 == request.user:
            return render(request, "match_error.html",
                          {'errore': "Fai già parte di questo match"})
        i.match_scopa.player3 = request.user
        i.match_scopa.players_amount = 3
    elif i.match_scopa.players_amount == 3:
        if i.match_scopa.player1 == request.user or i.match_scopa.player2 == request.user or i.match_scopa.player3 == request.user:
            return render(request, "match_error.html",
                          {'errore': "Fai già parte di questo match"})
        i.match_scopa.player4 = request.user
        i.match_scopa.players_amount = 4
    elif i.match_scopa.players_amount == 4:
        return render(request, "match_error.html",
                      {'errore': "La partita ha già raggiunto il limite massimo di partecipanti D:"})
    i.match_scopa.save()
    return match_view(request, i.match_scopa.id)
