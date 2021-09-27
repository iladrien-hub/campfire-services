from django.db import models


class Article(models.Model):
    title = models.CharField(verbose_name="Title", max_length=60)
    text = models.TextField(verbose_name="Text")

    user = models.IntegerField(verbose_name="Author")

    def __str__(self):
        return self.title
