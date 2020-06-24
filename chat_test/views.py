# chat/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'templates/chat_index.html')

def room(request, room_name):
    return render(request, 'templates/room.html', {
        'room_name': room_name
    })

