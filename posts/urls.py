from django.urls import path
from .views import (
    PostListView,
    PostCreateView,
    PostDetailView,
    CommentListView,
    CommentCreateView,
    CommentDetailView,
)

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/create/", PostCreateView.as_view(), name="post-create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("comments/", CommentListView.as_view(), name="comment-list"),
    path("comments/create/", CommentCreateView.as_view(), name="comment-create"),
    path("comments/<int:pk>/", CommentDetailView.as_view(), name="comment-detail"),
]
