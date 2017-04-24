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
from statistics import mode
from statistics import StatisticsError
from datetime import date
import urllib2


def index(request):
    """ Index view shows login page.
    :param request: GET request.
    :return response: login page.
    """
    next = request.GET.get('next', 'main')
    return render(request, 'rate/login.html', dict(next=next))


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
    return render(request, 'rate/login.html', response_dict)


def logout_user(request):
    """ Logout user from the application.
    :param request: GET request.
    :return response: login page.
    """
    logout(request)
    return render(request, 'rate/login.html', dict())


@login_required(login_url='/score_site/rate')
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
        if uws.status >= 100:
            api.scored = 1
            api.available = available
        else:
            if available:
                api.available = available
                available = False
            api.scored = 0

    return render(request, 'rate/main.html', dict(apis=apis))


@login_required(login_url='/score_site/rate')
def web_service(request):
    username = request.user.username
    uwss = UserWebService.objects.filter(user_username=username)
    ws_ids = []
    uws_dict = dict()
    porc = 0
    for uws in uwss:
        ws_ids.append(uws.ws_id)
        uws_dict[uws.ws_id] = uws
        if uws.status == 100:
            porc += 5
    apis = WebService.objects.filter(id__in=ws_ids)
    paginator = Paginator(apis, 1)

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

        scores = []
        uwss = UserWebService.objects.filter(ws_id=api.id)
        for uws in uwss:
            try:
                user_number = int(uws.user_username[4:])
            except ValueError:
                user_number = -1
            if user_number >= 0:
                if uws.score_date:
                    scores.append(int(uws.score))
        api.scores = scores
        api.has_mode = False
        try:
            m = mode(api.scores)
            api.has_mode = True
        except StatisticsError:
            api.has_mode = False
        print 'ws', api.scores, api.has_mode

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

            scores = []
            ucs = UserComment.objects.filter(cmt_id=comment.id)
            for uc in ucs:
                try:
                    user_number = int(uc.user_username[4:])
                except ValueError:
                    user_number = -1
                if user_number >= 0:
                    if uc.score_date:
                        scores.append(int(uc.score))
            comment.scores = scores
            comment.has_mode = False
            try:
                m = mode(comment.scores)
                comment.has_mode = True
            except StatisticsError:
                comment.has_mode = False
            print 'cmt', comment.scores, comment.has_mode


    return render(request, 'rate/web_service.html', dict(apis=apis, comments=comments, porcentage=porc))