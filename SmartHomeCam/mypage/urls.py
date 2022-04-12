from django.urls import path
from mypage import views

urlpatterns = [
    path('', views.landing),
    path('chart/', views.chart),
]