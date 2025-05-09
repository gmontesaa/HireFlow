# Generated by Django 4.2.7 on 2025-04-04 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('influencers', '0002_campaign_campaigninfluencer_influencer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='influencers',
            field=models.ManyToManyField(through='influencers.CampaignInfluencer', to='influencers.influencer'),
        ),
        migrations.AlterField(
            model_name='influencer',
            name='category',
            field=models.CharField(choices=[('fashion', 'Moda'), ('beauty', 'Belleza'), ('fitness', 'Fitness'), ('food', 'Comida'), ('travel', 'Viajes'), ('tech', 'Tecnología'), ('lifestyle', 'Estilo de Vida')], default='lifestyle', max_length=20),
        ),
        migrations.AlterField(
            model_name='influencer',
            name='platform',
            field=models.CharField(choices=[('instagram', 'Instagram'), ('youtube', 'YouTube'), ('tiktok', 'TikTok')], default='instagram', max_length=20),
        ),
        migrations.AlterField(
            model_name='influencer',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
    ]
