from django.urls import path

from article.api.v0 import views

app_name = 'article'


urlpatterns = [
    path('create', views.article_create_view, name='create'),
    path('retrieve/<int:pk>', views.ArticleViewSet.as_view(actions={"get": "retrieve"}), name='retrieve'),
]
