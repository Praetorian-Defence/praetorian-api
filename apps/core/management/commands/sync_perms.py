from django.contrib.auth.models import Permission, Group
from django.core.management import BaseCommand, call_command

from apps.core.roles import Temporary


class Command(BaseCommand):
    help = 'Generating permissions for existing users.'

    def handle(self, *args, **options):
        call_command('sync_roles')
        self.stdout.write(
            self.style.SUCCESS(
                'Successfully synchronized roles.'
            )
        )

        temporary_permissions = Temporary.available_permissions
        permissions = Permission.objects.all()

        try:
            temporary_group = Group.objects.get(name='temporary')
            temporary_group.permissions.clear()
            temporary_group.save()
        except Group.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    'Temporary group does not exist.'
                )
            )
            return 1

        for key, value in temporary_permissions.items():
            if value is True:
                try:
                    temporary_group.permissions.add(permissions.get(codename=key))
                    temporary_group.save()
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Permission "{key}" specified in temporary role does not exist. '
                        )
                    )
                    return 1

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully synchronized group permissions.'
            )
        )
        return 0
