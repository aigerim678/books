from django.contrib.auth.models import User
from django.db.models.expressions import result
from django.test import TestCase

from store.logic import set_rating
from store.models import Book, UserBookRelation


class SetRatingTestCase(TestCase):

    def setUp(self):
        user1 = User.objects.create(username='user1', first_name='', last_name='')
        user2 = User.objects.create(username='user2', first_name='', last_name='')
        user3 = User.objects.create(username='user3', first_name='', last_name='')

        self.book_1 = Book.objects.create(name='Test book 1', price=25, author='Test author 1', discount=10, owner=user1)

        UserBookRelation.objects.create(user=user1, book=self.book_1, like=True, rate=3)
        UserBookRelation.objects.create(user=user2, book=self.book_1, like=True, rate=4)
        UserBookRelation.objects.create(user=user3, book=self.book_1, like=True)


    def test_ok(self):
        set_rating(self.book_1)
        self.book_1.refresh_from_db()
        self.assertEqual('3.50', str(self.book_1.rating))