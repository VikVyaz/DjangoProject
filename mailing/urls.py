from django.urls import path

from mailing.apps import MailingConfig

from .views import (BroadcastAttemptDeleteView, BroadcastAttemptDetailView,
                    BroadcastAttemptListView, BroadcastCreateView,
                    BroadcastDeleteView, BroadcastDetailView,
                    BroadcastListView, BroadcastUpdateView, MainPageView,
                    MessageCreateView, MessageDeleteView, MessageDetailView,
                    MessageListView, MessageUpdateView, RecipientCreateView,
                    RecipientDeleteView, RecipientDetailView,
                    RecipientListView, RecipientUpdateView, StartBroadcastView)

app_name = MailingConfig.name

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),

    path('recipients/', RecipientListView.as_view(), name='recipient_list'),
    path('recipients/new/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipients/<int:pk>/details/', RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipients/<int:pk>/update/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipients/<int:pk>/delete/', RecipientDeleteView.as_view(), name='recipient_delete'),

    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/new/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/details/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    path('broadcasts/', BroadcastListView.as_view(), name='broadcast_list'),
    path('broadcasts/new/', BroadcastCreateView.as_view(), name='broadcast_create'),
    path('broadcasts/<int:pk>/details/', BroadcastDetailView.as_view(), name='broadcast_detail'),
    path('broadcasts/<int:pk>/update/', BroadcastUpdateView.as_view(), name='broadcast_update'),
    path('broadcasts/<int:pk>/delete/', BroadcastDeleteView.as_view(), name='broadcast_delete'),
    path('broadcasts/<int:pk>/start/', StartBroadcastView.as_view(), name='broadcast_start'),

    path('attempt/', BroadcastAttemptListView.as_view(), name='attempt_list'),
    path('attempt/<int:pk>/detail/', BroadcastAttemptDetailView.as_view(), name='attempt_detail'),
    path('attempt/<int:pk>/delete/', BroadcastAttemptDeleteView.as_view(), name='attempt_delete'),
]
