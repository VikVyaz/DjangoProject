from django.urls import path

from users.apps import UsersConfig

from .views import (CustomLoginView, CustomLogoutView, RegisterView,
                    UserBanView, UserDetailView, UserListView, UserUpdateView)

app_name = UsersConfig.name

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name='update'),
    path('user/<int:pk>/detail/', UserDetailView.as_view(), name='detail'),
    path('', UserListView.as_view(), name='user_list'),
    path('user/<int:pk>/ban/', UserBanView.as_view(), name='user_ban'),
]
