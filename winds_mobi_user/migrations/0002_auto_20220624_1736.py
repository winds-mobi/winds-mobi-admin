import logging

from django.conf import settings
from django.db import migrations
from pymongo import MongoClient, uri_parser

log = logging.getLogger(__name__)


def migrate_user_profiles(apps, schema_editor):
    if hasattr(settings, "MONGODB_URL") and settings.MONGODB_URL:
        uri = uri_parser.parse_uri(settings.MONGODB_URL)
        mongo_client = MongoClient(uri["nodelist"][0][0], uri["nodelist"][0][1])
        mongo_db = mongo_client[uri["database"]]

        User = apps.get_model("auth", "User")
        SocialAuth = apps.get_model("winds_mobi_user", "SocialAuth")
        Profile = apps.get_model("winds_mobi_user", "Profile")

        for user in User.objects.all():
            profile = mongo_db.users.find_one(user.username)
            if profile:
                provider, provider_id = user.username.split("-")
                SocialAuth.objects.get_or_create(
                    user=user, provider=provider, provider_id=provider_id, defaults={"data": profile["user-info"]}
                )
                if "favorites" in profile and profile["favorites"]:
                    Profile.objects.get_or_create(user=user, defaults={"data": {"favorites": profile["favorites"]}})
            else:
                log.warning(f"No profile found for user '{user.username}' in mongodb")


class Migration(migrations.Migration):
    dependencies = [
        ("winds_mobi_user", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(migrate_user_profiles),
    ]
