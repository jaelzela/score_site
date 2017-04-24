# -*- coding: utf-8 -*-

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from score.models import *
from datetime import date
import urllib2

###########################
####     Controllers   ####
###########################
def index(request):
    """ Index view shows login page.
    :param request: GET request.
    :return response: login page.
    """
    next = request.GET.get('next', 'main')
    return render(request, 'score/login.html', dict(next=next))


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
            #request.session.set_expiry(30)
            return HttpResponseRedirect(next)
        else:
            response_dict['login_error'] = "Account is not active!"
    else:
        response_dict['login_error'] = "Wrong user or password!"

    response_dict['username'] = username
    return render(request, 'score/login.html', response_dict)


def logout_user(request):
    """ Logout user from the application.
    :param request: GET request.
    :return response: login page.
    """
    logout(request)
    return render(request, 'score/login.html', dict())


@login_required(login_url='/score_site/score')
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
    available = True
    for api in apis:
        uws = uws_dict[api.id]
        if uws.score_date:
            api.scored = 1
            api.available = available
        else:
            if available:
                api.available = available
                available = False
            api.scored = 0

    return render(request, 'score/main.html', dict(apis=apis))


@login_required(login_url='/score_site/score')
def web_service(request):
    username = request.user.username
    uwss = UserWebService.objects.filter(user_username=username)
    ws_ids = []
    uws_dict = dict()
    porc = 0
    for uws in uwss:
        ws_ids.append(uws.ws_id)
        uws_dict[uws.ws_id] = uws
        if uws.score_date:
            porc += 5
    apis = WebService.objects.filter(id__in=ws_ids)
    paginator = Paginator(apis, 1)

    #print request.META['HTTP_REFERER']

    try: page_number = int(request.GET.get('page', '1'))
    except ValueError: page_number = 1

    try: apis = paginator.page(page_number)
    except (InvalidPage, EmptyPage): apis = paginator.page(paginator.num_pages)


    for api in apis:
        uws = uws_dict[api.id]
        if uws.score_date:
            api.scored = 1
            api.score = uws.score
        else:
            api.scored = 0

    comments = []
    if len(apis) > 0:
        api_id = apis[0].id
        comments = Comment.objects.filter(ws=int(api_id))
        user_comments = UserComment.objects.filter(user_username=username)
        user_comment_dict= dict()
        for user_comment in user_comments:
            user_comment_dict[user_comment.cmt_id] = user_comment

        for comment in comments:
            user_comment = user_comment_dict[comment.id]
            if user_comment.score_date:
                comment.scored = 1
                comment.score = user_comment.score
                if user_comment.review:
                    comment.review = user_comment.review
                else:
                    comment.review = ''
            else:
                comment.scored = 0


    return render(request, 'score/web_service.html', dict(apis=apis, comments=comments, porcentage=porc))

@login_required(login_url='/score_site/score')
def score_comment(request):
    username = request.user.username
    cmt_id = request.POST.get('cmt_id')
    score = request.POST.get('score')
    status = 200
    try:
        user_comment = UserComment.objects.get(user_username=username, cmt_id=cmt_id)
        user_comment.score = score
        user_comment.score_date = date.today()
        user_comment.save()
    except Exception:
        status = 500
    return JsonResponse({'status': status})

@login_required(login_url='/score_site/score')
def review_comment(request):
    username = request.user.username
    cmt_id = request.POST.get('cmt_id')
    review = request.POST.get('review')
    status = 200
    try:
        user_comment = UserComment.objects.get(user_username=username, cmt_id=cmt_id)
        user_comment.review = review
        user_comment.save()
    except Exception:
        status = 500
    return JsonResponse({'status': status})


@login_required(login_url='/score_site/score')
def score_webservice(request):
    username = request.user.username
    ws_id = request.POST.get('ws_id')
    score = request.POST.get('score')
    print ws_id, score
    status = 200
    try:
        user_webservice = UserWebService.objects.get(user_username=username, ws_id=ws_id)
        user_webservice.score = score
        user_webservice.score_date = date.today()
        user_webservice.save()
    except Exception:
        status = 500
    return JsonResponse({'status': status})


def signup(request):
    if request.method == 'GET':
        return render(request, "score/signup.html", dict())
    elif request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '').lower()
        password = request.POST.get('password', '')
        error = ""
        try:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
            user.is_active = False
            user.save()
        except IntegrityError:
            error = "Email address already registered."
            return render(request, "score/signup.html", dict(signup_error=error))

        print user, user.is_active
        return render(request, "score/confirmation.html", dict(type='signup'))
    else:
        return render(request, 'score/login.html', dict())


def activate_user(request):
    print 'me', request.method
    if request.method == 'GET':
        print 'id', request.GET.get('id')
        if request.GET.get('id'):
            id = str(request.GET.get('id'))
            id = urllib2.unquote(id)
            email = str(request.GET.get('e'))
            email = urllib2.unquote(email)
            users = User.objects.filter(password="pbkdf2_sha"+id, email=email)
            print 'user', users
            if len(users) > 0:
                print 'active', users[0].is_active
                if users[0].is_active:
                    raise Http404
                print users
                return render(request, 'score/activate.html', dict(new_user=users[0]))
            else:
                raise Http404
        else:
            raise Http404
    elif request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        if user:
            user.is_active = True
            user.save()

            apis = WebService.objects.all()
            for api in apis:
                user_wss = UserWebService.objects.filter(ws_id=api.id)
                api.num_scores = len(user_wss)
            return render(request, 'score/assignment.html', dict(apis=apis, type='activation', new_user=user))
        else:
            raise Http404

    return HttpResponseRedirect('/')


def user_assignment(request):
    if request.method == 'GET':
        raise Http404
    elif request.method == 'POST':
        keys = request.POST.keys()
        username = request.POST.get('username')

        if not username:
            raise Http404

        for key in keys:
            if str(key).startswith('ws'):
                ws_id = key.replace('ws', '')
                user_webservice = UserWebService()
                user_webservice.user_username = username
                user_webservice.ws_id = ws_id
                user_webservice.assigned_date = date.today()
                user_webservice.save()

                comments = Comment.objects.filter(ws=ws_id)

                for comment in comments:
                    user_comment = UserComment()
                    user_comment.cmt_id = comment.id
                    user_comment.ws_id = ws_id
                    user_comment.user_username = username
                    user_comment.assigned_date = date.today()
                    user_comment.save()

        return HttpResponseRedirect('/score_site/score')
    else:
        return HttpResponseRedirect('/score_site/score')


@login_required(login_url='/score_site/score')
def review_webservice(request):
    username = request.user.username
    ws_id = request.POST.get('ws_id')
    review = request.POST.get('review')
    status = 200
    try:
        user_webservice = UserWebService.objects.get(user_username=username, ws_id=ws_id)
        user_webservice.review = review
        user_webservice.save()
    except Exception:
        status = 500
    return JsonResponse({'status': status})


@login_required(login_url='/score_site/score')
def complete_webservice(request):
    username = request.user.username
    ws_id = request.POST.get('ws_id')
    status = 200
    print ws_id
    try:
        user_webservice = UserWebService.objects.get(user_username=username, ws_id=ws_id)
        user_webservice.status = 100
        user_webservice.save()
    except Exception:
        status = 500
    return JsonResponse({'status': status})