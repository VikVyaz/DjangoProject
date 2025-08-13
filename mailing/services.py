from decouple import config
from django.core.mail import send_mail
from django.utils import timezone

from .models import BroadcastAttempt


def to_start_broadcast(broadcast):
    """Старт рассылки"""

    broadcast.status = 'running'
    broadcast.save()

    subject = broadcast.message.subject
    message = broadcast.message.body
    from_email = config('YANDEX_EMAIL_HOST_USER')

    for rec in broadcast.recipient.all():
        try:
            result = send_mail(subject, message, from_email, [rec.email,])

            BroadcastAttempt.objects.create(
                attempt_date_time=timezone.now(),
                status='success' if result > 0 else 'fail',
                response=f'Сообщение отправлено на {rec.email}',
                broadcast=broadcast
            )
        except Exception as e:
            BroadcastAttempt.objects.create(
                attempt_date_time=timezone.now(),
                status='fail',
                response=str(e),
                broadcast=broadcast
            )
    broadcast.last_send = timezone.now()
    broadcast.status = 'completed'
    broadcast.save()


def get_valid_context(context, user):
    """Остановка рассылки"""

    success_br = BroadcastAttempt.objects.filter(status='success')
    fail_br = BroadcastAttempt.objects.filter(status='fail')
    all_br = BroadcastAttempt.objects.all()

    if user.has_perm('mailing.can_view_all_broadcasts'):
        context['success_attempt'] = success_br.count()
        context['fail_attempt'] = fail_br.count()
        context['all_attempt'] = all_br.count()
        return context

    context['success_attempt'] = success_br.filter(broadcast__owner=user).count()
    context['fail_attempt'] = fail_br.filter(broadcast__owner=user).count()
    context['all_attempt'] = all_br.filter(broadcast__owner=user).count()

    return context


class CreateCacheCleanerMixin:
    """Миксин очистки кэша для CreateView"""

    def from_valid(self, form):
        form.instance.owner = self.request.user
        cache.clear()
        return super().form_valid(form)


class UpdateCacheCleanerMixin:
    """Миксин очистки кэша для UpdateView"""

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.clear()
        return response


class DeleteCacheCleanerMixin:
    """Миксин очистки кэша для DeleteView"""

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        cache.clear()
        return response
