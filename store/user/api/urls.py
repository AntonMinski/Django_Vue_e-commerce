from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'base', views.UserViewSet)
router.register(r'profile', views.UserProfileViewSet)

base_list = views.UserViewSet.as_view({'get': 'list'})
base_detail = views.UserViewSet.as_view({'get': 'retrieve'})

profile_list = views.UserProfileViewSet.as_view({'get': 'list'})
profile_detail = views.UserProfileViewSet.as_view({'get': 'retrieve'})


urlpatterns = [
    path('', include (router.urls)),
]

