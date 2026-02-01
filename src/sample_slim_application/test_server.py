from slim import server


def test_run() -> None:
    environment = server.Environment()
    the_server = server.Server(environment, [], "localhost", 8080)

    assert the_server is not None
