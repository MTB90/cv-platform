import asyncio
import logging
import os
from kubernetes import config, client

logger = logging.getLogger(__name__)


class KubernetesClient:
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

    async def create_workflow(self, namespace: str, manifest: dict):
        logger.info(f"create new workflow in namespace: {namespace}")

        return await asyncio.to_thread(
            self._api_client.create_namespaced_custom_object,
            group="argoproj.io",
            version="v1alpha1",
            namespace=namespace,
            plural="workflows",
            body=manifest,
        )
