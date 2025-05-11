from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('influencers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=100, null=True),
        ),
    ] 