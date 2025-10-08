from django.contrib import admin

from .models import Client, Mailing, MailingAttempt, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Админка для модели Client."""

    list_display = ("email", "full_name")
    search_fields = ("email", "full_name")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Админка для модели Message."""

    list_display = ("subject",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """Админка для модели Mailing."""

    list_display = (
        "id",
        "status",
        "start_datetime",
        "end_datetime",
        "message",
    )
    list_filter = ("status",)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    """Админка для модели MailingAttempt."""

    list_display = ("mailing", "client", "attempt_datetime", "status")
    list_filter = ("status",)
