from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from apps.accounts.models import CustomUser
from apps.catalog.models import Category, Publisher, Book
from apps.circulation.models import BorrowRecord, Reservation

class CirculationTrustModelTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = CustomUser.objects.create_user(
            username='student1', email='student1@example.com', password='password123', role='student'
        )
        self.librarian = CustomUser.objects.create_user(
            username='lib1', email='lib1@example.com', password='password123', role='librarian'
        )
        self.category = Category.objects.create(name='IT')
        self.publisher = Publisher.objects.create(name='NXB KHKT')
        self.book1 = Book.objects.create(
            title='Django Web', category=self.category, publisher=self.publisher, isbn='9781111111111', available_copies=2
        )
        self.book2 = Book.objects.create(
            title='Python Pro', category=self.category, publisher=self.publisher, isbn='9782222222222', available_copies=1
        )

    def test_overdue_record_locks_user_borrow_permission(self):
        """Edge case (Negative): Khi sách chuyển trạng thái overdue/lost, tài khoản tự động bị khóa can_borrow=False."""
        record = BorrowRecord.objects.create(
            user=self.student,
            book=self.book1,
            borrow_date=timezone.now() - timedelta(days=20),
            due_date=timezone.now() - timedelta(days=5),
            status='borrowed'
        )
        # Khi save hoặc xử lý trả muộn -> trạng thái thành overdue
        record.status = 'overdue'
        record.save()
        
        self.student.refresh_from_db()
        self.assertFalse(self.student.can_borrow)

    def test_locked_user_cannot_create_reservation(self):
        """Edge case: Độc giả đang bị khóa mượn (do vi phạm tín nhiệm) không được đặt trước tài liệu (BR-13)."""
        self.student.can_borrow = False
        self.student.save()
        
        self.client.login(username='student1@example.com', password='password123')
        url = reverse('circulation:reserve_book', args=[self.book2.pk])
        response = self.client.post(url)
        
        # Bị từ chối hoặc redirect với lỗi
        self.assertEqual(Reservation.objects.filter(user=self.student, book=self.book2).count(), 0)

    def test_resolve_violation_restores_borrow_permission(self):
        """Happy case: Thủ thư gỡ vi phạm thành công giúp khôi phục quyền mượn cho độc giả."""
        record = BorrowRecord.objects.create(
            user=self.student,
            book=self.book1,
            borrow_date=timezone.now() - timedelta(days=20),
            due_date=timezone.now() - timedelta(days=5),
            status='overdue'
        )
        self.student.can_borrow = False
        self.student.save()
        
        self.client.login(username='lib1@example.com', password='password123')
        url = reverse('circulation:resolve_violation', args=[record.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        
        record.refresh_from_db()
        self.student.refresh_from_db()
        self.assertEqual(record.status, 'returned')
        self.assertTrue(self.student.can_borrow)
