from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from score.models import *
from info.models import *

def index(request):
    """ Index view shows login page.
    :param request: GET request.
    :return response: login page.
    """
    next = request.GET.get('next', 'main')
    return render(request, 'info/login.html', dict(next=next))


@csrf_protect
def login_user(request):
    """ Authenticate a user from login page and create a session, then goes to 'next' page.
    :param request: POST request
    :return response: 'next' page
    """
    if request.method == 'GET':
        raise Http404

    username = request.POST.get('username')
    password = request.POST.get('password')
    next = request.POST.get('next', 'main')

    response_dict = dict()
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(next)
        else:
            response_dict['login_error'] = "Account is not active!"
    else:
        response_dict['login_error'] = "Wrong user or password!"

    response_dict['username'] = username
    return render(request, 'info/login.html', response_dict)


def logout_user(request):
    """ Logout user from the application.
    :param request: GET request.
    :return response: login page.
    """
    logout(request)
    return render(request, 'info/login.html', dict())


@login_required(login_url='/score_site/info')
def main(request):
    """ Web Services view displays all web services assigned to the user.
    :param request: GET request.
    :return response: web services page.
    """
    username = request.user.username
    uwss = UserWebService.objects.filter(user_username=username)
    ws_ids = []
    uws_dict = dict()
    for uws in uwss:
        ws_ids.append(uws.ws_id)
        uws_dict[uws.ws_id] = uws
    apis = WebService.objects.filter(id__in=ws_ids)

    for api in apis:
        api.info_score = -1
        if uws_dict[api.id].status >= 200:
            api.info_score = uws_dict[api.id].info_score

    infos = MaxMin.objects.all()
    return render(request, 'info/main.html', dict(apis=apis, infos=infos))

def info_score_webservice(request):
    username = request.user.username
    ws_id = request.POST.get('ws_id')
    score = request.POST.get('score')
    print ws_id, score
    status = 200
    try:
        user_webservice = UserWebService.objects.get(user_username=username, ws_id=ws_id)
        user_webservice.info_score = score
        user_webservice.status = 200
        user_webservice.save()
    except Exception:
        status = 500
    return JsonResponse({'status': status})
