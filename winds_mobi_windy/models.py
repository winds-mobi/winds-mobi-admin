from django.db import models
from django.utils.translation import gettext_lazy as _


class Station(models.Model):
    id = models.CharField(_("Id"), max_length=50, primary_key=True)

    def __str__(self):
        return self.id
