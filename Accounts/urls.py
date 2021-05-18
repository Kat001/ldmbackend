from django.urls import path,include
from . import views

urlpatterns = [
    path('sign-up/',views.signup,name="signup"),
    path('sign-up/<slug:username>',views.signup2,name="signup"),
    path('detail/',views.detail,name="detail"),
    path('login/',views.login1, name='login'),
]
