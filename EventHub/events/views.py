from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Event, Category


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

        if category_id:
            context["category"] = get_object_or_404(
                Category,
                pk=category_id,
            )

        return context


def event_about(request):
    return render(request, "events/event_about.html")


class EventDetailView(DetailView):
    model = Event
    context_object_name = "event"

    def get_queryset(self):
        return Event.objects.filter(is_published=True)
