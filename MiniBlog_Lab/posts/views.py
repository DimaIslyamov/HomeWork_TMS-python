"""Views for the posts application."""

from django.views.generic import ListView, DetailView

from posts.models import Post


class PostListView(ListView):
    """Display the list of posts."""

    model = Post
    context_object_name = 'posts'


class PostDetailView(DetailView):
    """Display one post."""

    model = Post
    context_object_name = 'post'
