from django.urls import path

from posts import views

app_name = 'posts'

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path(
        "tag/<int:tag_id>/",
        views.PostListView.as_view(),
        name="post_list_by_tag",
    ),
    path("create/", views.PostCreateView.as_view(), name="post_create"),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("<slug:slug>/update/", views.PostUpdateView.as_view(), name="post_update"),
    path("<slug:slug>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
    path(
        "comments/<int:pk>/delete/",
        views.CommentDeleteView.as_view(),
        name="comment_delete",
    ),
]
