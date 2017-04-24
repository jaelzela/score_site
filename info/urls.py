from django.conf.urls import url

from info import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'signup', views.signup, name='signup'),
    url(r'login', views.login_user, name='login'),
    url(r'logout', views.logout_user, name='logout'),
    #url(r'activate', views.activate_user, name='activate_user'),
    #url(r'assignment', views.user_assignment, name='user_assignment'),
    url(r'webservice/infoscore', views.info_score_webservice, name='infoscorewebservice'),
    #url(r'comment/score', views.score_comment, name='scorecomment'),
    #url(r'comment/review', views.review_comment, name='reviewcomment'),
    #url(r'webservice', views.web_service, name='webservice'),
    url(r'main', views.main, name='main'),
]