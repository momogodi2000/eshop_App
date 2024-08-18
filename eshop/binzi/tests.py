from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from .models import Product, Sale, Message, Category, Catalog
from .forms import ProductForm, GeneralSettingsForm

class TestEndpoints(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password=make_password('testpassword'),
        )
        self.client.force_login(self.user)
        self.category = Category.objects.create(name='Test Category')
        self.catalog = Catalog.objects.create(name='Test Catalog')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            quantity=10,
            max_quantity=20,
            min_quantity=5,
            price=10.00,
            category=self.category,
            catalog=self.catalog,
        )
        self.sale = Sale.objects.create(
            product=self.product,
            quantity=5,
            sale_date=timezone.now(),
        )
        self.message = Message.objects.create(
            sender=self.user,
            content='Test Message',
        )

    def test_homepage(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_contact(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_product_browsing(self):
        response = self.client.get(reverse('product_browsing'))
        self.assertEqual(response.status_code, 200)

    def test_product_details(self):
        response = self.client.get(reverse('product_details', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart(self):
        response = self.client.post(reverse('add_to_cart', args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)

    def test_remove_from_cart(self):
        response = self.client.post(reverse('remove_from_cart', args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)

    def test_view_cart(self):
        response = self.client.get(reverse('view_cart'))
        self.assertEqual(response.status_code, 200)

    def test_checkout(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)

    def test_place_order(self):
        response = self.client.post(reverse('place_order'))
        self.assertEqual(response.status_code, 302)

