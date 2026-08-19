from django.db import migrations
from django.utils.text import slugify


def populate_slugs(apps, schema_editor):
    Post = apps.get_model("posts", "Post")

    for post in Post.objects.all():
        if not post.slug:
            base_slug = slugify(post.title)
            slug = base_slug
            counter = 2

            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            post.slug = slug
            post.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0005_post_slug"),
    ]

    operations = [
        migrations.RunPython(
            populate_slugs,
            migrations.RunPython.noop,
        ),
    ]