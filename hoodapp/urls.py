from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views



urlpatterns=[
    path('superuser/<int:pk>/', views.SuperuserProfileView.as_view()),
    

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)