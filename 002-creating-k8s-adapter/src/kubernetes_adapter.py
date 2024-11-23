from kubernetes import client, config

from src.configmap_source import ConfigMapSource


class KubernetesAdapter(ConfigMapSource):
    def __init__(self) -> None:
        config.load_kube_config()
        self.api_instance = client.CoreV1Api()

    def list_namespaces(self):
        return [ns.metadata.name for ns in self.api_instance.list_namespace().items]

    def list_configmaps(self, namespace):
        return self.api_instance.list_namespaced_config_map(namespace).items

    def update_configmap(self, configmap):
        self.api_instance.replace_namespaced_config_map(
            configmap.metadata.name, configmap.metadata.namespace, configmap
        )
