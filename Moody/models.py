from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.postgres.fields import ArrayField


class moody_record(models.Model):
    data = ArrayField(models.CharField(max_length=15), null=True, blank=True)
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="moody_user"
    )

    def add_data(self, datetime, value):
        self.data.append(str(datetime) + " " + str(value))
        self.save()
