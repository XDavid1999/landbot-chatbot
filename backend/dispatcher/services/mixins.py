from abc import ABC, abstractmethod
import os
from typing import Any


class ServiceInterfaceMixin(ABC):
    """
    Abstract base class defining the interface for notification services.
    Implements context management for connecting and disconnecting services.
    """

    def __init__(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        Initializes the service with a message.

        Args:
            message (str): The message to send.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.message: str = message

    @abstractmethod
    def send(self, *args: Any, **kwargs: Any) -> None:
        """
        Sends the message through the service.

        Raises:
            NotImplementedError: If not implemented in the subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def connect(self, *args: Any, **kwargs: Any) -> None:
        """
        Establishes a connection to the service.

        Raises:
            NotImplementedError: If not implemented in the subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def disconnect(self, *args: Any, **kwargs: Any) -> None:
        """
        Closes the connection to the service.

        Raises:
            NotImplementedError: If not implemented in the subclass.
        """
        raise NotImplementedError

    def _get_secret(self, key: str) -> str:
        """
        Retrieves a secret value from environment variables.

        Args:
            key (str): The environment variable key.

        Returns:
            str: The value of the environment variable.

        Raises:
            KeyError: If the environment variable is not set.
        """
        value = os.getenv(key)
        if value is None:
            raise KeyError(f"Environment variable '{key}' not found.")
        return value

    def __enter__(self) -> "ServiceInterfaceMixin":
        """
        Enters the runtime context related to this object.

        Returns:
            ServiceInterfaceMixin: The service instance.
        """
        self.connect()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        Exits the runtime context and disconnects the service.

        Args:
            exc_type: Exception type.
            exc_val: Exception value.
            exc_tb: Exception traceback.
        """
        self.disconnect()

    def validate(self, *args: Any, **kwargs: Any) -> bool:
        """
        Validates the necessary configuration for the service.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            bool: True if valid, False otherwise.
        """
        return True
