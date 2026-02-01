# pylint: disable=C0103
from slim import server


class IndexView(server.View):
    def action_do(self, request: server.Request) -> server.Response:
        return server.Response({"message": "It works!"})


the_hostname = "localhost"
the_port = 8080
the_route = server.Route(server.Method.GET, "/")
the_view = IndexView()
the_index = [server.IndexNode(the_route, the_view)]
the_environment = server.Environment({"debug": True})
the_server = server.Server(the_environment, the_index, the_hostname, the_port)

the_server.run()
