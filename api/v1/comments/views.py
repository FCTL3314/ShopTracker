from django.db.models import QuerySet
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet

from api.v1.comments.models import Comment
from api.v1.comments.paginators import CommentPageNumberPagination
from api.v1.comments.serializers import CommentSerializer, CommentReadSerializer


class CommentViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    model = Comment
    serializer_class = CommentSerializer
    pagination_class = CommentPageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self) -> QuerySet[Comment]:
        queryset = self.model.objects.newest()
        if self.action != "list":
            return queryset
        queryset = queryset.filter(
            content_type__model=self.request.query_params.get("content_type")
        )
        if parent_id := self.request.query_params.get("parent_id"):
            return queryset.filter(parent_id=parent_id)
        return queryset.top_level()

    def list(self, request, *args, **kwargs) -> Response:
        CommentReadSerializer(data=request.query_params).is_valid(raise_exception=True)
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(author=self.request.user)

    def perform_update(self, serializer: Serializer) -> None:
        serializer.save(edited=True)
