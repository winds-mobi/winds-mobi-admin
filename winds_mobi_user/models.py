from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class SocialAuth(models.Model):
    provider = models.CharField(_("Provider"), max_length=50)
    provider_id = models.CharField(_("Provider id"), max_length=50)
    user = models.ForeignKey(get_user_model(), related_name="social_auths", on_delete=models.CASCADE)
    data = models.JSONField(_("Data"))

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["provider", "provider_id"], name="unique_provider_id"),
        ]


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name="profile", on_delete=models.CASCADE)
    data = models.JSONField(_("Data"), default=dict)
