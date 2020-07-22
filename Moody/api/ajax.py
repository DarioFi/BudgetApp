from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponse

from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from Moody.models import moody_record


@login_required
@require_GET
def get_moody_data(request):
    if not hasattr(request.user, "moody_user"):
        return JsonResponse({'status': 'false',
                             'message': "The user hasn't a moody user account, please create one before trying to access its data"},
                            status=500)
    data: moody_record = request.user.moody_user

    date_init = request.GET.get("date_init", None)
    date_end = request.GET.get("date_end", None)

    return JsonResponse(data.get_data_as_dictionary(date_init, date_end))


@login_required
@require_POST
def generate_moody_user_if_not_exist_post(request):
    if not hasattr(request.user, "moody_user"):
        moody_record.objects.create(data=[], user=request.user)
        return JsonResponse({'message': "Moody record created"})
    return JsonResponse({'message': "Moody record already exists"})


@login_required
@require_GET
def check_if_moody_exists(request):
    if not hasattr(request.user, "moody_user"):
        return JsonResponse({'message': "False"})
    return JsonResponse({'message': "True"})


@login_required
@require_POST
def add_data(request):
    datetime = request.POST.get("datetime")
    value = request.POST.get("value")
    if not isinstance(datetime, str) or not isinstance(value, int):
        return JsonResponse({'status': 'false',
                             'message': "Bad data"},
                            status=500)
    status, message = request.user.moody_user.add_data_safe(datetime, value)
    return JsonResponse({'message': message}, status=status)
