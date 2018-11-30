import requests

from idact.core.retry import Retry
from idact.detail.helper.retry import retry_with_config
from idact.detail.tunnel.tunnel_internal import TunnelInternal


def validate_tunnel_http_connection(tunnel: TunnelInternal):
    """Checks whether there is an HTTP server replying to a request through
        the tunnel.

         :param tunnel: Tunnel to validate.

    """

    def access_server():
        with requests.Session() as session:
            return session.get("http://127.0.0.1:{local_port}".format(
                local_port=tunnel.here))

    request = retry_with_config(access_server,
                                name=Retry.VALIDATE_HTTP_TUNNEL,
                                config=tunnel.config)
    if "text/html" not in request.headers['Content-type']:
        raise RuntimeError("Unable to obtain a HTML response.")
