from django.urls import path

from SmartHomeCam.settings import base
from account import views
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', views.signup),
    path('logout/', views.logout, name="logout"),
    path('facelogin', views.FaceLogin),
    path('', views.login, name="login"), # {% url
]
urlpatterns += static(base.STATIC_URL, document_root=base.STATIC_ROOT)