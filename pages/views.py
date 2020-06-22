from django.shortcuts import render
from Budgeting.views import *
from users.views import login_request
# Create your views here.

def home_view(request, *args, **kwargs):

    if request.user.is_authenticated:
        return home_budget(request) #todo: create a general purpose landing page for budgeting, cardgames and moody
    else:
        return login_request(request)
        pass


def changelog(request):
    return render(request, 'changelog.html', {})