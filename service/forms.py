from django import forms

from .models import Client, Mailing, Message


class ClientForm(forms.ModelForm):
    """Форма для создания и редактирования клиента."""

    class Meta:
        model = Client
        fields = ["email", "full_name", "comment"]


class MessageForm(forms.ModelForm):
    """Форма для создания и редактирования сообщения."""

    class Meta:
        model = Message
        fields = ["subject", "body"]


class MailingForm(forms.ModelForm):
    """Форма для создания и редактирования рассылки."""

    class Meta:
        model = Mailing
        fields = [
            "start_datetime",
            "end_datetime",
            "status",
            "message",
            "clients",
        ]
        widgets = {
            "clients": forms.CheckboxSelectMultiple(),
            "status": forms.Select(),
            "start_datetime": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local"}),
            "end_datetime": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local"}),
        }
