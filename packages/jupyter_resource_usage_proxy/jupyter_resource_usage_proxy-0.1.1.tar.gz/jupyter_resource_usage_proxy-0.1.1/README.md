# Jupyter Resource Usage Proxy

In one terminal/environment:

```console
pip install fps_uvicorn
pip install fps_resource_usage
pip install fps-noauth

# launch a terminal server at http://127.0.0.1:8000
fps-uvicorn --port=8000 --no-open-browser
```

In another terminal/environment:

```console
pip install jupyter_resource_usage
pip install jupyter_resource_usage_proxy
pip install jupyterlab

# launch JupyterLab at http://127.0.0.1:8888, deactivate the resource usage server extension, and proxy resource usage at http://127.0.0.1:8000
jupyter lab --port=8888 --ServerApp.jpserver_extensions="jupyter_resource_usage=False" --ResourceUsageProxyExtensionApp.proxy_url='http://127.0.0.1:8000'
```

Resource usage should now be served from http://127.0.0.1:8000.
