from jupyter_server.extension.application import ExtensionApp
from traitlets import Unicode

from . import handlers


class ResourceUsageProxyExtensionApp(ExtensionApp):

    name = "jupyter_resource_usage_proxy"

    proxy_url = Unicode(
        help="The URL from where to proxy resource usage."
    ).tag(config=True)

    def initialize_settings(self):
        self.settings.update(dict(resource_usage_proxy_url=self.proxy_url))

    def initialize_handlers(self):
        self.handlers.extend(handlers.default_handlers)
