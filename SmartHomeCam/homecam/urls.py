from django.urls import path
from homecam import views

urlpatterns = [
    path('', views.landing),
    path('basic/', views.basic),
    path('basic/<username>/<id>/', views.basic_livecam),
    path('pet/', views.pet),
    path('video_basic/<username>/<id>/', views.video_basic, name="video_basic"),
    path('video_pet', views.video_pet, name="video_pet"),
    path('ajax/', views.ajax_method),
    path('ajax/disconnect/<username>/<id>/', views.ajax_disconnect),
]
#(?P<username>[^/]+)$