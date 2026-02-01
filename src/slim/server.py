import abc
import dataclasses
import enum
import socket
import typing


class EndOfStream(Exception):
    pass


class ContinuationOfStream(Exception):
    pass


class Method(enum.Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class Environment(dict):
    pass


@dataclasses.dataclass
class Route:
    method: Method
    action: str


@dataclasses.dataclass
class ViewBlock(abc.ABC):
    request: Request
    view: View

    def answer(self) -> Response:
        return self.take_action()

    @abc.abstractmethod
    def take_action(self) -> Response:
        raise NotImplementedError()


class Request(dict):
    pass


class Response(dict):
    pass


class View(abc.ABC):
    @abc.abstractmethod
    def action_do(self, request: Request) -> Response:
        raise NotImplementedError()


@dataclasses.dataclass
class IndexNode:
    route: Route
    view: View


class Server:
    RECV_BUFFER_SIZE = 4096

    def __init__(
        self,
        environment: Environment,
        index: typing.List[IndexNode],
        hostname: str,
        port: int,
    ) -> None:
        self.environment = environment
        self.index = index
        self.port = port
        self.hostname = hostname

        self.whoami()

    def whoami(self) -> None:
        print(f"Running server on {self.hostname}:{self.port}.")

    def run(self) -> None:
        buffer = ""
        connection = None

        def get():
            nonlocal buffer, connection

            message_part = connection.recv(self.RECV_BUFFER_SIZE)
            length = len(message_part)

            if length == 0 or length <= self.RECV_BUFFER_SIZE:
                raise EndOfStream()

            buffer += message_part.decode("utf-8").strip()
            raise ContinuationOfStream()

        the_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        the_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        the_socket.bind((self.hostname, self.port))
        the_socket.listen()

        while True:
            try:
                print("Waiting for connection...")
                connection, client_address = the_socket.accept()
                ip, port = client_address
                print(f"Connected to {ip}:{port}.")

                print("Getting.")
                while True:
                    print("Streaming...")
                    try:
                        get()
                    except ContinuationOfStream:
                        print("Stream continues.")
            except EndOfStream:
                print("Stream ended.")
                if connection is not None:
                    connection.close()

    def process(self, request: Request) -> Response:
        return Response(request)

    def send_response(self, status_code: int) -> None:
        pass

    def send_header(self, type_string: str, value_string: str) -> None:
        pass

    def send_headers(self) -> None:
        self.send_response(200)
        self.send_header("Content-type", "application/json")
