from django.shortcuts import render
from .models import Profile, Article


def show_articles(request):
    articles = Article.objects.all()

    return render(
        request,
        'articles.html',
        {'articles': articles,
         }
    )


def show_article(request, id):
    article = Article.objects.get(id=id)
    user = request.user

    if request.method == 'POST':
        user.profile.subscription = True
        user.save()

    return render(
        request,
        'article.html',
        {'article': article,
         'user': user}
    )

