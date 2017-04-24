from django.shortcuts import render
import json
from collections import Counter
# Create your views here.
class WebServicesFP:
    def __init__(self):
        self.id = None
        self.name = ''
        self.user_scores = []
        self.comments = []
        self.fp = ''

class CommentFP:
    def __init__(self):
        self.id = None
        self.text = ''
        self.user_scores = []
        self.fp = ''
        self.tuples = []
        self.tuples_polarity = []
        self.pos = ''

def get_mode(elements):
    data = Counter(elements)
    counters = data.most_common()

    if len(counters) > 1 and len(counters) == len(elements):
        return [None]

    return counters[0]

def read_webservices(part):
    with open('/Users/jzelar/Documents/MAESTRIA/FRANCIA/Development/Project/jael/code/score_site/fp/score_site_fp.json') as data_file:
        apis = json.load(data_file)
        data_file.close()

    apis = apis[21*part: 21*part+21]
    print 'len', len(apis)

    wss = []
    for api in apis:
        ws = WebServicesFP()
        ws.id = api['id']
        ws.name = api['name']
        for user_score in api['user_scores']:
            ws.user_scores.append(user_score['score'])
        fp_str = ''
        if api['fp_pos']:
            fp_str += ' POSITIVE'
        if api['fp_neg']:
            fp_str += ' NEGATIVE'
        if api['fp_neu']:
            fp_str += ' NEUTRAL'

        mode_val = get_mode(ws.user_scores)[0]
        if mode_val is None:
            fp_str += ' NO CONSENSUS (not included in the experimentation)'

        ws.fp = fp_str.strip()

        if len(ws.fp) == 0:
            ws.fp = 'NO FALSE POSITIVE'

        for comment in api['comments']:
            cmt = CommentFP()
            cmt.id = comment['id']
            cmt.text = comment['comment']
            for user_cmt_score in comment['user_scores']:
                cmt.user_scores.append(user_cmt_score['score'])
            fp_cmt_str = ''
            if comment['fp_pos']:
                fp_cmt_str += ' POSITIVE'
            if comment['fp_neg']:
                fp_cmt_str += ' NEGATIVE'
            if comment['fp_neu']:
                fp_cmt_str += ' NEUTRAL'

            mode_val = get_mode(cmt.user_scores)[0]
            if mode_val is None:
                fp_cmt_str += ' NO CONSENSUS (not included in the experimentation)'

            cmt.fp = fp_cmt_str.strip()
            cmt.pos = str(comment['pos'])

            if len(cmt.fp) == 0:
                cmt.fp = 'NO FALSE POSITIVE'

            for tuple in comment['tuples']:
                cmt.tuples.append(tuple)
            for polarity in comment['tuples_polarity']:
                cmt.tuples_polarity.append(polarity)

            ws.comments.append(cmt)

        wss.append(ws)

    return wss

def read_webservices_fn(part):
    with open('/Users/jzelar/Documents/MAESTRIA/FRANCIA/Development/Project/jael/code/score_site/fp/score_site_fn.json') as data_file_fn:
        apis_fn = json.load(data_file_fn)
        data_file_fn.close()

    apis_fn = apis_fn[21*part: 21*part+21]
    print 'len', len(apis_fn)

    wss = []
    for api in apis_fn:
        ws = WebServicesFP()
        ws.id = api['id']
        ws.name = api['name']
        for user_score in api['user_scores']:
            ws.user_scores.append(user_score['score'])
        fp_str = ''
        if api['fp_pos']:
            fp_str += ' POSITIVE'
        if api['fp_neg']:
            fp_str += ' NEGATIVE'
        if api['fp_neu']:
            fp_str += ' NEUTRAL'

        mode_val = get_mode(ws.user_scores)[0]
        if mode_val is None:
            fp_str += ' NO CONSENSUS (not included in the experimentation)'

        ws.fp = fp_str.strip()

        if len(ws.fp) == 0:
            ws.fp = 'NO FALSE POSITIVE'

        for comment in api['comments']:
            cmt = CommentFP()
            cmt.id = comment['id']
            cmt.text = comment['comment']
            for user_cmt_score in comment['user_scores']:
                cmt.user_scores.append(user_cmt_score['score'])
            fp_cmt_str = ''
            if comment['fp_pos']:
                fp_cmt_str += ' POSITIVE'
            if comment['fp_neg']:
                fp_cmt_str += ' NEGATIVE'
            if comment['fp_neu']:
                fp_cmt_str += ' NEUTRAL'

            mode_val = get_mode(cmt.user_scores)[0]
            if mode_val is None:
                fp_cmt_str += ' NO CONSENSUS (not included in the experimentation)'

            cmt.fp = fp_cmt_str.strip()

            if len(cmt.fp) == 0:
                cmt.fp = 'NO FALSE POSITIVE'

            for tuple in comment['tuples']:
                cmt.tuples += str(tuple).replace('u\'', '\'') + '  '

            ws.comments.append(cmt)

        wss.append(ws)

    return wss

def first(request):
    web_services = read_webservices(0)
    return render(request, 'fp/web_service.html', dict(apis=web_services))

def second(request):
    web_services = read_webservices(1)
    return render(request, 'fp/web_service.html', dict(apis=web_services))

def third(request):
    web_services = read_webservices(2)
    return render(request, 'fp/web_service.html', dict(apis=web_services))

def first_fn(request):
    web_services = read_webservices_fn(0)
    return render(request, 'fp/web_service.html', dict(apis=web_services))

def second_fn(request):
    web_services = read_webservices_fn(1)
    return render(request, 'fp/web_service.html', dict(apis=web_services))

def third_fn(request):
    web_services = read_webservices_fn(2)
    return render(request, 'fp/web_service.html', dict(apis=web_services))