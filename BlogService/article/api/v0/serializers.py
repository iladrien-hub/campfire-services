from rest_framework import serializers

from article.models import Article, ArticleImage, Image


class ArticleCreationSerializer(serializers.ModelSerializer):
    image = serializers.ListField(required=False)

    class Meta:
        model = Article
        fields = ['text', 'image']

    def save(self, user):
        article = Article(
            text=self.validated_data['text'],
            user=user
        )
        article.save()
        for image in self.validated_data.get('image', ()):
            article_image = ArticleImage(model=article)
            article_image.set_image(image)
            article_image.save()
        return article


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['image_medium', 'image_big']


class ArticleSerializer(serializers.ModelSerializer):

    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        return ImageSerializer(ArticleImage.objects.filter(model=obj), many=True).data

    class Meta:
        model = Article
        fields = ['pk', 'text', 'created', 'user', 'images']