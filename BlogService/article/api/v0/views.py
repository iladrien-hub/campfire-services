from rest_framework import status, viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from article.api.v0.serializers import ArticleCreationSerializer, ArticleSerializer
from article.models import Article


class ArticleViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        serializer = ArticleSerializer(article)
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

    def destroy(self, request, pk=None):
        article = get_object_or_404(Article.objects.all(), pk=pk)
        if article.user != request.user.id:
            return Response(data={
                "success": False,
                "errors": {},
                "status": "Forbidden"
            }, status=status.HTTP_403_FORBIDDEN)
        article.delete()
        return Response(data={
            "success": True,
            "errors": {},
            "status": "Deleted"
        }, status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return (AllowAny(),)
        return (IsAuthenticated(),)


class ArticleSearchView(generics.ListAPIView):

    permission_classes = (AllowAny, )
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.filter(user=self.request.query_params["user"])