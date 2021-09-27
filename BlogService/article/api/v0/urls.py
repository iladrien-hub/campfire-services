from django.urls import path

from article.api.v0.views import article_create_view

app_name = 'article'


urlpatterns = [
    path('create', article_create_view, name='create'),
]
