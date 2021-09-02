from django.urls import path, include
from . import views


urlpatterns = [
    path('product_list/', views.ProductListCreateAPIView.as_view(),
         name='api_product_list'),
    path('product_detail/<int:id>/', views.ProductDetailAPIView.as_view(),
         name='api_product_detail'),
    path('notebook_product_detail/<int:id>/',
         views.NotebookProductDetailAPIView.as_view(),
         name='api_notebook_product_detail'),
    path('category_list/', views.CategoryListCreateAPIView.as_view(),
         name='api_category_list'),
    path('category_list/<int:id>/', views.CategoryDetailCreateAPIView.as_view(),
         name='api_category_list'),

]



