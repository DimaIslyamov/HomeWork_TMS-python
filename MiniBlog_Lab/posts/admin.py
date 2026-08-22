from django.contrib import admin
from .models import Post, Category, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin configuration for Post model."""

    # ---------- List page ----------
    list_display = (
        "id",
        "title",
        "is_published",
        "created_at",
    )

    list_display_links = (
        "id",
        "title",
    )

    list_filter = (
        "is_published",
        "created_at",
    )

    search_fields = (
        "title",
    )

    ordering = (
        "-created_at",
    )

    list_editable = (
        "is_published",
    )

    # ---------- Edit page ----------
    readonly_fields = (
        "created_at",
        "updated_at",
    )


admin.site.register(Category)
admin.site.register(Tag)
