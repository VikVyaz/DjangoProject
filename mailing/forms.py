from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Broadcast, Message, Recipient


class StyleFormMixin:
    placeholder_data = {}
    form_class_data = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            data = {
                'class': self.form_class_data.get(name, 'form-control'),
                'placeholder': self.placeholder_data.get(name, '')
            }
            if name == 'status':
                field.help_text = ('"Создана" - рассылка создана, но не запущена\n'
                                   '"Запущена" - рассылка работает\n'
                                   '"Завершена" - рассылка закончила работу, все адресаты отработаны')

            self.fields[name].widget.attrs.update(data)


class RecipientForm(StyleFormMixin, ModelForm):
    placeholder_data = {
        'email': 'Формат: example@mail.com',
        'full_name': 'Формат: "Иванов Иван Иванович" или "John Smith"'
    }

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if len(full_name.strip().split()) not in [2, 3]:
            raise ValidationError('ФИО должно состоять из фамилии, имени и отчества(если есть).\n'
                                  'Например: Иванов Иван Иванович, или John Smith')
        return full_name

    class Meta:
        model = Recipient
        fields = ['email', 'full_name', 'comment']


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']


class BroadcastForm(StyleFormMixin, ModelForm):
    form_class_data = {
        'status': 'form-select',
        'message': 'form-select'
    }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            if user.has_perm('mailing.can_view_all_recipients'):
                self.fields['recipient'].queryset = Recipient.objects.all()
            else:
                self.fields['recipient'].queryset = Recipient.objects.filter(owner=user)

    class Meta:
        model = Broadcast
        fields = ['message', 'recipient']
