import typing

from pytest import fixture

from slim import server


@fixture
def generate_environment() -> server.Environment:
    return server.Environment({"SENTRY_DSN": "https://sentry.com/?dsn=Ablablublebly"})


@fixture
def generate_route() -> server.Route:
    method = server.Method.GET
    action = "/"

    the_route = server.Route(method, action)
    return the_route


@fixture
def generate_index() -> typing.List[server.IndexNode]:
    return []


@fixture
def generate_port() -> int:
    return 8080


@fixture
def generate_message() -> str:
    return "It works!"


@fixture
def generate_hostname() -> str:
    return "localhost"


@fixture
def generate_server(
    generate_environment, generate_index, generate_hostname, generate_port
) -> server.Server:
    the_server = server.Server(
        generate_environment, generate_index, generate_hostname, generate_port
    )
    return the_server


class TestServer:
    def test_server_adds_route(
        self, generate_environment, generate_index, generate_hostname, generate_port
    ) -> None:
        the_server = server.Server(
            generate_environment, generate_index, generate_hostname, generate_port
        )

        assert isinstance(generate_environment, server.Environment)
        assert len(generate_index) >= 0
        assert the_server.port == generate_port

    def test_server_accepts(self):
        pass
