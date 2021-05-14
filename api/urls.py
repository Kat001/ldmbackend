from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here


urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

]
