from django.urls import path
from . import views

# functions:
# urlpatterns = [
#     path('product_list', views.product_list_create_api_view, name='api'),
#     path('product_detail/<int:id>/', views.product_detail_api_view, name='api_product_detail'),
# ]

# classes:
urlpatterns = [
    path('product_list', views.ProductListCreateAPIView.as_view(), name='api'),
    path('product_detail/<int:id>/', views.ProductDetailAPIView.as_view(), name='api_product_detail'),
    path('category_list/', views.CategoryListCreateAPIView.as_view(), name='api_category_list'),
]



