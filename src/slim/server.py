import abc
import dataclasses
import enum
import socket


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
        index: list[IndexNode],
        hostname: str,
        port: int,
    ) -> None:
        self.environment: Environment = environment
        self.index: list[IndexNode] = index
        self.port: int = port
        self.hostname: str = hostname

        self.socket: socket.socket | None = None
        self.connection: socket.socket | None = None

        self.whoami()

    def whoami(self) -> None:
        print(f"Running server on {self.hostname}:{self.port}.")

    def setup_connection(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.hostname, self.port))

        self.socket.listen()

    def get(self, buffer: str = "", connection: socket.socket | None = None) -> None:
        if connection is None:
            return
        message_part = connection.recv(self.RECV_BUFFER_SIZE)
        buffer += message_part

        length = len(message_part)
        if length > self.RECV_BUFFER_SIZE:
            raise ContinuationOfStream()
        if length <= self.RECV_BUFFER_SIZE:
            raise EndOfStream()

    def while_loop(self) -> None:
        while True:
            try:
                print("Waiting for connection...")
                self.connection, client_address = self.socket.accept()
                ip, port = client_address
                print(f"Connected to {ip}:{port}.")

                print("Getting.")
                while True:
                    print("Streaming...")
                    try:
                        self.get()
                    except ContinuationOfStream:
                        print("Stream continues.")
            except EndOfStream:
                print("Stream ended.")
                if self.connection is not None:
                    self.connection.close()

    def run(self) -> None:
        self.setup_connection()
        self.while_loop()

    @staticmethod
    def process(request: Request) -> Response:
        return Response(request)

    def send_response(self, status_code: int) -> None:
        pass

    def send_header(self, type_string: str, value_string: str) -> None:
        pass

    def send_headers(self) -> None:
        self.send_response(200)
        self.send_header("Content-type", "application/json")
