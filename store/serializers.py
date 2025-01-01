from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from store.models import Book, UserBookRelation


class BookReadersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')



class BooksSerializer(ModelSerializer):
    # likes_count = serializers.SerializerMethodField()
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    final_price = serializers.DecimalField(max_digits=7, decimal_places=2, read_only=True)
    owner_name = serializers.CharField(read_only=True)
    readers = BookReadersSerializer(many=True, read_only=True)


    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'discount', 'author', 'annotated_likes', 'rating', 'final_price', 'owner_name', 'readers')

    # def get_likes_count(self, instance):
    #     return UserBookRelation.objects.filter(book=instance, like=True).count()

class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        exclude = ['user']