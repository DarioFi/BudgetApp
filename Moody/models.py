from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.postgres.fields import ArrayField
import re

import datetime


def validate(date_text):
    a = datetime.datetime.strptime(date_text, '%Y-%m-%d')
    return str(a.date())


class moody_record(models.Model):
    data = ArrayField(models.CharField(max_length=15), null=True, blank=True)
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="moody_user"
    )

    def add_data_safe(self, datetime_str: str, value: int):
        """
        This function add a line to the records of moody but it checks if the datetime is valid
         (between 2000 and with a valid month/day) and if value is good.
         It does not check the type of datetime and value
        @param datetime_str: date in format YYYY-MM-DD
        @param value: number between 0 and 100 (inclusive)
        @return: Tuple with (status code (HTTP MODE, MESSAGE)
        """
        # todo: check for uniqueness
        # date validation
        try:
            datetime_str = validate(datetime_str)
        except ValueError:
            return 500, "Bad date"

        if 0 > value or value > 100 or not isinstance(value, int):
            return 500, "Bad value"

        self.data.append(str(datetime_str) + "." + str(value))
        self.save()
        return 200, "OK"

    def get_data_as_dictionary(self, date_init=None, date_end=None):  # todo: add args for filtering
        r = []
        for j in self.data:
            x = j.split(".")
            if date_init is None or x[0] >= date_init and (date_end is None or x[0] <= date_end):
                r.append({
                    'datetime': x[0],
                    'value': x[1]
                })

        return {'data': r}

    def delete_data(self, day):
        raise NotImplementedError()
