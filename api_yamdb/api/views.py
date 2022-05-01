from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework import viewsets, permissions, status
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound

from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment,
)
from users.models import User
from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsModeratorOrReadOnly,
    IsUserOrStaff,
)
from .serializers import (
    CategorieSerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer,
    UserSerializer,
)


class UsersViewSet(viewsets.ModelViewSet):
    """Вьюсет для пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAdmin,
    ]
    pagination_class = PageNumberPagination
    search_fields = ('user__username')

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=request)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['get', 'patch', ])
    def me(self, request):
        user = User.objects.get(id=request.user.id)
        if request.method == 'patch':
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TargetUserViewSet(viewsets.ModelViewSet):
    """Тестовый вьюсет, нужно будет удалить."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    pagination_class = PageNumberPagination
    search_fields = ('user__username')

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=request)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @action(detail=True, url_path='me')
    def get_me(self, request):
        user = User.objects.get(id=request.user.id)
        if request.method == 'patch':
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [
        IsAdminOrReadOnly,
    ]
    pagination_class = LimitOffsetPagination
    search_fields = ('category__slug')


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [
        IsAdminOrReadOnly,
    ]
    pagination_class = PageNumberPagination
    search_fields = ('genre__slug')


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для заголовков."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [
        IsAdminOrReadOnly,
    ]
    pagination_class = PageNumberPagination


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для ревью."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAdminOrReadOnly,
        IsModeratorOrReadOnly,
    ]


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""

    serializer_class = CommentSerializer
    permission_classes = [
        IsUserOrStaff,
    ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        if not title.reviews.filter(id=review_id).exists():
            raise NotFound()
        return review.comments.filter(review__title_id=title_id)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
