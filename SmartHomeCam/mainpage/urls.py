from django.urls import path

from SmartHomeCam.settings import base
from mainpage import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.landing),
]
urlpatterns += static(base.STATIC_URL, document_root=base.STATIC_ROOT)