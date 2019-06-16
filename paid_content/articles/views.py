from django.shortcuts import render
from .models import Profile, Article


def show_articles(request):
    articles = Article.objects.all()
    user = request.user

    return render(
        request,
        'articles.html',
        {'articles': articles,
         'user': user
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


def subscription(request):
    # article = Article.objects.get(id=id)
    user = request.user

    if request.method == 'POST':
        if  not user.profile.subscription:
            user.profile.subscription = True
        else:
            user.profile.subscription = False
        user.save()

    return render(
        request,
        'subscription.html',
        {'user': user}
    )
