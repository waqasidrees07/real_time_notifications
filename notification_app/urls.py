from django.urls import path
from .views import NotificationView, SendWelcomeEmailView, CheckTaskStatusView


urlpatterns = [
    path("notification-status/", NotificationView.as_view(), name="update_notification"),
    path('send-welcome-email/', SendWelcomeEmailView.as_view(), name='send_welcome_email'),
    path('task-status/<str:task_id>/', CheckTaskStatusView.as_view(), name='check_task_status'),
]
