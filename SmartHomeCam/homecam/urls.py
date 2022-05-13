from django.conf.urls.static import static
from django.urls import path

from SmartHomeCam import settings
from homecam import views

urlpatterns = [
    path('', views.landing),
    path('basic/', views.basic),
    path('basic/<username>/<id>/', views.basic_livecam),
    path('video_basic/<username>/<id>/', views.video_basic, name="video_basic"),
    path('pet/', views.pet),
    path('video_pet', views.video_pet, name="video_pet"),
    path('ajax/config/<username>/<id>/', views.ajax_connect_config),
    path('ajax/disconnect/<username>/<id>/', views.ajax_disconnect),
    path('ajax/capture/<username>/<id>/', views.ajax_capture),
    path('ajax/videoRC/<username>/<id>/', views.ajax_video_recording),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#(?P<username>[^/]+)$