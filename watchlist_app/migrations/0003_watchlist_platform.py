# Generated by Django 4.2 on 2024-11-25 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0002_streamplatform_watchlist_delete_movie'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='platform',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='watchlists', to='watchlist_app.streamplatform'),
            preserve_default=False,
        ),
    ]
