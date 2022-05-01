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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)