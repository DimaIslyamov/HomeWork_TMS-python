from django.urls import path

from posts import views
from posts.views import CommentDeleteView

app_name = 'posts'

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("create/", views.PostCreateView.as_view(), name="post_create"),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("<slug:slug>/update/", views.PostUpdateView.as_view(), name="post_update"),
    path("<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
    path(
        "comments/<int:pk>/delete/",
        CommentDeleteView.as_view(),
        name="comment_delete",
    ),
]
