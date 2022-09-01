from django.conf.urls.static import static
from django.urls import path
from django.views.static import serve

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
    path('connected/config/<id>/', views.config_mode),
    path('records/detectPerson/', views.record_detect_person),
    path('records/detectPerson/<id>/', views.record_detect_person_detail),
    path('records/detectPerson/delete/<id>/', views.delete_record_detect_person),
    path('records/unknownDetect/', views.record_detect_unknown),
    path('records/unknownDetect/<id>/', views.record_detect_unknown_detail),
    path('records/unknownDetect/delete/<id>/', views.delete_record_detect_unknown),
    path('records/detectFire/', views.record_detect_fire),
    path('records/detectFire/<id>/', views.record_detect_fire_detail),
    path('records/detectFire/delete/<id>/', views.delete_record_detect_fire),
    path('records/detectAnimal/', views.record_detect_animal),
    path('records/safemode/noPerson/', views.record_safemode_noPerson),
    path('records/safemode/noAction/', views.record_safemode_noAction),
    path('records/safemode/noAction/<id>/', views.record_safemode_noAction_detail),
    path('records/safemode/noAction/delete/<id>/', views.record_safemode_noAction_delete),
    #path('records/safemode/falldown/', views.record_safemode_falldown),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#urlpatterns+=url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT})
#urlpatterns+=url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})