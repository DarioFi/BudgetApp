from django.urls import path, include
from .views import game_homepage, match_view, ajax_request_match_info, ajax_play_card, start_match, join_match

urlpatterns = [
    path('home/', game_homepage, name="game_home"),
    path('matches/<int:match_id>/', match_view, name="match_detail"),
    path('ajax/requestgameinfo/', ajax_request_match_info, name="ajax_info_request"),
    path('ajax/playcard/', ajax_play_card, name="ajax_play_card"),
    path('initiate_match/<int:match_id>/', start_match, name="start_match"),
    path('join_match/<int:id>/<str:password>/', join_match, name="join_match"),
]

# TODO: creare pagina per gestire le partite
