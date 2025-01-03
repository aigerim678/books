from django.contrib.auth.models import User
from django.db.models import When, Case, Count, Avg, ExpressionWrapper, F, DecimalField
from django.test import TestCase

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username='user1', first_name='', last_name='')
        user2 = User.objects.create(username='user2', first_name='', last_name='')
        user3 = User.objects.create(username='user3', first_name='', last_name='')

        book_1 = Book.objects.create(name='Test book 1', price=25, author='Test author 1', discount=10, owner=user1)
        book_2 = Book.objects.create(name='Test book 2', price=55, author='Test author 2', owner=user2)

        UserBookRelation.objects.create(user=user1, book=book_1, like=True, rate=3)
        UserBookRelation.objects.create(user=user2, book=book_1, like=True, rate=4)
        user_book_3 = UserBookRelation.objects.create(user=user3, book=book_1, like=True)
        user_book_3.rate = 4
        user_book_3.save()

        UserBookRelation.objects.create(user=user1, book=book_2, like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=book_2, like=True)
        UserBookRelation.objects.create(user=user3, book=book_2, like=True)

        books = Book.objects.all().annotate(annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
                                            final_price=ExpressionWrapper(F('price') - (F('price') * F('discount') / 100), output_field=DecimalField(max_digits=7, decimal_places=2)), owner_name=F('owner__username')
                                            ).order_by('id')

        data = BooksSerializer(books, many=True).data
        expected_data = [
            {'id': book_1.id,
             'name': 'Test book 1',
             'price': '25.00',
             'discount': '10.00',
             'author':'Test author 1',
             'annotated_likes': 3,
             'rating': '3.50',
             'final_price': '22.50',
             'owner_name': 'user1',
             'readers': [{
                 'first_name': '',
                 'last_name': ''
             },
                 {
                     'first_name': '',
                     'last_name': ''
                 },
                 {
                     'first_name': '',
                     'last_name': ''
                 }
             ]},
            {'id': book_2.id,
             'name': 'Test book 2',
             'price': '55.00',
             'discount': '0.00',
             'author':'Test author 2',
             'annotated_likes': 3,
             'rating': '5.00',
             'final_price': '55.00',
             'owner_name': 'user2',
             'readers': [{
                 'first_name': '',
                 'last_name': ''
             },
                 {
                     'first_name': '',
                     'last_name': ''
                 },
                 {
                     'first_name': '',
                     'last_name': ''
                 }
             ]}]
        self.assertEqual(expected_data, data)



