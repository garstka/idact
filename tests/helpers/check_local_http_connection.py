import requests


def check_local_http_connection(port: int):
    """Checks, whether a http server is listening on this port of the local
        host.

        :param port: HTTP port.

    """
    request = requests.get("http://127.0.0.1:{port}".format(
        port=port))
    assert "text/html" in request.headers['Content-type']
