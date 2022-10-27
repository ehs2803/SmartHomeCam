#from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from django.views.static import serve

from SmartHomeCam.settings import base

from homecam import views

urlpatterns = [
    path('', views.landing), # dashboard
    path('live/list/', views.live_list), # 연결된 홈캠 리스트
    path('basic/', views.basic), # 홈캠 시작 페이지
    path('basic/<username>/<id>/', views.basic_livecam), # 홈캠 실시간 스트리밍 페이지
    path('video_basic/<username>/<id>/', views.video_basic, name="video_basic"), # StreamingHttpResponse
    path('mode/set/person/<id>/', views.set_mode_detectPerson), # 사람탐지 모드 on/off
    path('mode/set/unknown/<id>/', views.set_mode_detectUnknown), # 외부인탐지 모드 on/off
    path('mode/set/fire/<id>/', views.set_mode_detectFire), # 화재탐지 모드 on/off
    path('mode/set/animal/<id>/', views.set_mode_detectAnimal), # 반려동물탐지 모드 on/off
    path('mode/set/noperson/<id>/', views.set_mode_detectNoPerson), # 일정시간 사람 미감지 모드 on/off
    path('mode/set/noaction/<id>/', views.set_mode_detectNoAction), # 사람 행동 미감지 모드 on/off
    path('mode/set/noperson/day/<id>/', views.set_mode_detectNoPerson_Day), # 일정시간 사람 미감지 모드 시간 설정
    path('ajax/config/<username>/<id>/', views.ajax_connect_config), # 특정 홈카메라 연결 여부
    path('ajax/disconnect/<username>/<id>/', views.ajax_disconnect), # 실시간스트리밍 페이지 - 홈카메라 연결 끊기
    path('ajax/capture/<username>/<id>/', views.ajax_capture), # 실시간 스트리밍 페이지 - 이미지 캡처
    path('ajax/videoRC/<username>/<id>/', views.ajax_video_recording), # 실시간 스트리밍 페이지 - 동영상 녹화
    path('ajax/config/rc/<username>/<id>/', views.config_Recording), # 실시간 스트리밍 페이지 - 동영상 녹화 여부
    path('ajax/config/safemode/setTime/<username>/<id>/', views.config_safe_mode_set_time), # 일정시간 사람 미감지 시간 설정
    path('ajax/data/animal/', views.ajax_getData_Animal), # 반려동물 탐지모드 통계 서비스
    path('ajax/main/', views.main_state), # 데시보드 홈캠 연결 유무 통신
    path('ajax/configs/<username>/<id>/', views.config_info),  # 모드 on/off 정보 - 사용 X
    path('ajax/config/detectperson/<username>/<id>/', views.config_detect_person),  # 사람탐지 on/off - 사용 X
    path('ajax/config/recognitionface/<username>/<id>/', views.config_recognition_face),  # 외부인탐지 on/off - 사용 X
    path('ajax/config/detectfire/<username>/<id>/', views.config_detect_fire),  # 화재탐지 on/off - 사용 X
    path('ajax/config/detectanimal/<username>/<id>/', views.config_detect_animal),  # 반려동물 탐지 on/off - 사용 X
    path('ajax/config/safemode/<username>/<id>/', views.config_safe_mode),  # 안심모드 on/off - 사용 X
]
urlpatterns += static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)
urlpatterns += static(base.STATIC_URL, document_root=base.STATIC_ROOT)

#(?P<username>[^/]+)$
#urlpatterns+=url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT})
#urlpatterns+=url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})