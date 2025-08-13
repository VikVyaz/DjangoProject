from django.db import models

from users.models import User


class Recipient(models.Model):
    """МОДЕЛЬ. Клиент, получатель рассылки"""

    email = models.EmailField(unique=True, verbose_name='Email получателя рассылки')
    full_name = models.CharField(verbose_name='ФИО получателя рассылки')
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий к профилю получатель рассылки')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='recipient', null=True, blank=True,
                              verbose_name='Создатель карточки клиента')

    def __str__(self):
        return f'Получатель рассылки: {self.full_name}. Email: {self.email}.'

    class Meta:
        verbose_name = 'Получатель рассылки'
        verbose_name_plural = 'Получатели рассылки'
        ordering = ['id']
        db_table = 'recipient'
        permissions = [
            ('can_view_all_recipients', 'Может просматривать всех клиентов')
        ]


class Message(models.Model):
    """МОДЕЛЬ. Сообщение"""

    subject = models.CharField(verbose_name='Тема сообщения')
    body = models.TextField(verbose_name='Тело сообщения')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='message', null=True, blank=True,
                              verbose_name='Создатель сообщения')

    def __str__(self):
        return f'"{self.subject}"'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщении'
        ordering = ['id']
        db_table = 'message'
        permissions = [
            ('can_view_all_messages', 'Может просматривать все сообщения')
        ]


class Broadcast(models.Model):
    """МОДЕЛЬ. Рассылка"""

    MAILING_STATUS = [
        ('created', 'Создана'),
        ('running', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    first_send = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата и время первой отправки')
    last_send = models.DateTimeField(blank=True, null=True,
                                     verbose_name='Дата и время окончания отправки')
    status = models.CharField(choices=MAILING_STATUS, default='created',
                              verbose_name='Статус рассылки')
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, blank=True, null=True,
                                verbose_name='Сообщение рассылки')
    recipient = models.ManyToManyField(Recipient,
                                       verbose_name='Получатель/получатели рассылки')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='broadcast', null=True, blank=True,
                              verbose_name='Создатель рассылки')

    def __str__(self):
        return f'Рассылка №{self.id}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['id']
        db_table = 'broadcast'
        permissions = [
            ('can_view_all_broadcasts', 'Может просматривать все рассылки'),
            ('broadcast_shutdown', 'Отключение рассылки')
        ]


class BroadcastAttempt(models.Model):
    """МОДЕЛЬ. Попытка рассылки"""

    ATTEMPT_STATUS = [
        ('success', 'Успешно'),
        ('fail', 'Не успешно')
    ]

    attempt_date_time = models.DateTimeField(auto_now=True,
                                             verbose_name='Дата и время попытки рассылки')
    status = models.CharField(choices=ATTEMPT_STATUS,
                              verbose_name='Статус попытки')
    response = models.TextField(verbose_name='Ответ почтового сервера')
    broadcast = models.ForeignKey(Broadcast, on_delete=models.SET_NULL, blank=True, null=True,
                                  verbose_name='Рассылка')

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
        ordering = ['id']
        db_table = 'broadcast_attempt'
