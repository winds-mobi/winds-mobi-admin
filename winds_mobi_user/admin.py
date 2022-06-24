from django.contrib import admin
from django.contrib.admin import display
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db.models import F
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from winds_mobi_user.models import Profile, SocialAuth


@admin.register(SocialAuth)
class SocialAuthAdmin(admin.ModelAdmin):
    list_display = ("id", "provider", "provider_id", "user_url")
    readonly_fields = ("provider", "provider_id", "data")

    @display(description=_("User url"))
    def user_url(self, obj):
        url = reverse("admin:auth_user_change", args=[obj.user.id])
        return format_html(f"<a href='{url}'>{obj.user.username}</a>", url=url)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("username",)
    search_fields = ("data__favorites",)

    @display(description=_("Username"))
    def username(self, obj):
        return obj.user.username


class ProfileInline(admin.StackedInline):
    model = Profile


class SocialAuthInline(admin.StackedInline):
    model = SocialAuth
    extra = 0


class CustomUserAdmin(UserAdmin):
    list_display = list(UserAdmin.list_display) + ["last_login", "date_joined"]
    inlines = (ProfileInline, SocialAuthInline)

    def get_ordering(self, request):
        return (F("last_login").desc(nulls_last=True),)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
