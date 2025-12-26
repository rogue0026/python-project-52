from django.db import models


class Label(models.Model):
    name = models.CharField(verbose_name="Имя")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name