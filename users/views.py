from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login

from Budgeting.views import home_budget
# from django.contrib.auth.models import AbstractUser
from users.models import User

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def login_request(request):
    if request.method == "POST":
        if 'login' in request.POST:

            username = request.POST.get('username_l')
            password = request.POST.get('password_l')

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return home_budget(request)
            else:
                return HttpResponseRedirect('/')

        else:

            return render(request, 'error.html', {'err': "Login o registrazione rotti "})

    print(get_client_ip(request))

    stuff = {

    }

    return render(request, 'login.html', stuff)


def validate_username_l(request):
    username = request.GET.get('username', None)
    return JsonResponse({'exist': User.objects.filter(username__iexact=username).exists()})


def ajax_login(request):
    response = {
        'errore': 0
    }
    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username)
        print(password)

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse(response)
        else:
            response['errore'] = 2
            return JsonResponse(response)


    else:

        response['errore'] = 1

        return JsonResponse(response)
