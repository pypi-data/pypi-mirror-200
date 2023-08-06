from .app import ResourceUsageProxyExtensionApp


__version__ = "0.1.1"


def _jupyter_server_extension_points():  # pragma: no cover
    return [
        {
            "module": "jupyter_resource_usage_proxy.app",
            "app": ResourceUsageProxyExtensionApp,
        },
    ]
