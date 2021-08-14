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
        self.assertEqual(response.context['products'][0].name, 'ほげほげ')
        self.assertEqual(response.context['products'][0].description, 'ビジネス')
        self.assertEqual(response.context['products'][0].price, 1000)
        self.assertTrue(len(response.context['categories']) > 0)
        self.assertTemplateUsed(response, 'product/index.html')


class TestProductCreateView(TestCase):
    """Test ProductCreateView"""

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

    def test_get_product_new(self):
        """
        Get /product/
        Template: /product/new.html
        """
        self.client.login(email=self.user.email, password='password')
        response = self.client.get('/product/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/new.html')

    def test_post_product_new(self):
        """
        Post /product/
        Template: /product/new.html
        """
        self.client.login(email=self.user.email, password='password')
        response = self.client.post('/product/', {
            'name': 'name1',
            'description': 'description1',
            'price': 10,
            'category_id': 1,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/products/')


class TestProductDetailView(TestCase):
    """Test ProductDetailView"""

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

    def test_get_detail(self):
        """
        Get /product/1
        Template: /product/new.html
        """
        self.client.login(email=self.user.email, password='password')
        response = self.client.get('/product/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/show.html')


class TestProductEditView(TestCase):
    """Test ProductEditView"""

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

    def test_get_product_update(self):
        """
        Get /product/1/edit
        Template: /product/edit.html
        """
        self.client.login(email=self.user.email, password='password')
        response = self.client.get('/product/1/edit')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/edit.html')

    def test_post_product_update(self):
        """
        Post /product/1/edit
        """
        self.client.login(email=self.user.email, password='password')
        response = self.client.post('/product/1/edit', {
            'name': 'name1',
            'description': 'description1',
            'price': 10,
            'category_id': 1,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/products/')


class TestProductDeleteView(TestCase):
    """Test ProductDeleteView"""

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

    def test_delete_product(self):
        """
        Post /product/1/delete
        """
        self.client.login(email=self.user.email, password='password')
        response = self.client.post('/product/1/delete')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/products/')
