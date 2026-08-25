from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Event, Category
from .forms import EventForm


class EventListView(ListView):
    model = Event
    context_object_name = "events"

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

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("category_id")

        context["page_title"] = "All Events"
        context["events_count"] = context["events"].count()
        context["categories"] = Category.objects.all()

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


def event_about(request):
    return render(request, "events/event_about.html")


# ========= MyEventListView ====================

class MyEventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "events/my_event_list.html"
    context_object_name = "events"

    def get_queryset(self):
        queryset = Event.objects.filter(
            organizer=self.request.user
        ).select_related(
            "category",
            "organizer",
        )

        status = self.request.GET.get("status")

        if status == "published":
            queryset = queryset.filter(is_published=True)
        elif status == "draft":
            queryset = queryset.filter(is_published=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_status"] = (
            self.request.GET.get(
                "status",
                "all"
            )
        )
        return context