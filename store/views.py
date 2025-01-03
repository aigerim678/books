from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg, ExpressionWrapper, DecimalField, F, Prefetch
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from store.models import Book, UserBookRelation
from store.permissions import IsOwnerOrStaffOrReadOnly
from store.serializers import BooksSerializer, UserBookRelationSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all().annotate(annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
                                           final_price=ExpressionWrapper(
                                               F('price') - (F('price') * F('discount') / 100),
                                               output_field=DecimalField(max_digits=7, decimal_places=2)),
                                           owner_name=F('owner__username')
                                           ).prefetch_related(Prefetch('readers', queryset=User.objects.all().only('first_name', 'last_name'))).order_by('id')
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filterset_fields = ['price']
    search_fields = ['name', 'author']
    ordering_fields = ['price', 'author']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


def auth(request):
    return render(request, 'oauth.html')


class UserBookRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = 'book'

    def get_object(self):
        obj, _ = UserBookRelation.objects.get_or_create(user=self.request.user, book_id=self.kwargs['book'])
        return obj



