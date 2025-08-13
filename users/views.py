from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.views import LoginView, LogoutView
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import CustomAuthForm, UserRegisterFrom, UserUpdateForm
from .models import User


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = CustomAuthForm
    next_page = ''

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.clear()
        return response


class CustomLogoutView(LogoutView):
    next_page = ''

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        cache.clear()
        return response


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterFrom
    success_url = reverse_lazy('mailing:main_page')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        cache.clear()
        return super().form_valid(form)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/detail.html'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/update.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('mailing:main_page')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        cache.clear()
        return super().form_valid(form)


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'view_users_list'
    context_object_name = 'users'


class UserBanView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'view_users_list'

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        user.is_active = not user.is_active
        user.save()

        return redirect('users:user_list')
