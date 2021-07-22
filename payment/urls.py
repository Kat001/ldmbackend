from . import views
from django.conf.urls import url, include
from django.contrib import admin
from .views import PaymentSetupView, PaymentList, create_new_payment, PaymentDetail
from django.urls import path, include
from . import views

urlpatterns = [

    url(r'', include('django_coinpayments.urls', namespace='django_coinpayments')),
    url('^$', PaymentSetupView.as_view(), name='payment_setup'),
    url(r'^payments/$', PaymentList.as_view(), name='payment_list'),
    url(r'^payment/(?P<pk>[0-9a-f-]+)$',
        PaymentDetail.as_view(), name='payment_detail'),
    url(r'^payment/new/(?P<pk>[0-9a-f-]+)$',
        create_new_payment, name='payment_new'),

    path('ipn_view', views.ipn_view, name='ipn_view'),
    path('cheak', views.cheak, name='cheak'),
    path('success', views.success, name='success'),
    # Withdrawal........
    path('withdrawal',views.withdrawal,name='withdrawal')
]
