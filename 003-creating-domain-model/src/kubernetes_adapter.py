from typing import List
from kubernetes import client, config
from src.configmap import Configmap
from src.configmap_source import ConfigMapSource


class KubernetesAdapter(ConfigMapSource):
    def __init__(self) -> None:
        config.load_kube_config()
        self.api_instance = client.CoreV1Api()

    def list_namespaces(self) -> List[str]:
        return [ns.metadata.name for ns in self.api_instance.list_namespace().items]

    def list_configmaps(self, namespace) -> List[Configmap]:
        k8s_configmaps = self.api_instance.list_namespaced_config_map(namespace).items
        return [
            Configmap(
                name=cm.metadata.name,
                namespace=cm.metadata.namespace,
                labels=cm.metadata.labels or {},
                data=cm.data or {},
            )
            for cm in k8s_configmaps
        ]

    def update_configmap(self, configmap: Configmap) -> None:
        existing_cm = self.api_instance.read_namespaced_config_map(
            name=configmap.name, namespace=configmap.namespace
        )

        existing_cm.data = configmap.data

        self.api_instance.replace_namespaced_config_map(
            configmap.name, configmap.namespace, existing_cm
        )
