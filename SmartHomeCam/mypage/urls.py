from django.conf.urls.static import static
from django.urls import path

from SmartHomeCam import settings
from mypage import views

urlpatterns = [
    path('', views.landing),
    path('chart/', views.chart),
    path('familyInfo/', views.family),
    path('familyInfo/<id>/', views.family_detail),
    path('register_family/', views.register_family, name="familyregister"),
    path('family/update/<id>/', views.update_family, name="familyupdate"),
    path('family/delete/<id>/', views.delete_family, name="familydelete"),
    path('capturePictures/', views.user_capture_pictures),
    path('capture/delete/<id>/', views.delete_capture),
    path('recordingVideos/', views.user_recording_videos),
    path('video/delete/<id>/', views.delete_video),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)