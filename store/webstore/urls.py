from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from store import settings
# from views import ContactView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('home/', views.home, name='index'),  # сделать http redirect !! на обычный
    path('about/', views.about, name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('category/<int:id>/<slug:slug>', views.category, name='category'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

