from apps.accounts.models import User
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.utils import timezone


class Command(BaseCommand):
    help = "Creates an Admin User"

    def handle(self, *args, **kwargs):
        try:
            print("Creating user <janedoe@gmail.com> ... \n")
            User.objects.create_superuser(
                "janedoe", "janedoe@gmail.com", "janedoe"
            )
        except Exception as e:
            if not type(e) == IntegrityError:
                print(
                    "Something went wrong while"
                    "creating the user: janedoe@gmail.com \n"
                )
                print(e)
        else:
            print("Added user <janedoe@gmail.com> to the database")

        print(User.objects.all().values())
        print("\n")
