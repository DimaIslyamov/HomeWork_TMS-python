from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Event, Category
from .forms import EventForm


def build_query_string(request, **updates):
    query_params = request.GET.copy()
    query_params.pop("page", None)

    for key, value in updates.items():
        query_params.pop(key, None)
        if value:
            query_params[key] = value

    return query_params.urlencode()


@login_required
@require_POST
def join_event(request, pk):
    event = get_object_or_404(
        Event,
        pk=pk,
        is_published=True,
    )

    if request.user == event.organizer:
        return redirect(event.get_absolute_url())
    
    event.participants.add(request.user)

    return redirect(event.get_absolute_url())


@login_required
@require_POST
def leave_event(request, pk):
    event = get_object_or_404(
        Event,
        pk=pk,
        is_published=True,
    )

    event.participants.remove(request.user)

    return redirect(event.get_absolute_url())


class EventListView(ListView):
    model = Event
    template_name = "events/event_list.html"
    context_object_name = "events"
    paginate_by = 5

    def get_queryset(self):
        queryset = Event.objects.filter(
            is_published=True
        ).select_related(
            "category",
            "organizer"
        )

        category_id = self.kwargs.get("category_id")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("category_id")

        context["page_title"] = "All Events"
        context["events_count"] = context["paginator"].count
        context["categories"] = Category.objects.all()
        context["query"] = self.request.GET.get("q", "")
        context["pagination_query"] = build_query_string(self.request)

        if category_id:
            context["category"] = get_object_or_404(
                Category,
                pk=category_id,
            )

        return context


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "events/event_form.html"

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        if self.object.is_published:
            return self.object.get_absolute_url()

        return reverse("events:event_list")


class EventDetailView(DetailView):
    model = Event
    context_object_name = "event"

    def get_queryset(self):
        return Event.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["is_participant"] = False

        if self.request.user.is_authenticated:
            context["is_participant"] = self.object.participants.filter(
                pk=self.request.user.pk
            ).exists()

        return context


class EventUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    model = Event
    form_class = EventForm
    template_name = "events/event_form.html"

    def test_func(self):
        event = self.get_object()
        return event.organizer == self.request.user

    def get_success_url(self):
        if self.object.is_published:
            return self.object.get_absolute_url()

        return reverse("events:event_list")


class EventDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView,
):
    model = Event
    template_name = "events/event_confirm_delete.html"
    success_url = reverse_lazy("events:event_list")

    def test_func(self):
        event = self.get_object()
        return event.organizer == self.request.user


# ========= MyEventListView ====================

class MyEventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "events/my_event_list.html"
    context_object_name = "events"
    paginate_by = 5

    def get_queryset(self):
        queryset = Event.objects.filter(
            organizer=self.request.user
        ).select_related(
            "category",
            "organizer",
        )

        status = self.request.GET.get("status")
        query = self.request.GET.get("q")

        if status == "published":
            queryset = queryset.filter(is_published=True)
        elif status == "draft":
            queryset = queryset.filter(is_published=False)

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["query"] = self.request.GET.get("q", "")
        current_status = self.request.GET.get("status", "all")
        if current_status not in ("published", "draft"):
            current_status = "all"

        context["current_status"] = current_status
        context["pagination_query"] = build_query_string(self.request)
        context["all_query"] = build_query_string(
            self.request,
            status="",
        )
        context["published_query"] = build_query_string(
            self.request,
            status="published",
        )
        context["draft_query"] = build_query_string(
            self.request,
            status="draft",
        )

        return context


class MyRegistrationListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "events/my_registration_list.html"
    context_object_name = "events"

    def get_queryset(self):
        return self.request.user.participated_events.filter(
            is_published=True
        ).select_related(
            "category",
            "organizer",
        )