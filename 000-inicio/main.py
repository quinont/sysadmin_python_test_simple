from kubernetes import client, config

def main():
    config.load_kube_config()
    api_instance = client.CoreV1Api()
    namespaces = [ns.metadata.name for ns in api_instance.list_namespace().items]

    for namespace in namespaces:
        configmaps = api_instance.list_namespaced_config_map(namespace).items
        for configmap in configmaps:
            name = configmap.metadata.name
            labels = configmap.metadata.labels or {}

            if labels.get("syntax-checking") != "true":
                continue

            config_type = labels.get("config-type")
            if config_type == "file":
                if len(configmap.data) > 0:
                    first_key = list(configmap.data.keys())[0]
                    configmap.data = {first_key: configmap.data[first_key].replace("\\n\\n", "\\n").replace("\n\n", "\n")}
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

            print(f"Modified ConfigMap: {name}")
            api_instance.replace_namespaced_config_map(name, namespace, configmap)

if __name__ == "__main__":
    main()
