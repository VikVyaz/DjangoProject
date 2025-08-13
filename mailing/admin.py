from django.contrib import admin

from .models import Broadcast, BroadcastAttempt, Message, Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'comment',)
    search_fields = ('id', 'full_name',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'body',)
    search_fields = ('subject', 'body',)


@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_send', 'last_send', 'status', 'message', 'get_recipients',)
    search_fields = ('status', 'message',)

    @admin.display(description='Получатели')
    def get_recipients(self, obj):
        return ", ".join([str(r) for r in obj.recipient.all()])


@admin.register(BroadcastAttempt)
class BroadcastAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'attempt_date_time', 'status', 'response', 'broadcast',)
