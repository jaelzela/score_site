from django.db import models

#   username: jzelar
#   email: jael.zela@lirmm.fr
#   password: programmableweb

class WebService(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    name = models.CharField(max_length=50, null=False)
    description = models.TextField()
    articles = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    developers = models.IntegerField(default=0)
    mashups = models.IntegerField(default=0)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    ws = models.IntegerField()
    text = models.TextField()
    date = models.DateTimeField()

class UserWebService(models.Model):
    user_username = models.CharField(max_length=30)
    ws_id = models.IntegerField()
    score = models.IntegerField(default=0)
    info_score = models.IntegerField(default=0)
    assigned_date = models.DateTimeField(null=True)
    score_date = models.DateTimeField(null=True)
    status = models.IntegerField(default=0)
    review = models.TextField(null=True)

class UserComment(models.Model):
    user_username = models.CharField(max_length=30)
    ws_id = models.IntegerField()
    cmt_id = models.IntegerField()
    score = models.IntegerField(default=0)
    assigned_date = models.DateTimeField(null=True)
    score_date = models.DateTimeField(null=True)
    review = models.TextField(null=True)