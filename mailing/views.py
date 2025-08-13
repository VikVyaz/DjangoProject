from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import BroadcastForm, MessageForm, RecipientForm
from .models import Broadcast, BroadcastAttempt, Message, Recipient
from .services import get_valid_context, to_start_broadcast, CreateCacheCleanerMixin


# __________________________________________block Main Page_____________________________________________________________
class MainPageView(View):
    template_name = 'main_page/main_page.html'

    def get(self, request):
        context = {
            'total_broadcasts': Broadcast.objects.all().count(),
            'active_broadcasts': Broadcast.objects.filter(status='running').count(),
            'unique_recipients': Recipient.objects.all().count(),
        }
        return render(request, self.template_name, context)


# __________________________________________block Recipients____________________________________________________________
@method_decorator(cache_page(60 * 15), name='dispatch')
class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = 'recipients/recipient_list.html'
    context_object_name = 'recipients'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('mailing.can_view_all_recipients'):
            return queryset
        return queryset.filter(owner=self.request.user)


class RecipientCreateView(LoginRequiredMixin, CreateCacheCleanerMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'recipients/recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    template_name = 'recipients/recipient_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        full_name = self.object.full_name.strip().split()
        if len(full_name) == 3:
            context['last_name'], context['first_name'], context['patronymic'] \
                = full_name
        if len(full_name) == 2:
            context['first_name'], context['last_name'] = full_name

        return context


class RecipientUpdateView(LoginRequiredMixin, UpdateCacheCleanerMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'recipients/recipient_form.html'
    extra_context = {'update': True}

    def get_success_url(self):
        return reverse_lazy('mailing:recipient_detail', kwargs={'pk': self.object.pk})


class RecipientDeleteView(LoginRequiredMixin, DeleteCacheCleanerMixin, DeleteView):
    model = Recipient
    template_name = 'recipients/recipient_delete.html'
    success_url = reverse_lazy('mailing:recipient_list')


# __________________________________________block Messages______________________________________________________________
@method_decorator(cache_page(60 * 15), name='dispatch')
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messages/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('mailing.can_view_all_messages'):
            return queryset
        return queryset.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateCacheCleanerMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'messages/message_form.html'
    success_url = reverse_lazy('mailing:message_list')


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'messages/message_detail.html'


class MessageUpdateView(LoginRequiredMixin, UpdateCacheCleanerMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'messages/message_form.html'
    extra_context = {'update': True}

    def get_success_url(self):
        return reverse_lazy('mailing:message_detail', kwargs={'pk': self.object.pk})


class MessageDeleteView(LoginRequiredMixin, DeleteCacheCleanerMixin, DeleteView):
    model = Message
    template_name = 'messages/message_delete.html'
    success_url = reverse_lazy('mailing:message_list')


# __________________________________________block Broadcasts____________________________________________________________
class UserFormKwargsMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


@method_decorator(cache_page(60 * 15), name='dispatch')
class BroadcastListView(LoginRequiredMixin, ListView):
    model = Broadcast
    template_name = 'broadcasts/broadcast_list.html'
    context_object_name = 'broadcasts'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('mailing.can_view_all_broadcasts'):
            return queryset
        return queryset.filter(owner=self.request.user)


class BroadcastCreateView(LoginRequiredMixin, UserFormKwargsMixin, CreateCacheCleanerMixin, CreateView):
    model = Broadcast
    form_class = BroadcastForm
    template_name = 'broadcasts/broadcast_form.html'
    success_url = reverse_lazy('mailing:broadcast_list')


class BroadcastDetailView(LoginRequiredMixin, DetailView):
    model = Broadcast
    template_name = 'broadcasts/broadcast_detail.html'


class BroadcastUpdateView(LoginRequiredMixin, UserFormKwargsMixin, UpdateCacheCleanerMixin, UpdateView):
    model = Broadcast
    form_class = BroadcastForm
    template_name = 'broadcasts/broadcast_form.html'
    extra_context = {'update': True}

    def get_success_url(self):
        return reverse_lazy('mailing:broadcast_detail', kwargs={'pk': self.object.pk})


class BroadcastDeleteView(LoginRequiredMixin, DeleteCacheCleanerMixin, DeleteView):
    model = Broadcast
    template_name = 'broadcasts/broadcast_delete.html'
    success_url = reverse_lazy('mailing:broadcast_list')


class StartBroadcastView(LoginRequiredMixin, View):
    def post(self, request, pk):
        broadcast = get_object_or_404(Broadcast, pk=pk)
        cache.clear()
        to_start_broadcast(broadcast)
        return redirect('mailing:broadcast_detail', pk=pk)


class StopBroadcastView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'mailing.broadcast_shutdown'

    def post(self, request, pk):
        broadcast = get_object_or_404(Broadcast, pk=pk)
        broadcast.status = 'stopped'
        cache.clear()
        broadcast.save()
        return redirect('mailing:broadcast_detail', pk=pk)


# __________________________________________block BroadcastAttempt____________________________________________________

@method_decorator(cache_page(60 * 15), name='dispatch')
class BroadcastAttemptListView(LoginRequiredMixin, ListView):
    model = BroadcastAttempt
    template_name = 'attempt/attempt_list.html'
    context_object_name = 'attempts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        valid_context = get_valid_context(context, user)

        return valid_context

    def get_queryset(self):
        if self.request.user.has_perm('mailing.can_view_all_broadcasts'):
            return super().get_queryset()
        return super().get_queryset().filter(broadcast__owner=self.request.user)


class BroadcastAttemptDetailView(LoginRequiredMixin, DetailView):
    model = BroadcastAttempt
    template_name = 'attempt/attempt_detail.html'
    context_object_name = 'attempt'


class BroadcastAttemptDeleteView(LoginRequiredMixin, DeleteCacheCleanerMixin, DeleteView):
    model = BroadcastAttempt
    template_name = 'attempt/attempt_delete.html'
    success_url = reverse_lazy('mailing:attempt_list')
    context_object_name = 'attempt'
