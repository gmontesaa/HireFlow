# Generated by Django 4.2.21 on 2025-05-22 03:51

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('budget', models.DecimalField(decimal_places=2, max_digits=10)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(choices=[('pending', 'Pendiente'), ('active', 'Activa'), ('completed', 'Completada'), ('cancelled', 'Cancelada')], default='pending', max_length=20)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CampaignInfluencer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('status', models.CharField(choices=[('pending_review', 'Pendiente de Revisión'), ('review_approved', 'Revisión Aprobada'), ('review_rejected', 'Revisión Rechazada'), ('message_sent', 'Mensaje Enviado'), ('accepted', 'Aceptado'), ('rejected', 'Rechazado'), ('completed', 'Completado')], default='pending_review', max_length=20)),
                ('review_notes', models.TextField(blank=True, null=True)),
                ('message_sent_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('slug', models.SlugField(default='', max_length=100, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Influencer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='Nombre de usuario')),
                ('platform', models.CharField(choices=[('instagram', 'Instagram'), ('youtube', 'YouTube'), ('tiktok', 'TikTok')], default='instagram', max_length=20, verbose_name='Plataforma')),
                ('followers', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Seguidores')),
                ('engagement_rate', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Tasa de engagement')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('price_per_post', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Precio por publicación')),
                ('contact_email', models.EmailField(max_length=254, verbose_name='Email de contacto')),
                ('instagram_url', models.URLField(blank=True, null=True, verbose_name='URL de Instagram')),
                ('location', models.CharField(blank=True, max_length=100, verbose_name='Ubicación')),
                ('is_available', models.BooleanField(default=True, verbose_name='Disponible')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='Slug')),
                ('categories', models.ManyToManyField(related_name='influencers', to='influencers.category', verbose_name='Categorías')),
            ],
            options={
                'verbose_name': 'Influencer',
                'verbose_name_plural': 'Influencers',
                'ordering': ['-followers'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('rating', models.IntegerField(choices=[(1, '1 estrella'), (2, '2 estrellas'), (3, '3 estrellas'), (4, '4 estrellas'), (5, '5 estrellas')])),
                ('comment', models.TextField()),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='influencers.campaign')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_given', to=settings.AUTH_USER_MODEL)),
                ('influencer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='influencers.influencer')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['name'], name='influencers_name_39ee3b_idx'),
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['slug'], name='influencers_slug_2e99d2_idx'),
        ),
        migrations.AddField(
            model_name='campaigninfluencer',
            name='campaign',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='influencers.campaign'),
        ),
        migrations.AddField(
            model_name='campaigninfluencer',
            name='influencer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='influencers.influencer'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='campaign',
            name='influencers',
            field=models.ManyToManyField(through='influencers.CampaignInfluencer', to='influencers.influencer'),
        ),
        migrations.AddIndex(
            model_name='review',
            index=models.Index(fields=['rating'], name='influencers_rating_f8b28a_idx'),
        ),
        migrations.AddIndex(
            model_name='review',
            index=models.Index(fields=['created_at'], name='influencers_created_dbf3e7_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('campaign', 'influencer', 'company')},
        ),
        migrations.AddIndex(
            model_name='influencer',
            index=models.Index(fields=['username'], name='influencers_usernam_eac8e5_idx'),
        ),
        migrations.AddIndex(
            model_name='influencer',
            index=models.Index(fields=['platform'], name='influencers_platfor_4e69c4_idx'),
        ),
        migrations.AddIndex(
            model_name='influencer',
            index=models.Index(fields=['is_available'], name='influencers_is_avai_846a8c_idx'),
        ),
        migrations.AddIndex(
            model_name='influencer',
            index=models.Index(fields=['followers'], name='influencers_followe_452660_idx'),
        ),
        migrations.AddIndex(
            model_name='influencer',
            index=models.Index(fields=['engagement_rate'], name='influencers_engagem_557e80_idx'),
        ),
        migrations.AddIndex(
            model_name='campaigninfluencer',
            index=models.Index(fields=['status'], name='influencers_status_1aceaf_idx'),
        ),
        migrations.AddIndex(
            model_name='campaigninfluencer',
            index=models.Index(fields=['message_sent_date'], name='influencers_message_9371ee_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='campaigninfluencer',
            unique_together={('campaign', 'influencer')},
        ),
        migrations.AddIndex(
            model_name='campaign',
            index=models.Index(fields=['status'], name='influencers_status_4b10be_idx'),
        ),
        migrations.AddIndex(
            model_name='campaign',
            index=models.Index(fields=['start_date'], name='influencers_start_d_3e700a_idx'),
        ),
        migrations.AddIndex(
            model_name='campaign',
            index=models.Index(fields=['end_date'], name='influencers_end_dat_f060f9_idx'),
        ),
    ]
