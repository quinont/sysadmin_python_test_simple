from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Configmap():
    name: str
    namespace: str
    labels: Dict[str, str] = field(default_factory=dict)
    data: Dict[str, str] = field(default_factory=dict)
