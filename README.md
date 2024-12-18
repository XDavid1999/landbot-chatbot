# 🚀 Configuration Steps 🚀

Welcome to this amazing project! 🎉 Here's everything you need to know to set it up, run it, and test it locally.

---

## 🛠️ Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/XDavid1999/landbot-chatbot.git
   cd landbot-chatbot
   ```

2. **Create a `.env` file:**
   Inside the project root, create a `.env` file based on `template.env`. 
    ```bash
    cp emplate.env .env
    ```
   Fill in the required values, particularly:
   - `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
   - `DJANGO_SECRET_KEY` (Use a strong random string here)
   - Add your email credentials if required: `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`

3. **Start the application using Docker Compose:**
   ```bash
   docker-compose up --build
   ```

   - This will spin up the frontend, backend, PostgreSQL, and Redis services.
   - Once the services are up:
     - The **frontend** will be accessible at [http://localhost:3000](http://localhost:3000)
     - The **backend API** will be available at [http://localhost:8000](http://localhost:8000)

---

## 🛡️ Setting up the Admin Panel

To access the Django admin panel at [http://localhost:8000/admin](http://localhost:8000/admin), you'll need to create a superuser:

1. **Run the createsuperuser command:**
   ```bash
   docker-compose exec chatbot-backend python manage.py createsuperuser
   ```
2. **Follow the prompts to set up the admin user credentials.**

---

## 🗂️ Folder Structure Overview

- `frontend/`: Contains the code for the frontend application.
- `backend/`: Contains the Django project and its apps.
- `template.env`: Environment variables template for configuring the project.

---


## 🤖 Integrating Services

This project supports third-party services like Telegram and Slack:
- Add tokens in `.env`:
  - `TELEGRAM_BOT_TOKEN`
  - `SLACK_API_TOKEN`
- ⚠️ Some example values are on database and they can be modified as desired from django admin to work properly. ⚠️

# Notification System Overview

This project enables sending notifications via multiple channels (Email, Slack, and Telegram). Below is a breakdown of how the system works and the key components:

---

## 📚 How It Works

1. **Models**:
   - `Notification`:
     - Defines the method (`Email`, `Slack`, `Telegram`) and its corresponding configuration (`config`).
     - Validates the provided configuration and associates it with a service handler.
   - `Topic`:
     - Groups notifications under a named context. Each topic has a unique name, description, and associated notification method.

2. **Services**:
   Each notification method has a corresponding service class that:
   - Validates the provided configuration.
   - Handles the connection to the respective external service (e.g., Slack API or SMTP for Email).
   - Implements the `send()` method for delivering notifications.

   The service classes for each method:
   - `EmailService`: Uses Django's email framework to send emails.
   - `SlackService`: Utilizes the Slack SDK for message delivery.
   - `TelegramService`: Sends messages via the Telegram Bot API.

3. **Validation**:
   Before saving a notification, the `validate` method ensures:
   - All required fields are correctly populated.
   - The provided data matches the required schema (`EmailRequirements`, `SlackRequirements`, `TelegramRequirements`).

4. **Dispatcher Mechanism**:
   When a message is to be sent, the system:
   - Determines the notification method (based on the `method` field in the `Notification` model).
   - Invokes the corresponding service class to deliver the message.

---

## 🚀 Example Python Usage (Equivalent on django admin)

### 1. Create a Notification
Add a new notification configuration:
```python
from dispatcher.models import Notification

notification = Notification.objects.create(
    method=Notification.EMAIL,
    config={
        "recipient_list": ["user@example.com"],
        "subject": "Welcome Notification"
    },
)
```

### 2. Create a Topic
Associate the notification with a topic:
```python
from dispatcher.models import Topic

topic = Topic.objects.create(
    name="Welcome",
    description="Notifications sent to users when they first sign up",
    notification=notification,
)
```

### 3. Send a Notification
Use the appropriate service to dispatch the notification:
```python
from dispatcher.services.email import EmailService

email_service = EmailService()
email_service.send(
    message="Welcome to our platform!",
    recipient_list=["user@example.com"],
    subject="Hello!"
)
```

---

## 📦 Service Architecture

- **Email**:
  - Uses `Django.core.mail` to send messages.
  - Requires a recipient list and an optional subject.

- **Slack**:
  - Uses `slack_sdk` to post messages to a channel.
  - Requires a Slack channel and a valid API token.

- **Telegram**:
  - Sends messages using the Telegram Bot API.
  - Requires a `chat_id` and a bot token.

---

## 🔧 How to Extend It

1. **Add a New Notification Service**:
   - Create a new service class inheriting from `ServiceInterfaceMixin`.
   - Define:
     - `validator_class`: For validating configuration.
     - Methods: `connect`, `disconnect`, `send`.

2. **Update the `Notification` Model**:
   - Add the new service method to the `METHOD_CHOICES`.
   - Map the method to the new service in the `get_service` method.

Example for WhatsApp integration:
```python
class WhatsAppService(ServiceInterfaceMixin):
    validator_class = WhatsAppRequirements
    # Implementation here

class Notification(TimestampedModel):
    WHATSAPP = "WhatsApp"

    METHOD_CHOICES = [
        (EMAIL, "Email"),
        (SLACK, "Slack"),
        (TELEGRAM, "Telegram"),
        (WHATSAPP, "WhatsApp"),
    ]

    def get_service(self):
        if self.method == Notification.WHATSAPP:
            return WhatsAppService
```

3. **Test Your Integration**:
   - Write unit tests to validate your service and ensure the end-to-end flow works seamlessly.

---

With this system, you have a flexible and extensible way to manage notifications for different channels, ensuring scalability and ease of use.
