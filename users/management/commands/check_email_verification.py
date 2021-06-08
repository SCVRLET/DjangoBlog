from django.core.management.base import BaseCommand, CommandError
from users.models import User


class Command(BaseCommand):
    help = 'Checking users without e-mail verification'

    def handle(self, *args, **options):
        users_without_verification = User.objects.filter(is_email_verified=False)

        for user in users_without_verification:
            print(user.id, user.login, user.email, user.is_email_verified)