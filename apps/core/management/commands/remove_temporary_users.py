from django.core.management import BaseCommand
from django.utils import timezone

from apps.core.models import User


class Command(BaseCommand):
    help = 'Remove expired temporary users.'

    def handle(self, *args, **options):
        User.objects.filter(is_temporary=True, active_to__lte=timezone.now()).delete()
        self.stdout.write(
            self.style.SUCCESS(
                'Successfully removed all expired temporary users.'
            )
        )
