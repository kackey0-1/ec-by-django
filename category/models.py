from django.db import models
from django.utils import timezone


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='category name')
    description = models.TextField(verbose_name='category description')
    major_category_name = models.CharField(max_length=255, verbose_name='major category name')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'category'
