from abc import ABC, abstractmethod
import os
from typing import Any


class ServiceInterfaceMixin(ABC):
    """
    Abstract base class defining the interface for notification services.
    Implements context management for connecting and disconnecting services.
    """

    validator_class: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initializes the service with a message.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.connect()

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
            raise KeyError(f"The secret '{key}' is not set")
        return value

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
        if self.validator_class is None:
            raise NotImplementedError("Validator class not set")

        try:
            self.validator_class(**kwargs)
            return True
        except TypeError:
            return False
