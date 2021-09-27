import binascii
import io
import os

from PIL import Image as PILImage
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils.deconstruct import deconstructible


class Article(models.Model):
    text = models.TextField(verbose_name="Text")
    user = models.IntegerField(verbose_name="Author")
    created = models.DateTimeField(verbose_name="Created at", auto_now=True)

    def __str__(self):
        return f"Article(user={self.user}, created={self.created})"


@deconstructible
class UploadTo(object):
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        return os.path.join(".", self.path, f"{binascii.hexlify(os.urandom(20)).decode()}.jpg")


class Image(models.Model):
    image_medium = models.ImageField(upload_to=UploadTo('medium'))
    image_big = models.ImageField(upload_to=UploadTo('big'))

    def resize(self, image, size):
        resize = min(image.size[0], size)
        pil_cropped = image.resize((resize, resize), PILImage.ANTIALIAS)

        buffer = io.BytesIO()
        pil_cropped.save(fp=buffer, format="JPEG", quality=95)
        cropped = ContentFile(buffer.getvalue())

        return InMemoryUploadedFile(
            cropped,  # file
            None,  # field_name
            "image.jpg",  # file name
            'image/jpeg',  # content_type
            cropped.tell,  # size
            None  # content_type_extra
        )

    def set_image(self, image):
        tmp = PILImage.open(io.BytesIO(image.read()))
        # Cropping
        width, height = tmp.size
        side = min(width, height)
        pil_cropped = tmp.crop(
            (width / 2 - side / 2, height / 2 - side / 2, width / 2 + side / 2, height / 2 + side / 2))

        # Resizing
        self.image_medium = self.resize(pil_cropped, 256)
        self.image_big = self.resize(pil_cropped, 800)

    def __str__(self):
        return str(self.image_medium)


class ArticleImage(Image):
    model = models.ForeignKey(Article, on_delete=models.CASCADE)