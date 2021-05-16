from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here
from . import views


urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('return-pack/', views.ReturnPack, name='api_token_auth'),
    path('level-1/', views.LevelOne.as_view(),),
    path('level-2/', views.LevelTwo.as_view(),),
    path('level-3/', views.LevelThree.as_view(),),
    path('level-4/', views.LevelFour.as_view(),),
    path('level-5/', views.LevelFive.as_view(),),

    # ID Upgradation...........
    path('purchase-package/', views.PurchasePackage.as_view(),),


]
