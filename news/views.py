from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.views import View
from django.conf import settings as conf_settings
from datetime import datetime
import json


def get_articles():
    with open(conf_settings.NEWS_JSON_PATH) as f:
        articles = json.load(f)
    return articles


class NewsDetailView(View):
    def get(self, request, link):
        for article in get_articles():
            if link == article['link']:
                context = article
                return render(request, 'news/news_detail.html', context=context)
        return HttpResponseNotFound()


class NewsListView(View):
    def get(self, request):
        articles = get_articles()
        articles = sorted(articles, key=lambda k: k['created'], reverse=True)
        arts = []
        prev_created = ''
        q = request.GET.get('q')
        q = '' if q is None else q
        for article in articles:
            if q in article['title']:
                a = {}
                a['link'] = article['link']
                a['title'] = article['title']
                if article['created'][:10] != prev_created:
                    a['created'] = article['created'][:10]
                    prev_created = a['created']
                arts.append(a)
        return render(request, 'news/main.html', context={'articles': arts})

    def post(self, request):
        return redirect('/news/?q=' + request.POST.get('q'))


class NewsCreateView(View):

    def get(self, request):
        return render(request, 'news/news_create.html')

    def post(self, request):
        title = str(request.POST.get('title'))
        text = str(request.POST.get('text'))
        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        articles = get_articles()
        link = len(articles) + 1
        articles.append({'title': title, 'text': text, 'created': created, 'link': link})
        with open(conf_settings.NEWS_JSON_PATH, 'w') as f:
            json.dump(articles, f)
        return redirect('/news/')


