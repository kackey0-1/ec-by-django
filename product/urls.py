from django.urls import path, include
from .views import ProductIndexView, ProductCreateView, ProductDetailView, ProductEditView, ProductDeleteView

app_name = 'product'
urlpatterns = [
    path('products/', ProductIndexView.as_view(), name='index'),
    path('product/', ProductCreateView.as_view(), name='product'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='detail'),
    path('product/<int:pk>/edit', ProductEditView.as_view(), name='edit'),
    path('product/<int:pk>/delete', ProductDeleteView.as_view(), name='delete'),
]
