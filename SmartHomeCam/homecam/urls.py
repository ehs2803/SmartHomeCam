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
    path('ajax/configs/<username>/<id>/', views.config_info),
    path('ajax/config/rc/<username>/<id>/', views.config_Recording),
    path('ajax/config/detectperson/<username>/<id>/', views.config_detect_person),
    path('ajax/config/recognitionface/<username>/<id>/', views.config_recognition_face),
    path('ajax/config/detectfire/<username>/<id>/', views.config_detect_fire),
    path('ajax/config/detectanimal/<username>/<id>/', views.config_detect_animal),
    path('ajax/config/safemode/<username>/<id>/', views.config_safe_mode),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#(?P<username>[^/]+)$