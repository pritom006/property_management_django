from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from property.models import Accommodation


class Command(BaseCommand):
    help = "Create the Property Owners group and assign permissions"

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Property Owners")
        if created:
            self.stdout.write("Created Property Owners group.")
        else:
            self.stdout.write("Property Owners group already exists.")

        content_type = ContentType.objects.get_for_model(Accommodation)

        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=["view_accommodation",
                          "add_accommodation", "change_accommodation"]
        )
        group.permissions.set(permissions)

        self.stdout.write("Assigned permissions to Property Owners group.")
