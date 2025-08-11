import asyncio
import logging
import os

from kubernetes import config, client

logger = logging.getLogger(__name__)


class ArgoClient:
    def __init__(self):
        self._load_kubernetes_config()
        self._api_client = client.CustomObjectsApi()

    @staticmethod
    def _load_kubernetes_config():
        if os.getenv("KUBERNETES_SERVICE_HOST"):
            logger.info("loading service account config")
            config.load_incluster_config()
        else:
            logger.info("loading kube config")
            config.load_kube_config()

    async def _create_workflow(self, namespace: str, name: str, entrypoint: str, templates: list):
        logger.info(f"create new workflow in namespace: {namespace}")

        manifest = {
            "apiVersion": "argoproj.io/v1alpha1",
            "kind": "Workflow",
            "metadata": {"name": name},
            "spec": {
                "serviceAccountName": "workflow-executor",
                "entrypoint": entrypoint,
                "templates": templates,
                "ttlStrategy": {
                    "secondsAfterCompletion": 60
                },
                "podGC": {
                    "strategy": "OnPodCompletion"
                }
            }
        }

        return await asyncio.to_thread(
            self._api_client.create_namespaced_custom_object,
            group="argoproj.io",
            version="v1alpha1",
            namespace=namespace,
            plural="workflows",
            body=manifest,
        )

    async def create_formating_workflow(self, namespace: str, name: str):
        entrypoint = "formating"
        templates = [{
            "name": "formating",
            "container": {
                "image": "python:3.12-slim",
                "command": ["python", "-c"],
                "args": [
                    "import time; print('Starting sleep...'); time.sleep(10); print('Done!')"
                ]
            }
        }]
        await self._create_workflow(namespace, name, entrypoint, templates)
