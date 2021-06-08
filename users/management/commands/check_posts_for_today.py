from django.core.management.base import BaseCommand, CommandError

from users.models import User

import datetime


class Command(BaseCommand):
    help = 'Checking posts made today'

    def handle(self, *args, **options):
        today_posts = User.objects.filter(created_at=datetime.date.today().strftime("%Y-%m-%d"))

        print(today_posts.count())