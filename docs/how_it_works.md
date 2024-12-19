# Notification System Overview

This project enables sending notifications via multiple channels (Email, Slack, and Telegram). Below is a breakdown of how the system works and the key components:

---

## ⚙️ How It Works

1. **Models**:
   - `Notification`:
     - Defines the method (`Email`, `Slack`, `Telegram`) and its corresponding configuration (`config`).
     - Validates the provided configuration and associates it with a service handler.
   - `Topic`:
     - Groups notifications under a named context. Each topic has a unique name, description, chatbot_token, and associated notification method.

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

