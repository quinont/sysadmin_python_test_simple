"""Main code"""

from src.configmap_source import ConfigMapSource
from src.kubernetes_adapter import KubernetesAdapter


def main(configmap_source: ConfigMapSource):
    namespaces = configmap_source.list_namespaces()

    for namespace in namespaces:
        configmaps = configmap_source.list_configmaps(namespace)
        for configmap in configmaps:
            if configmap.labels.get("syntax-checking") != "true":
                continue

            config_type = configmap.labels.get("config-type")
            if config_type == "file":
                if len(configmap.data) > 0:
                    first_key = list(configmap.data.keys())[0]
                    configmap.data = {
                        first_key: configmap.data[first_key]
                        .replace("\\n\\n", "\\n")
                        .replace("\n\n", "\n")
                    }
                else:
                    configmap.data = {"index.html": "archivo nuevo"}

            elif config_type == "env":
                new_data = {}
                for key, value in configmap.data.items():
                    key = key.upper()
                    value = value.replace("\\n", "").replace("\n", "")
                    new_data[key] = value
                if not new_data:
                    new_data = {"CLAVE": "MI VALOR"}
                configmap.data = new_data

            else:
                continue

            print(f"Modified ConfigMap: {configmap.name}")
            configmap_source.update_configmap(configmap)


if __name__ == "__main__":
    kubernetes_configmap_source = KubernetesAdapter()
    main(kubernetes_configmap_source)
