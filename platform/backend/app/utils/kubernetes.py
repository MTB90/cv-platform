import asyncio
import logging

from kubernetes import config, client

logger = logging.getLogger(__name__)


class KubernetesClient:
    def __init__(self):
        logger.info("loading service account config")

        config.load_incluster_config()
        self._api_client = client.CustomObjectsApi()

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
