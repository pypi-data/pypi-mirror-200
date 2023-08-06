"""
Transport abstract class.
"""
from abc import ABC, abstractmethod
from typing import Callable
from iqrfpy.messages.requests.IRequest import IRequest
from iqrfpy.messages.responses.IResponse import IResponse


class ITransport(ABC):
    """
    Abstract class providing interface for communication channels.

    Methods
    -------
    initialize() -> None:
        Initializes transport and creates connection if applicable.
    send(request: IRequest) -> None:
        Serialize passed request to format acceptable by the communication channel and send request.
    receive() -> IResponse:
        Receive a response synchronously, deserialize data from communication channel to a response object.
    receive_async(callback: Callable[[IResponse], None]) -> None:
        Receive a response asynchronously, deserialize data from communication channel to a response object
        and execute a callback if a function was passed.
    """

    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize transport and create a connection if applicable.

        Returns
        -------
        None
        """

    @abstractmethod
    def send(self, request: IRequest) -> None:
        """
        Serialize passed request to format acceptable by the communication channel and send request.

        Parameters
        ----------
        request: IRequest
            Request to send

        Returns
        -------
        None
        """

    @abstractmethod
    def receive(self) -> IResponse:
        """
        Receive a response synchronously, deserialize data from communication channel to a response object.

        Returns
        -------
        response: IResponse
            Deserialized response object, returns concrete response class objects
        """

    @abstractmethod
    def receive_async(self, callback: Callable[[IResponse], None]) -> None:
        """
        Receive a response asynchronously, deserialize data from communication channel to a response object
        and execute a callback if a function was passed.

        Parameters
        ----------
        callback: Callable[[IResponse], None
            Function to call once a message has been received and successfully deserialized

        Returns
        -------
        None
        """
