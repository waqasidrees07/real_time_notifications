
# Project Setup and Testing Instructions

This document provides step-by-step instructions to set up and test the WebSocket integration and Celery task processing in your Django project.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setting Up the Server](#setting-up-the-server)
3. [Running Celery Worker](#running-celery-worker)
4. [Testing WebSocket Integration](#testing-websocket-integration)
5. [Testing Celery Task](#testing-celery-task)
6. [Check Celery Task Status](#check-celery-task-status)
7. [API to Update Notification Status](#api-to-update-notification-status)
6. [Troubleshooting](#troubleshooting)

## 1. Prerequisites

Before you begin, make sure you have the following installed:
- Python 3.8+
- Django
- Redis (for Celery and WebSocket)
- Celery

### Install Python Dependencies
Run the following command to install all required dependencies:

```bash
pip install -r requirements.txt
```

### Install Redis
Redis is required for both Celery and WebSocket functionalities. If Redis is not already installed, follow the instructions below.

- **On Ubuntu/Debian**:
  ```bash
  sudo apt update
  sudo apt install redis-server
  ```

- **On macOS (via Homebrew)**:
  ```bash
  brew install redis
  ```

To start Redis:
```bash
redis-server
```

## 2. Setting Up the Server

### Run the Django Server
Once Redis is installed and running, start the Django development server by running:

```bash
python manage.py runserver
```

This will start the server at `http://127.0.0.1:8000/`.

## 3. Running Celery Worker

To handle background tasks, you need to start a Celery worker. Open a new terminal and run:

```bash
celery -A real_time_notifications worker --loglevel=info
```

### Monitoring Celery Tasks
You can monitor the Celery task execution through the terminal logs. The `--loglevel=info` flag will display information about task execution.

## 4. Testing WebSocket Integration

### WebSocket Endpoint

Test the WebSocket connection at the following URL:
```
ws://127.0.0.1:8000/ws/notifications/
```

Send the following event to create and send a notification:
```json
{
    "message": "Here is a notification for you"
}
```

Once the event is sent, it will trigger the creation and sending of the notification.

## 5. Testing Celery Task

### API to Send Welcome Emails using Celery

To send welcome emails to users using Celery, make a `POST` request to the following endpoint:
```
POST http://127.0.0.1:8000/send-welcome-email/
```

**Payload**:
```json
{
    "emails": [
        "waqasxyz15@gmail.com", 
        "waqas84573@gmail.com", 
        "waqasxyz15+1@gmail.com", 
        "waqas84573+1@gmail.com",
        "waqasxyz15+2@gmail.com", 
        "waqas84573+2@gmail.com"
    ]
}
```

The response will return a `task_id` to track the status of the Celery task:
```json
{
    "task_id": "1c4d566e-9fc2-4ac2-b3fe-64dd21099c14"
}
```

## 6. Check Celery Task Status

To check the status of a specific Celery task, make a `GET` request to:
```
GET http://127.0.0.1:8000/task-status/{task_id}
```

For example:
```
GET http://127.0.0.1:8000/task-status/8185d90d-4790-45d5-b804-bb9531c2fa95
```

**Response**:
```json
{
    "task_id": "8185d90d-4790-45d5-b804-bb9531c2fa95",
    "status": "SUCCESS",
    "result": null
}
```

## 7. API to Update Notification Status

#### Get Notification Status
To check the status of a notification, make a `GET` request to:
```
GET http://127.0.0.1:8000/notification-status?status=read
```

#### Update Notification Status
To update the status of multiple notifications, make a `POST` request to:
```
POST http://127.0.0.1:8000/notification-status/
```

**Payload**:
```json
{
    "notification_ids": [2, 3, 4],
    "status": "read"
}
```

## 8. Troubleshooting

### Common Issues

1. **Celery Worker Not Running:**
   Ensure that the Celery worker is running by using the following command in separate terminal:
   ```bash
   celery -A real_time_notifications worker --loglevel=info
   ```

2. **WebSocket Not Responding:**
   Ensure that Django Channels or your WebSocket server is properly configured in the `settings.py` and `routing.py` files.

3. **Redis Not Found:**
   If Redis is not found, ensure that Redis is installed and running. You can check its status with:
   ```bash
   sudo systemctl status redis
   ```

4. **Celery Task Not Executing:**
   If Celery tasks are not executing, check the logs for errors. Verify that the `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` are correctly configured in `settings.py`.

5. **WebSocket Connection Issues:**
   - Make sure that the WebSocket URL is correct and accessible at `ws://127.0.0.1:8000/ws/notifications/`.
   - Check if any firewall or security settings are blocking WebSocket connections.

---

For additional help, refer to the [Django documentation](https://docs.djangoproject.com/en/stable/) or the [Celery documentation](https://docs.celeryproject.org/en/stable/).