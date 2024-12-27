import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from faker import Faker
import random
from watchlist_app.models import WatchList, StreamPlatform


def seed_watchlist(n):
    fake = Faker()

    platforms = list(StreamPlatform.objects.all())

    for _ in range(n):
        WatchList.objects.create(
            title=fake.name(),
            storyline=fake.text(max_nb_chars=120),
            platform=random.choice(platforms),
            active=random.choice([True, False]),
            avg_rating=random.randint(1, 5),
            number_rating=random.randint(1, 50)
        )


seed_watchlist(200)