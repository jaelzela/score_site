import json
import peewee
from peewee import *
from statistics import mean, stdev

### Open a database connection
db = MySQLDatabase('score_site', user='user', passwd='pass', host='127.0.0.1')

### Mapping for score_webservice table
class score_webservice(peewee.Model):
    id = peewee.IntegerField()
    name = peewee.CharField()
    description = peewee.TextField()
    articles = peewee.IntegerField()
    followers = peewee.IntegerField()
    developers = peewee.IntegerField()
    mashups = peewee.IntegerField()

    class Meta:
        database = db

### Mapping for score_comment table
class score_comment(peewee.Model):
    id = peewee.IntegerField()
    ws_id = peewee.IntegerField()
    text = peewee.TextField()
    date = peewee.DateTimeField()

    class Meta:
        database = db

### Mapping for info_maxmin table
class info_maxmin(peewee.Model):
    id = peewee.IntegerField()
    name = peewee.TextField()
    min = peewee.IntegerField()
    max = peewee.IntegerField()
    mean = peewee.DoubleField()
    stdev = peewee.DoubleField()

    class Meta:
        database = db


### function for sort Web Services by number of comments
def size(item):
    return len(item['comments'])

### Read all Web Services
with open('dataset_apis.json') as data_file:
    apis = json.load(data_file)
    data_file.close()

### Sorting Web Services according its number of comments
sorted_apis = sorted(apis, key=size, reverse=True)

count_apis = 1
comment_id = 1
### Inserting the first 100 Web Services
for api in sorted_apis:
    web_service = score_webservice()
    web_service.id = api['id']
    web_service.name = api['name']
    web_service.description = api['description']
    web_service.save(force_insert=True)

    print api['name']

    for comment in api['comments']:
        ws_comment = score_comment()
        ws_comment.id = comment_id
        ws_comment.ws_id = api['id']
        ws_comment.text = comment['comment']
        ws_comment.date = date.fromtimestamp(comment['date']/1000)
        ws_comment.save(force_insert=True)
        comment_id += 1

    if count_apis == 100:
        break
    count_apis += 1
"""
apis_dict = dict()
for api in sorted_apis:
    apis_dict[int(api['id'])] = api

web_services = score_webservice().select()
articles = []
followers = []
developers = []
mashups = []
for ws in web_services:
    num_articles = len(apis_dict[ws.id]['articles'])
    num_followers = len(apis_dict[ws.id]['followers'])
    num_developers = len(apis_dict[ws.id]['developers'])
    num_mashups = apis_dict[ws.id]['mashups']
    articles.append(num_articles)
    followers.append(num_followers)
    developers.append(num_developers)
    mashups.append(num_mashups)

    #ws.articles = num_articles
    #ws.followers = num_followers
    #ws.developers = num_developers
    #ws.mashups = num_mashups
    #ws.save()


info_articles = info_maxmin()
info_articles.id = 1
info_articles.name = 'Articles'
info_articles.min = min(articles)
info_articles.max = max(articles)
info_articles.mean = mean(articles)
info_articles.stdev = round(stdev(articles), 2)
info_articles.save(force_insert=True)

info_articles = info_maxmin()
info_articles.id = 2
info_articles.name = 'Followers'
info_articles.min = min(followers)
info_articles.max = max(followers)
info_articles.mean = mean(followers)
info_articles.stdev = round(stdev(followers), 2)
info_articles.save(force_insert=True)

info_articles = info_maxmin()
info_articles.id = 3
info_articles.name = 'Developers'
info_articles.min = min(developers)
info_articles.max = max(developers)
info_articles.mean = mean(developers)
info_articles.stdev = round(stdev(developers), 2)
info_articles.save(force_insert=True)

info_articles = info_maxmin()
info_articles.id = 4
info_articles.name = 'Mashups'
info_articles.min = min(mashups)
info_articles.max = max(mashups)
info_articles.mean = mean(mashups)
info_articles.stdev = round(stdev(mashups), 2)
info_articles.save(force_insert=True)

print articles
print followers
print developers
print mashups
print max(articles), min(articles), mean(articles), stdev(articles)
print max(followers), min(followers), mean(followers), stdev(followers)
print max(developers), min(developers), mean(developers), stdev(developers)
print max(mashups), min(mashups), mean(mashups), stdev(mashups)
"""
