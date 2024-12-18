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

- **`frontend/`:** Contains the code for the frontend application.
- **`backend/`:** Contains the Django project and its apps.
- **`template.env`:** Environment variables template for configuring the project.

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

### ❓ **Design Defense**

#### Why `_get_secret` is defined in `ServiceInterfaceMixin`?
- **Reasoning**: `_get_secret` centralizes the retrieval of secure credentials such as API tokens or keys. Storing such credentials in environments like Google Secrets or AWS Secrets Manager ensures they are safe from unauthorized database access or accidental leakage.  
- **Benefits**:
  - Facilitates secure access control and auditing.
  - Decouples sensitive configuration from database-managed runtime data.
  - Promotes scalability, especially for environments where secrets might differ between instances or regions.

#### Why is the `config` stored in the database?
- **Reasoning**:  We could encrypt the field and, unlike secrets or highly sensitive keys, the notification `config` (e.g., channel names, recipient lists, or `chat_id`) is operational data required to manage the application's behavior. Keeping such configurations in the database allows for:
  - **Flexibility**: Users and administrators can modify notification settings without needing a developer to deploy changes.
  - **Ease of Use**: Changes via UI or admin dashboards make it easier for non-developers to control the application dynamically.
  - **Non-Critical Data**: The data stored doesn’t present a significant security risk, as credentials are fetched securely via `_get_secret`.

#### Why use an interface and the inheritance/composition pattern?
- **Reasoning**: 
  - The system uses **inheritance** (via `ServiceInterfaceMixin`) to enforce a standard structure and workflow for any service class. This ensures all services:
    - Have common connection, validation, and disconnection methods.
    - Adhere to the `send` interface, making the notification dispatch process generic and extensible.
  - **Composition** comes into play when:
    - The `Notification` class selects and uses the appropriate service class (`get_service()`).
  - **Pattern Benefits**:
    - **Abstraction**: The `Notification` model need not care about implementation details (e.g., how Slack handles API errors or how Telegram formats requests).
    - **Scalability**: Adding new notification methods is frictionless — simply implement a new service class adhering to the interface.
    - **Maintainability**: By segregating logic into service-specific handlers, the code remains clean, testable, and future-proof.

#### Why Use Celery?
- **Asynchronous Processing:** Notifications (e.g., sending emails, posting to Slack) can be time-consuming due to API latency. Celery allows these tasks to be handled in the background, ensuring the system remains responsive.
- **Scalability:** Celery can handle a large volume of notifications by distributing tasks across multiple workers, crucial for systems with high throughput requirements.
- **Retry Mechanisms:** If a notification fails (e.g., API downtime), Celery's built-in retries ensure the system automatically attempts to reprocess it without manual intervention.
- **Separation of Concerns:** Offloading execution from the main request cycle enhances maintainability and simplifies the codebase.

---

### 🔝 **Proposed Improvements**

#### Store Sent Notifications in a Log Table
- **Auditability:** A persistent record provides traceability for debugging and accountability, especially for important notifications.
- **Error Tracking:** Logging metadata such as failures, retries, timestamps, and recipient information makes it easier to identify issues.
- **Statistical Analysis:** Historical logs allow generating reports on notification success rates, platform performance, and user engagement.
- **Flexibility:** Logs can include:
- **Notification ID**.
- **Method** (`Slack`, `Email`, etc.).
- **Status** (`Sent`, `Failed`, `Retrying`).
- **Metadata** (recipient, timestamp, error message).

##### Why Use Elasticsearch for Logs?
- **Full-Text Search:** Elasticsearch provides a fast and powerful search interface to query logs, perfect for filtering and analyzing large datasets.
- **Centralized Logging:** Store all logs in Elasticsearch to aggregate notifications, API errors, and task retries in one place.
- **Real-Time Analytics:** Elasticsearch enables dashboards (via Kibana) to visualize metrics like message delivery success rates or performance by platform in real time.
- **Scalability:** Unlike relational databases, Elasticsearch is optimized for large-scale read and write operations, making it ideal for log management.

#### Cross-Platform Communication via WebSocket Responses

**Problem**: While we can send notifications to various platforms, there's no feedback or acknowledgment mechanism from those platforms to our users.  
**Proposed Improvement**:
- Redirect **destination responses** back to our API and provide real-time updates using WebSockets to clients interacting on different platforms.
  - For example, if a user sends a query via Telegram:
    1. The Telegram API forwards the query to our backend.
    2. The backend processes the message and sends the response to our notification service.
    3. The notification service delivers the response to Telegram and also emits the same message to other platforms (e.g., Slack or web UI) using WebSockets.

**Advantages**:
- **Cross-Platform Synchronization**: A user interacting on Telegram could see relevant updates or messages on Slack or a web UI without delay.
- **Enhanced User Experience**: Real-time feedback keeps users informed, reducing anxiety about message status.
- **Interactivity**: With WebSockets, user replies on one platform could dynamically influence outputs on another.

#### High-Level Architecture for Cross-Platform Real-Time Communication:
1. **Message Ingress**:
   - Receive messages (or actions) from platforms such as Telegram, Slack, or Email.
   - Process them in the backend and store responses in a shared structure (e.g., queues or in-memory databases).

2. **WebSocket Communication**:
   - Set up a WebSocket server (using Django Channels or similar).
   - Notify connected clients of updates in real-time.

3. **Delivery Coordination**:
   - Implement a dispatcher that sends responses back to platforms via the respective notification service.
   - Broadcast updates simultaneously via WebSocket to connected clients (e.g., browser-based admin dashboards).
