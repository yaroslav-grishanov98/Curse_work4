from django.core.management.base import BaseCommand, CommandError
from service.utils import send_mailing
from service.models import Mailing

class Command(BaseCommand):
    help = 'Запуск рассылок. Можно указать ID рассылки.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--id',
            type=int,
            help='ID рассылки для отправки (если не указан, отправит все активные)'
        )

    def handle(self, *args, **options):
        mailing_id = options.get('id')
        if mailing_id:
            try:
                send_mailing(mailing_id)
                self.stdout.write(self.style.SUCCESS(f'Рассылка #{mailing_id} успешно отправлена'))
            except Mailing.DoesNotExist:
                raise CommandError(f'Рассылка с ID {mailing_id} не найдена')
        else:
            mailings = Mailing.objects.filter(status='created')
            for mailing in mailings:
                send_mailing(mailing.id)
                self.stdout.write(self.style.SUCCESS(f'Рассылка #{mailing.id} успешно отправлена'))
