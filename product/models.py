from django.db import models
from django.core.validators import MinValueValidator


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='category name')
    description = models.TextField(verbose_name='category description')
    major_category_name = models.CharField(max_length=255, verbose_name='major category name')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'category'


class Product(models.Model):

    name = models.CharField(max_length=255, verbose_name='product name')
    description = models.TextField(verbose_name='product description')
    price = models.IntegerField(validators=[MinValueValidator(limit_value=0)], verbose_name='product price')
    category = models.ForeignKey(Category, null=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
