import requests

from idact.core.tunnel import Tunnel
from idact.detail.helper.retry import retry


def validate_tunnel_http_connection(tunnel: Tunnel):
    """Checks whether there is an HTTP server replying to a request through
        the tunnel.

         :param tunnel: Tunnel to validate.

    """

    def access_server():
        with requests.Session() as session:
            return session.get("http://127.0.0.1:{local_port}".format(
                local_port=tunnel.here))

    request = retry(access_server,
                    retries=3,
                    seconds_between_retries=2)
    if "text/html" not in request.headers['Content-type']:
        raise RuntimeError("Unable to obtain a HTML response.")
