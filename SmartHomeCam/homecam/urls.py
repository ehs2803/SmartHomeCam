from django.urls import path
from homecam import views

urlpatterns = [
    path('', views.landing),
    path('basic/', views.basic),
    path('pet/', views.pet),
]