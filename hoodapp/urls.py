from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views



urlpatterns=[
    path('superuser/<int:pk>/', views.SuperuserProfileView.as_view()),
    path('admin/<int:pk>/', views.AdminProfileView.as_view()),
    path('admins/', views.AdminsView.as_view()),
    path('occupant/<int:pk>/', views.OccupantProfileView.as_view()),
    path('occupants/', views.OccupantsView.as_view()),
    path('business/',views.BusinessList.as_view()),
    

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)