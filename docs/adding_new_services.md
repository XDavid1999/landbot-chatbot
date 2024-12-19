# 🚀 Example: Adding a New Service via Django Admin or Migrations

## 1. Add a Notification via Admin Panel  
- Go to the **Django Admin** panel and navigate to the **Notifications** section.  
- Create a new Notification by selecting a `method` (e.g., **Email**, **Slack**, or **Telegram**) and configuring the appropriate `config` field with JSON, like:  

    ##### Email
    ```json
    {
        "recipient_list": ["user@example.com"],
        "subject": "Welcome Notification"
    }
    ```

    ##### Slack
    ```json
    {
        "channel": "#channel"
    }
    ```

    ##### Telegram
    ```json
    {
        "chat_id": "12345678"
    }
    ```

---

## 2. Add a Notification via Migrations  
Alternatively, use a **migration script** to define a new Notification:

```python
from django.db import migrations

def create_notification(apps, schema_editor):
    Notification = apps.get_model("dispatcher", "Notification")
    notification = Notification.objects.create(
        method="Email",
        config={
            "recipient_list": ["user@example.com"],
            "subject": "Welcome Notification",
        },
    )

class Migration(migrations.Migration):
    dependencies = [
        ("dispatcher", "XXXX_dependency")
    ]

    operations = [
        migrations.RunPython(create_notification),
    ]
```

---

## 3. Assign Notifications to Topics  
Use the Admin or migration scripts to associate a Notification with a **Topic**, making it reusable across events.


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

