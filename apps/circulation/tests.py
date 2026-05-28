from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from apps.catalog.models import Author, Book, Category, Publisher

from .models import BorrowRecord, Reservation


class CirculationModelRelationshipTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='reader',
            password='StrongPass123',
        )
        self.librarian = get_user_model().objects.create_user(
            username='librarian',
            password='StrongPass123',
            role='librarian',
        )
        category = Category.objects.create(name='Van hoc Viet Nam')
        publisher = Publisher.objects.create(name='NXB Tre')
        author = Author.objects.create(name='Nam Cao')
        self.book = Book.objects.create(
            title='Chi Pheo',
            isbn='1234567890124',
            category=category,
            publisher=publisher,
            publication_year=1941,
            description='Truyen ngan hien thuc.',
            total_copies=9,
            available_copies=9,
        )
        self.book.authors.add(author)

    def test_borrow_record_foreign_keys_and_reverse_relations(self):
        borrow = BorrowRecord.objects.create(
            user=self.user,
            book=self.book,
            due_date=timezone.now() + timedelta(days=14),
            status='approved',
            approved_by=self.librarian,
        )

        self.assertEqual(borrow.user, self.user)
        self.assertEqual(borrow.book, self.book)
        self.assertEqual(borrow.approved_by, self.librarian)
        self.assertIn(borrow, self.user.borrow_records.all())
        self.assertIn(borrow, self.book.borrow_records.all())
        self.assertIn(borrow, self.librarian.approved_borrows.all())
        self.assertFalse(borrow.is_overdue)

    def test_reservation_foreign_keys_and_reverse_relations(self):
        reservation = Reservation.objects.create(
            user=self.user,
            book=self.book,
            expires_at=timezone.now() + timedelta(days=3),
        )

        self.assertEqual(reservation.status, 'active')
        self.assertEqual(reservation.user, self.user)
        self.assertEqual(reservation.book, self.book)
        self.assertIn(reservation, self.user.reservations.all())
        self.assertIn(reservation, self.book.reservations.all())

    def test_borrow_record_detects_overdue_when_borrowed_past_due_date(self):
        borrow = BorrowRecord.objects.create(
            user=self.user,
            book=self.book,
            due_date=timezone.now() - timedelta(days=1),
            status='borrowed',
        )

        self.assertTrue(borrow.is_overdue)
