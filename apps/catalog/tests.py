from django.test import TestCase

from .models import Author, Book, Category, Publisher


class CatalogModelRelationshipTests(TestCase):
    def test_book_relations_with_category_publisher_and_authors(self):
        category = Category.objects.create(name='Van hoc Viet Nam')
        publisher = Publisher.objects.create(name='NXB Tre')
        first_author = Author.objects.create(name='Nguyen Nhat Anh')
        second_author = Author.objects.create(name='Co tac gia')

        book = Book.objects.create(
            title='Mat biec',
            isbn='1234567890123',
            category=category,
            publisher=publisher,
            publication_year=1990,
            description='Tieu thuyet ve tuoi tre va moi tinh don phuong.',
            total_copies=5,
            available_copies=4,
        )
        book.authors.add(first_author, second_author)

        self.assertEqual(book.category, category)
        self.assertEqual(book.publisher, publisher)
        self.assertEqual(book.authors.count(), 2)
        self.assertIn(book, category.books.all())
        self.assertIn(book, publisher.books.all())
        self.assertIn(book, first_author.books.all())
        self.assertTrue(book.is_available)

    def test_book_can_store_cover_and_pdf_paths(self):
        book = Book.objects.create(
            title='Tai lieu PDF',
            cover_image='covers/sample.jpg',
            pdf_file='books_pdf/sample.pdf',
            total_copies=1,
            available_copies=1,
        )

        self.assertEqual(book.cover_image.name, 'covers/sample.jpg')
        self.assertEqual(book.pdf_file.name, 'books_pdf/sample.pdf')
