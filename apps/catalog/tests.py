from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.models import CustomUser
from apps.catalog.models import Category, Publisher, Book

class CatalogGuestRestrictionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='student1', email='student1@example.com', password='password123', role='student'
        )
        self.category = Category.objects.create(name='IT')
        self.publisher = Publisher.objects.create(name='NXB KHKT')
        self.book = Book.objects.create(
            title='Django Web', category=self.category, publisher=self.publisher, isbn='9781234567890'
        )

    def test_guest_cannot_access_book_list(self):
        """Edge case: Guest chưa đăng nhập bị chuyển hướng khi truy cập danh sách sách."""
        url = reverse('catalog:book_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_guest_cannot_access_book_detail(self):
        """Edge case: Guest chưa đăng nhập bị chuyển hướng khi xem chi tiết sách."""
        url = reverse('catalog:book_detail', args=[self.book.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_guest_cannot_access_book_search(self):
        """Edge case: Guest chưa đăng nhập bị chuyển hướng khi tra cứu sách."""
        url = reverse('catalog:book_search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_logged_in_user_can_access_catalog(self):
        """Happy case: User đã đăng nhập truy cập thành công tra cứu sách."""
        self.client.login(username='student1@example.com', password='password123')
        url = reverse('catalog:book_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Web')
