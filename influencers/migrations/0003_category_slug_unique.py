from django.db import migrations, models
from django.utils.text import slugify

def generate_unique_slugs(apps, schema_editor):
    Category = apps.get_model('influencers', 'Category')
    for category in Category.objects.all():
        base_slug = slugify(category.name)
        slug = base_slug
        counter = 1
        while Category.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        category.slug = slug
        category.save()

class Migration(migrations.Migration):
    dependencies = [
        ('influencers', '0002_category_slug'),
    ]

    operations = [
        migrations.RunPython(generate_unique_slugs),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ] 