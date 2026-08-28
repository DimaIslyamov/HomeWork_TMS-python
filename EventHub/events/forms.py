from django import forms
from django.forms import inlineformset_factory

from .models import Event, Session


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "slug",
            "description",
            "category",
            "is_published",
        ]

    def clean_slug(self):
        slug = self.cleaned_data["slug"].strip()

        if not slug:
            raise forms.ValidationError(
                "Slug cannot be empty."
            )

        queryset = Event.objects.filter(slug=slug)

        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise forms.ValidationError(
                "Event with this slug already exists."
            )

        return slug


SessionFormSet = inlineformset_factory(
    Event,
    Session,
    fields=[
        "title",
        "description",
        "start_time",
    ],
    extra=1,
    can_delete=True,
)