"""Views for the posts application."""

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView, UpdateView, DeleteView,
)

from posts.forms import PostForm, CommentForm
from posts.models import Post, Comment, Tag


class PostListView(ListView):
    """Display the list of posts."""

    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = (
            Post.objects
            .filter(is_published=True)
            .select_related('author', 'category')
            .prefetch_related('tags')
            .order_by('-created_at')
        )

        tag_id = self.kwargs.get('tag_id')

        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(
            object_list=object_list,
            **kwargs,
        )

        context['page_title'] = 'Все публикации'

        tag_id = self.kwargs.get('tag_id')

        if tag_id:
            context['current_tag'] = get_object_or_404(
                Tag,
                pk=tag_id,
            )
        return context


class PostDetailView(DetailView):
    """Display one post."""

    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return (
            Post.objects
            .filter(is_published=True)
            .select_related('author', 'category')
            .prefetch_related(
                'tags',
                'comments__author',
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())

        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()

            return redirect(self.object.get_absolute_url())

        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a new post."""

    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('posts:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    """Update a post."""

    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView
):
    """Delete a post."""

    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts:post_list')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'posts/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return self.object.post.get_absolute_url()
