from django.urls import path

from . import views

app_name = 'basicapp'


urlpatterns = [
    path('', views.index, name='index'),
    path('checkout_done/', views.checkout_done, name='checkout_done'),
    path('index2/', views.index2, name='index2'),
    path('checkout/', views.checkout, name='checkout')
]
