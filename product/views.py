import logging
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from .models import Product
logger = logging.getLogger(__name__)


class ProductIndexView(ListView):
    template_name = 'product/index.html'
    context_object_name = 'products'
    model = Product
    paginate_by = 100

    def get_queryset(self):
        return Product.objects.select_related('category').order_by('-updated_at')


class ProductCreateView(CreateView):
    template_name = 'product/create.html'
    model = Product
    fields = ['name', 'description', 'price']
    success_url = reverse_lazy('product:products')


class ProductDetailView(DetailView):
    template_name = 'product/show.html'
    model = Product


class ProductEditView(UpdateView):
    template_name = 'product/edit.html'
    model = Product
    fields = ['name', 'description', 'price']
    success_url = reverse_lazy('product:products')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('product:products')

