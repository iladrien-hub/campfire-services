import binascii
import io
import os

from PIL import Image
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models


class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    # Standard fields
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Personal info fields
    name = models.CharField(verbose_name="name", max_length=60, default="", blank=True)
    surname = models.CharField(verbose_name="surname", max_length=60, default="", blank=True)
    phone = models.CharField(verbose_name="phone", max_length=60, default="", blank=True)

    # Additional fields
    photo = models.IntegerField(verbose_name="profile image", blank=True, null=True)

    # Authorization
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = AccountManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


def upload_to(path):
    def func(instance, filename):
        return os.path.join(".", path, f"{binascii.hexlify(os.urandom(20)).decode()}.jpg")
    return func


class ProfileImage(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    image_medium = models.ImageField(upload_to=upload_to('medium'))
    image_big = models.ImageField(upload_to=upload_to('big'))

    def resize(self, image, size):
        resize = min(image.size[0], size)
        pil_cropped = image.resize((resize, resize), Image.ANTIALIAS)

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
        tmp = Image.open(io.BytesIO(image.read()))
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
