from django.test import TestCase

from store.models import Book
from store.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book_1 = Book.objects.create(name='Test book 1', price=25, author='Test author 1')
        book_2 = Book.objects.create(name='Test book 2', price=55, author='Test author 2')
        data = BooksSerializer([book_1, book_2], many=True).data
        expected_data = [{'id': book_1.id, 'name': 'Test book 1', 'price': '25.00', 'author':'Test author 1'}, {'id': book_2.id, 'name': 'Test book 2', 'price': '55.00', 'author':'Test author 2'}]
        self.assertEqual(expected_data, data)



