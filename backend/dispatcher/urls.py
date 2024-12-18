from django.urls import path, include
from rest_framework.routers import DefaultRouter
from dispatcher.views import (
    TopicViewSet,
    NotificationViewSet,
    Dispatcher,
)


# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(r"topics", TopicViewSet)
router.register(r"notifications", NotificationViewSet)

# The API URLs are now determined automatically by the router.
dispatcher_urlpatterns = [
    path("dispatcher/", Dispatcher.as_view({"post": "post"})),
    path("", include(router.urls)),
]
