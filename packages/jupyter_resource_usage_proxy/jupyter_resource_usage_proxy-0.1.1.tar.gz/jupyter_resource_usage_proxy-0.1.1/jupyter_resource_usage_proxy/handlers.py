import httpx
from tornado import web

from jupyter_server.auth.decorator import authorized
from jupyter_server.base.handlers import APIHandler


class ResourceUsageHandler(APIHandler):
    @web.authenticated
    async def get(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.settings['resource_usage_proxy_url']}/api/metrics/v1")
        self.set_status(response.status_code)
        self.finish(response.text)


default_handlers = [
    (r"/api/metrics/v1", ResourceUsageHandler),
]
