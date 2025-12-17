from django.contrib.auth.models import User


def full_name(self):
    return f"{self.first_name} {self.last_name}"


User.add_to_class("__str__", full_name)
