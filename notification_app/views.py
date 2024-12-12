from rest_framework.permissions import AllowAny
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .tasks import send_mail_task
from celery.result import AsyncResult


class NotificationView(APIView):
    serializer_class = NotificationSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            notification_status = request.query_params.get('status', None)
            if notification_status:
                notifications = Notification.objects.filter(status=notification_status)
                serializer = NotificationSerializer(notifications, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'please provide status in query params'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):
        try:
            notification_ids = request.data.get('notification_ids', [])
            notification_status = request.data.get('status', None)

            if notification_status != "read" and notification_status != "unread":
                return Response(
                    {'error': 'Status must be read or unread'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not notification_ids or not notification_status:
                return Response(
                    {'error': 'Both notification_ids and status are required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not all(isinstance(id_, int) for id_ in notification_ids):
                return Response(
                    {'error': 'All notification IDs must be integers.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            notifications = Notification.objects.filter(id__in=notification_ids)
            if not notifications.exists():
                return Response(
                    {'error': 'No notifications found for the given IDs.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            for notification in notifications:
                notification.status = notification_status

            Notification.objects.bulk_update(notifications, ['status'])

            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SendWelcomeEmailView(APIView):
    def post(self, request, *args, **kwargs):
        user_emails = request.data.get('emails', [])
        subject = 'Welcome!'
        message = 'Thanks for joining our platform!'

        if not user_emails:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        task = send_mail_task.delay(subject, message, user_emails)
        print(task)

        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)


class CheckTaskStatusView(APIView):
    def get(self, request, task_id, *args, **kwargs):
        task = AsyncResult(task_id)

        if task.state == 'SUCCESS':
            return JsonResponse({'task_id': task.id, 'status': task.state, 'result': task.result})

        elif task.state == 'PENDING':
            return JsonResponse({'task_id': task.id, 'status': task.state, 'result': 'Task is still processing'})

        elif task.state == 'FAILURE':
            return JsonResponse({'task_id': task.id, 'status': task.state, 'result': str(task.result)})

        return Response({'task_id': task.id, 'status': 'UNKNOWN', 'result': 'Status is unknown'}, status=status.HTTP_400_BAD_REQUEST)
