# Generated by Django 4.2 on 2024-12-30 01:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0006_watchlist_avg_rating_watchlist_number_rating'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='watchlist',
            options={'ordering': ['-id']},
        ),
    ]
