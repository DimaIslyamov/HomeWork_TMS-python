from django import forms

from .models import Event


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