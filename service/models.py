from django.db import models
from django.conf import settings

class Client(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='clients', verbose_name='Владелец')
    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=255, verbose_name='Ф.И.О.')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    def __str__(self):
        return f"{self.full_name} <{self.email}>"

class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return self.subject

class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('running', 'Запущена'),
        ('finished', 'Завершена'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mailings', verbose_name='Владелец')
    start_datetime = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время первой отправки')
    end_datetime = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время окончания отправки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created', verbose_name='Статус рассылки')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='mailings', verbose_name='Сообщение')
    clients = models.ManyToManyField(Client, related_name='mailings', verbose_name='Получатели')

    def __str__(self):
        return f"Рассылка #{self.id} - {self.get_status_display()}"

class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Не успешно'),
    ]

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts', verbose_name='Рассылка')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='attempts', verbose_name='Клиент')
    attempt_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Статус')
    server_response = models.TextField(blank=True, verbose_name='Ответ почтового сервера')

    def __str__(self):
        return f"Попытка рассылки #{self.id} для {self.client.email} - {self.get_status_display()}"

