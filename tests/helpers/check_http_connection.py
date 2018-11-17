import requests


def check_http_connection(url: str):
    """Checks, whether an http server is listening on this URL.

        :param url: URL.

    """
    request = requests.get(url)
    assert "text/html" in request.headers['Content-type']


def check_local_http_connection(port: int):
    """Checks, whether an http server is listening on this port of the local
        host.

        :param port: HTTP port.

    """
    check_http_connection("http://127.0.0.1:{port}".format(
        port=port))
