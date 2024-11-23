from abc import ABC, abstractmethod

class ConfigMapSource(ABC):
    @abstractmethod
    def list_namespaces(self):
        ...

    @abstractmethod
    def list_configmaps(self, namespace):
        ...

    @abstractmethod
    def update_configmap(self, configmap):
        ...