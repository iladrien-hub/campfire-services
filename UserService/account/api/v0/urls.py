from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from account.api.v0.views import (
    registration_view, authentication_view, account_view, set_personal_view, set_password_view, set_username_view,
    add_photo_view, remove_photo_view
)

app_name = 'account'

urlpatterns = [
    path('register', registration_view, name='register'),
    path('login', obtain_auth_token, name='login'),
    path('authenticate', authentication_view, name='authenticate'),
    path('account', account_view, name='account'),
    path('set/personal', set_personal_view, name='set personal'),
    path('set/password', set_password_view, name='set password'),
    path('set/username', set_username_view, name='set username'),
    path('add/photo', add_photo_view, name='set photo'),
    path('remove/photo', remove_photo_view, name='remove photo'),
]