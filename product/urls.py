from django.urls import path, include
from .views import ProductIndexView, ProductCreateView, ProductDetailView, ProductEditView

app_name = 'product'
urlpatterns = [
    path('products', ProductIndexView.as_view(), name='products'),
    path('product', ProductCreateView.as_view(), name='product'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='detail'),
    path('products/<int:pk>', ProductEditView.as_view(), name='edit'),
]
