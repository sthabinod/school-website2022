from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from news.models import News


@login_required(login_url='login')
def news_details(request, id):
    news = News.objects.get(id=id)
    data = {'news': news}
    return render(request, 'news/news_details.html', data)




