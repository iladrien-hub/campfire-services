from django.urls import path

from article.api.v0 import views

app_name = 'article'


urlpatterns = [
    path('', views.ArticleViewSet.as_view(actions={"post": "create"}), name='create'),
    path('<int:pk>', views.ArticleViewSet.as_view(actions={"get": "retrieve", "delete": "destroy"})),

    path('search/', views.ArticleSearchView.as_view(), name="search")
]
