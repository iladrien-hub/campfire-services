from rest_framework import serializers

from article.models import Article


class ArticleCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['title', 'text']

    def save(self, user):
        article = Article(
            title=self.validated_data['title'],
            text=self.validated_data['text'],
            user=user
        )
        article.save()
        return article