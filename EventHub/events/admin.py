from django.contrib import admin

from events.models import Category, Event


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    search_fields = ("title",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "category",
        "organizer",
        "is_published",
        "created_at",
    )
    list_filter = (
        "is_published",
        "category",
        "created_at",
    )
    search_fields = (
        "title",
        "description",
    )
    prepopulated_fields = {
        "slug": ("title",),
    }
    ordering = ("-created_at",)
    list_editable = ("is_published",)
