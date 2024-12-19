# ❓ **Design Defense**

## Why `_get_secret` is defined in `ServiceInterfaceMixin`?
- **Reasoning**: `_get_secret` centralizes the retrieval of secure credentials such as API tokens or keys. Storing such credentials in environments like Google Secrets or AWS Secrets Manager ensures they are safe from unauthorized database access or accidental leakage.  
- **Benefits**:
  - Facilitates secure access control and auditing.
  - Decouples sensitive configuration from database-managed runtime data.
  - Promotes scalability, especially for environments where secrets might differ between instances or regions.

## Why is the `config` stored in the database?
- **Reasoning**:  We could encrypt the field and, unlike secrets or highly sensitive keys, the notification `config` (e.g., channel names, recipient lists, or `chat_id`) is operational data required to manage the application's behavior. Keeping such configurations in the database allows for:
  - **Flexibility**: Users and administrators can modify notification settings without needing a developer to deploy changes.
  - **Ease of Use**: Changes via UI or admin dashboards make it easier for non-developers to control the application dynamically.
  - **Non-Critical Data**: The data stored doesn’t present a significant security risk, as credentials are fetched securely via `_get_secret`.

## Why use an interface and the inheritance/composition pattern?
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

## Why Use Celery?
- **Asynchronous Processing:** Notifications (e.g., sending emails, posting to Slack) can be time-consuming due to API latency. Celery allows these tasks to be handled in the background, ensuring the system remains responsive.
- **Scalability:** Celery can handle a large volume of notifications by distributing tasks across multiple workers, crucial for systems with high throughput requirements.
- **Retry Mechanisms:** If a notification fails (e.g., API downtime), Celery's built-in retries ensure the system automatically attempts to reprocess it without manual intervention.
- **Separation of Concerns:** Offloading execution from the main request cycle enhances maintainability and simplifies the codebase.

