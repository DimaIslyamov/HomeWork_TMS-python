from django.urls import path

from posts import views


app_name = 'posts'

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("create/", views.PostCreateView.as_view(), name="post_create"),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("<int:pk>/update/", views.PostUpdateView.as_view(), name="post_update"),
    path("<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
]
