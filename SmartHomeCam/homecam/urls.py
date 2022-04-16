from django.urls import path
from homecam import views

urlpatterns = [
    path('', views.landing),
    path('basic/', views.basic),
    path('pet/', views.pet),
    path('video_basic', views.video_basic, name="video_basic"),
    path('video_pet', views.video_pet, name="video_pet"),
]