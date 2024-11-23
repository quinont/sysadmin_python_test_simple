from abc import ABC, abstractmethod
from typing import List
from src.configmap import Configmap


class ConfigMapSource(ABC):
    @abstractmethod
    def list_namespaces(self) -> List[str]: ...

    @abstractmethod
    def list_configmaps(self, namespace: str) -> List[Configmap]: ...

    @abstractmethod
    def update_configmap(self, configmap: Configmap) -> None: ...
