from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework import permissions

# router=DefaultRouter()
# router.register(r'',AdminsViewSet)



urlpatterns=[
    path('superuser/<int:pk>/', views.SuperuserProfileView.as_view()),
    path('admin/<int:pk>/', views.AdminProfileView.as_view()),
    path('admins/', views.AdminsView.as_view()),
    path('occupant/<int:pk>/', views.OccupantProfileView.as_view()),
    path('occupants/', views.OccupantsView.as_view()),
    path('business/',views.BusinessList.as_view()),
    path('comments/',views.CommentList.as_view()),
    path('occupantlist/', views.OccupantList.as_view(),name='occupant'),
    path('business/', views.BusinessList.as_view(),name='business'),
    path('post/',views.PostList.as_view()),
    path('Hoodlist/', views.NeighborhoodList.as_view(),name='hood'),
    path('hood/', views.NeighborhoodView.as_view(), name='hoodView'),
    

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)