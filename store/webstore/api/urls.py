from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'setting', views.SettingViewSet)
router.register(r'contact_message', views.ContactMessageViewSet)

setting_list = views.SettingViewSet.as_view({'get': 'list'})
setting_detail = views.SettingViewSet.as_view({'get': 'retrieve'})

contact_message_list = views.ContactMessageViewSet.as_view({'get': 'list'})
contact_message_detail = \
    views.ContactMessageViewSet.as_view({'get': 'retrieve'})



urlpatterns = [
    path('', include (router.urls)),
    path('products/', include('products.api.urls')),
    path('order/', include('order.api.urls')),
    path('user/', include('user.api.urls')),
]

