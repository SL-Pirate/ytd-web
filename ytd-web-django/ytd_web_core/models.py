from collections.abc import Iterable
from django.db import models
from ytd_web_core import keep_time
from ytd_web_core.celery import clean_func
from sequences import get_next_value

class Downloadable(models.Model):
    id = models.IntegerField(primary_key=True)
    path = models.TextField()
    name = models.TextField()
    folder = models.TextField()
    expiration_period = models.IntegerField(default=keep_time)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ) -> None:
        self.id = get_next_value("downloadable_id", reset_value=2000000000);
        super().save(force_insert, force_update, using, update_fields)


    def initInvalidation(self) -> None:
        clean_func.delay(self.folder, self.id)
