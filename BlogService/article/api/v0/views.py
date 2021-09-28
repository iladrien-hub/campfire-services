from rest_framework import status, mixins, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from article.api.v0.serializers import ArticleCreationSerializer, ArticleSerializer
from article.models import Article


class ArticleViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        queryset = Article.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ArticleSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        serializer = ArticleCreationSerializer(data=request.data)
        if serializer.is_valid():
            article = serializer.save(request.user.id)
            return Response(data={
                "success": True,
                "errors": {},
                "data": ArticleSerializer(instance=article).data,
                "status": "Article Added Successfully"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                "success": False,
                "errors": serializer.errors,
                "status": "Failed To Add a New Article"
            }, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return (AllowAny(),)
        return (IsAuthenticated(),)
