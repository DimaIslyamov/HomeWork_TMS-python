"""Views for the posts application."""

from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView, UpdateView, DeleteView,
)

from posts.forms import PostForm
from posts.models import Post


class PostListView(ListView):
    """Display the list of posts."""

    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(
            is_published=True
        ).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Все публикации'

        return context


class PostDetailView(DetailView):
    """Display one post."""

    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class PostCreateView(CreateView):
    """Create a new post."""

    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('posts:post_list')


class PostUpdateView(UpdateView):
    """Update a post."""

    model = Post
    form_class = PostForm

    def get_success_url(self):
        return reverse(
            'posts:post_detail',
            kwargs={'pk': self.object.pk},
        )


class PostDeleteView(DeleteView):
    """Delete a post."""

    model = Post
    success_url = reverse_lazy('posts:post_list')
