from django.core.mail import send_mail
from django.utils import timezone
from .models import Mailing, MailingAttempt

def send_mailing(mailing_id):
    mailing = Mailing.objects.get(id=mailing_id)
    now = timezone.now()

    if mailing.status == 'created':
        mailing.status = 'running'
        mailing.start_datetime = now
        mailing.save()

    if mailing.end_datetime and now > mailing.end_datetime:
        mailing.status = 'finished'
        mailing.save()
        return

    for client in mailing.clients.all():
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=None,
                recipient_list=[client.email],
                fail_silently=False,
            )
            status = 'success'
            server_response = 'OK'
        except Exception as e:
            status = 'failed'
            server_response = str(e)

        MailingAttempt.objects.create(
            mailing=mailing,
            client=client,
            status=status,
            server_response=server_response,
        )

    if mailing.end_datetime and timezone.now() > mailing.end_datetime:
        mailing.status = 'finished'
        mailing.save()
