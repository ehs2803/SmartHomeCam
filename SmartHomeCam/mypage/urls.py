from django.conf.urls.static import static
from django.urls import path
from django.views.static import serve

from SmartHomeCam.settings import base
from mypage import views

urlpatterns = [
    path('', views.landing), # 데시보드
    path('homecam/manage/', views.homecam_manage_list), # 홈캠 관리 페이지
    path('alarm/list/', views.alarm_list), # 알람 리스트 페이지
    path('alarm/list/<id>/', views.alarm_list_homecam), # 알람 상세 보기
    path('familyInfo/', views.family), # 가족 정보 페이지
    path('familyInfo/<id>/', views.family_detail), # 가족 정보 상세보기
    path('register_family/', views.register_family, name="familyregister"), # 가족 등록
    path('family/update/<id>/', views.update_family, name="familyupdate"), # 가족 정보 수정
    path('family/delete/<id>/', views.delete_family, name="familydelete"), # 가족 정보 삭제
    path('capturePictures/', views.user_capture_pictures), # 사용자 캡처 이미지 목록 페이지
    path('capture/<id>/', views.user_capture_picture_detail), # 사용자 캡처 이미지 상세 페이지
    path('capture/delete/<id>/', views.delete_capture), # 사용자 캡처 이미지 삭제
    path('recordingVideos/', views.user_recording_videos), # 사용자 녹화 동영상 목록 페이지
    path('video/<id>/', views.user_recording_video_detail), # 사용자 녹화 동영상 상세 페이지
    path('video/delete/<id>/', views.delete_video), # 사용자 녹화 동영상 삭제
    path('records/detectPerson/', views.record_detect_person), # 사람 탐지 목록 페이지
    path('records/detectPerson/<id>/', views.record_detect_person_detail), # 사람 탐지 상세 페이지
    path('records/detectPerson/delete/<id>/', views.delete_record_detect_person), # 사람 탐지 기록 삭제
    path('records/unknownDetect/', views.record_detect_unknown), # 외부인 탐지 목록 페이지
    path('records/unknownDetect/<id>/', views.record_detect_unknown_detail), # 외부인 탐지 상세 페이지
    path('records/unknownDetect/delete/<id>/', views.delete_record_detect_unknown), # 외부인 탐지 기록 삭제
    path('records/detectFire/', views.record_detect_fire), # 화재 탐지 목록 페이지
    path('records/detectFire/<id>/', views.record_detect_fire_detail), # 화재 탐지 상세 페이지
    path('records/detectFire/delete/<id>/', views.delete_record_detect_fire), # 화제 탐지 기록 삭제
    path('records/detectAnimal/', views.record_detect_animal), # 반려동물 탐지 활동성 통계 그래프 페이지
    path('records/safemode/noPerson/', views.record_safemode_noPerson), # 사람미탐지 목록 페이지
    path('records/safemode/noAction/', views.record_safemode_noAction), # 사람 행동 미감지 목록 페이지
    path('records/safemode/noAction/<id>/', views.record_safemode_noAction_detail), # 사람 행동 미감지 상세 페이지
    path('records/safemode/noAction/delete/<id>/', views.record_safemode_noAction_delete), # 사람 행동 미감지 기록 삭제
    #path('records/safemode/falldown/', views.record_safemode_falldown),
]

urlpatterns += static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)
urlpatterns += static(base.STATIC_URL, document_root=base.STATIC_ROOT)
#urlpatterns+=url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT})
#urlpatterns+=url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})