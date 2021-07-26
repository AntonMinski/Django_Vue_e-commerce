from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import views
from order import views as order_views
from user import views as user_views
from store import settings
# from views import ContactView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('home/', views.home, name='index'),
    path('about/', views.about, name='about'),
    path('choose_laptop/', views.choose_laptop, name='choose_laptop'),
    path('contact_info/', views.contact_info, name='contact_info'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('order/', include('order.urls')),
    path('user/', include('user.urls')),

    path('search/', views.search, name='search'),
    path('search_auto/', views.search_auto, name='search_auto'),
    path('category/<slug:slug>', views.category, name='category'),
    path('shop/', views.shop, name='shop'),
    path('product/<slug:slug>',
         views.ProductView.as_view(), name='product_detail'),
    path('notebookproduct/<slug:slug>',
         views.NotebookView.as_view(), name='notebook_detail'),
    path('shopcart/', order_views.shopcart, name='shopcart'),
    path('signup/', user_views.signup, name='signup'),
    path('login_form/', user_views.login_form, name='login_form'),
    path('logout/', user_views.logout_func, name='logout'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

