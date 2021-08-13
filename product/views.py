import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from .models import Product
from category.models import Category
logger = logging.getLogger(__name__)


class ProductIndexView(LoginRequiredMixin, ListView):
    template_name = 'product/index.html'
    context_object_name = 'products'
    model = Product
    # paginate_by = 5

    def get_queryset(self):
        return Product.objects.select_related('category').order_by('-updated_at')

    def get_context_data(self, **kwargs):
        context = super(ProductIndexView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductCreateView(CreateView):
    template_name = 'product/new.html'
    model = Product
    fields = ['name', 'description', 'price']
    success_url = reverse_lazy('product:index')

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.category_id = self.request.POST['category_id']
        return super(ProductCreateView, self).form_valid(form)


class ProductDetailView(LoginRequiredMixin, DetailView):
    template_name = 'product/show.html'
    model = Product


class ProductEditView(LoginRequiredMixin, UpdateView):
    template_name = 'product/edit.html'
    model = Product
    fields = ['name', 'description', 'price']
    success_url = reverse_lazy('product:index')

    def get_context_data(self, **kwargs):
        context = super(ProductEditView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.category_id = self.request.POST['category_id']
        return super(ProductEditView, self).form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('product:index')

