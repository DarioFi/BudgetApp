from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from Budgeting.views import home_budget
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt


User = get_user_model()

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


def does_username_exists(request):
    if User.objects.filter(username__iexact=request.GET.get('username', None)).exists():
        return JsonResponse({'exist': 1})
    return JsonResponse({'exist': 0})


@csrf_exempt
def ajax_login(request):
    response = {
        'errore': 0
    }
    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            response['user'] = username
            token = Token.objects.get(user=user).key
            response['token'] = token
            return JsonResponse(response)
        else:
            response['errore'] = 2
            return JsonResponse(response)

    else:
        response['errore'] = 1

        return JsonResponse(response)


@csrf_exempt
def ajax_register(request):
    if request.method == "POST":  # TODO: aggiungere la registrazione tramite rest api

        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if not ('@' in email and '.' in email):
            return JsonResponse({'state': 'this email is not considered valid'})

        if User.objects.filter(username=username).exists():
            return JsonResponse({'state': 'username already taken'})

        if User.objects.filter(email=email).exists():
            return JsonResponse({'state': 'this email is already associated with an account'})

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        new_user.save()

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)

        response = {'state': 'success'}
        response['user'] = username
        token = Token.objects.get(user=user).key
        response['token'] = token
        return JsonResponse(response)

    else:
        print('Server error')
        return JsonResponse({'state': 'Request Error'})


@api_view(['GET', ])
def is_authenticated(request):
    if request.user.is_authenticated:
        return JsonResponse({'detail': "user authenticated"})
    return JsonResponse({'detail': "valid token, unauthenticated"})
