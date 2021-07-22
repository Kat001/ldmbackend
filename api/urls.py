from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here
from . import views
from .views import RegisterAPI



urlpatterns = [
    # register............
    path('register/', RegisterAPI.as_view(), name='register'),
    path('change-password/', views.ChangePassword.as_view()),


    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('return-pack/', views.ReturnPack.as_view(),),
    path('user-detail/',views.UserDetail.as_view(),),
    path('check-daily-income/',views.CheckDailyIncome.as_view(),),
    path('transfer-fund/', views.TransferFund.as_view(),),
    path('user-profile/', views.UserProfile.as_view(),),
    path('main-page/', views.MainPage.as_view(),),
    path('level-1/', views.LevelOne.as_view(),),
    path('level-2/', views.LevelTwo.as_view(),),
    path('level-3/', views.LevelThree.as_view(),),
    path('level-4/', views.LevelFour.as_view(),),
    path('level-5/', views.LevelFive.as_view(),),
    path('level-income/', views.LevelIncome1.as_view(),),

    path('roi-on-roi/',views.RoiOnRoi.as_view(),),
    path('link-click/',views.LinkClicked.as_view(),),


    # ID Upgradation...........
    path('purchase-package/', views.PurchasePackage.as_view(),),

    # Download Apk
    path('download-apk/',views.Downloadapk, name="downloadapk"),

    # Signed Up
    path('sign-up/',views.Signup, name="Signup"),

    # links
    path('links/',views.ReturnLinks.as_view(),),

    #Task details...
    path('task-detail/',views.TaskDetails.as_view(),),

    #Withdrawal......
    path('withdrawal/',views.Withdrawal.as_view(),),
    path('withdrawal-history/',views.WithdrawalHistory.as_view(),)

]
