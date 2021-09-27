from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from article.api.v0.serializers import ArticleCreationSerializer


@api_view(('POST', ))
@permission_classes([IsAuthenticated])
def article_create_view(request):

    if request.method == 'POST':
        serializer = ArticleCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request.user.id)
            return Response(data={
                "success": True,
                "errors": {},
                "data": {},
                "status": "Article Added Successfully"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                "success": False,
                "errors": serializer.errors,
                "status": "Failed To Add a New Article"
            }, status=status.HTTP_400_BAD_REQUEST)

    return Response(data={
        "success": False,
        "errors": {},
        "status": "Method Not Allowed"
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)