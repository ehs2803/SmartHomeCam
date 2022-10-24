from django.urls import path

from SmartHomeCam.settings import base
from account import views
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', views.signup), # 회원가입
    path('logout/', views.logout, name="logout"), # 로그아웃
    # path('facelogin', views.FaceLogin),
    path('', views.login, name="login"), # 로그인
]
urlpatterns += static(base.STATIC_URL, document_root=base.STATIC_ROOT)