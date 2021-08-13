from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from product.models import Product, Category


class TestProductIndexView(TestCase):
    """Test ProductIndexView"""

    def setUp(self):
        print("# {} is running!".format(self.id()))
        self.user = get_user_model().objects.create_user(
            email='admin@example.com',
            password='password',
            is_active=True)
        call_command('loaddata', 'categories', verbosity=0)
        call_command('loaddata', 'products', verbosity=0)

    def tearDown(self):
        print("# {} is finished!".format(self.id()))

    def test_get_success(self):
        """
        Get /products/
        Template: /product/index.html
        """
        self.client.login(email=self.user.email, password='password')
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/index.html')

