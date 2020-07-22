from __future__ import print_function

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
        'state': "error"
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
            response['state'] = "success"
            return JsonResponse(response)
        else:

            response['state'] = "Errore: User not found"
            return JsonResponse(response)

    else:
        response['state'] = "Errore: Bad request"

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


google_client_id = "546317649909-arqlqr3sft8mgk3sc6pde0pact1vnkr0.apps.googleusercontent.com"
google_client_secret = "svJWoBRVzFUaBKjm0fFjTwD8"


# todo: far funzionare le mail

def sendmail(request=1):
    import pickle
    import os.path
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request

    # If modifying these scopes, delete the file token.pickle.

    SCOPES = ['https: // mail.google.com /',
              'https: // www.googleapis.com / auth / gmail.modify',
              'https: // www.googleapis.com / auth / gmail.compose',
              'https: // www.googleapis.com / auth / gmail.send']

    def main():
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('gmail', 'v1', credentials=creds)

    main()

# todo: login generalized for the admin
# todo: moody and deleting account is a bug
