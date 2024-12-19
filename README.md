# 🚀 Configuration Steps 🚀

Welcome to this amazing project! 🎉 Here's everything you need to know to set it up, run it, and test it locally.

## 📚 Additional Docs
- [Project Overview](docs/working_overview.md)
- [Notification System Overview](docs/how_it_works.md)
- [Adding New Services](docs/adding_new_services.md)
- [Possible Improvements](docs/possible_improvements.md)
- [Defense](docs/defense.md)

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
- **`docs/`:** Contains important information about the project.
- **`template.env`:** Environment variables template for configuring the project.

---


## 🤖 Integrating Services

This project supports third-party services like Telegram, Slack and Landbot:
- Add tokens in `.env`:
  - `TELEGRAM_BOT_TOKEN`
  - `SLACK_API_TOKEN`
- ⚠️ Some example values are on database and they can be modified as desired from django admin to work properly.
- Add your Landbot bot tokens on topics!.