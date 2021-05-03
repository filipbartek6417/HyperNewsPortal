import datetime

from django.shortcuts import render, redirect
from django.views import View
from json import load, dump
from collections import defaultdict
from random import randint
from datetime import datetime


# Create your views here.
class News(View):
    def get(self, request, *args, **kwargs):
        with open('./hypernews/news.json') as news_file:
            final_dict = defaultdict(list)
            query = request.GET.get('q')
            for new in sorted(load(news_file), key=lambda r: r['created']):
                if query is None or query == new['title']:
                    final_dict[new['created'].split(" ")[0]].append(new)
            print(final_dict)
            return render(
                request, 'news/index.html', context={
                    'news': dict(reversed(sorted(final_dict.items())))
                }
            )


class Blog(View):
    def get(self, request, blog_number, *args, **kwargs):
        with open('./hypernews/news.json') as news_file:
            for blog in load(news_file):
                if int(blog_number) == blog['link']:
                    current_blog = blog
                    break
            else:
                current_blog = None
            return render(
                request, 'blogs/index.html', context={
                    'blog': current_blog
                }
            )


class Create(View):
    def get(self, request, *args, **kwargs):
        return render(
            request, 'news/create/index.html'
        )

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        text = request.POST.get('text')
        with open('./hypernews/news.json') as news_file:
            all_news = load(news_file)
            all_links = [i['link'] for i in all_news]
        with open('./hypernews/news.json', 'w') as news_file:
            link = randint(1, 100000)
            while link in all_links:
                link = randint(1, 100000)
            all_news.append({
                'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'text': text,
                'title': title,
                'link': link
            })
            dump(all_news, news_file)
        return redirect('/news')


class Landing(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news')