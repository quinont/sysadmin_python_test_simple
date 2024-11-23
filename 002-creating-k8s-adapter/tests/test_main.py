import pytest

from unittest.mock import patch, MagicMock
from src.kubernetes_adapter import KubernetesAdapter
from src.main import main


@pytest.fixture
def mock_kubernetes():
    with patch("src.kubernetes_adapter.config.load_kube_config") as mock_load_kube_config, \
         patch("src.kubernetes_adapter.client.CoreV1Api") as mock_core_v1_api:

        # Mock del CoreV1Api
        mock_api_instance = MagicMock()
        mock_core_v1_api.return_value = mock_api_instance

        # Retornar los mocks necesarios
        yield {
            "mock_load_kube_config": mock_load_kube_config,
            "mock_api_instance": mock_api_instance,
        }


def test_configmap_with_systax_checking_and_config_file_without_double_new_line(mock_kubernetes):
    mock_api_instance = mock_kubernetes["mock_api_instance"]

    # Workaround para poder agregar name al MagicMock
    namespace1 = MagicMock(metadata=MagicMock())
    namespace1.metadata.name = "Namespace1"
    mock_api_instance.list_namespace.return_value.items = [namespace1]

    # Workaround para poder agregar name al MagicMock
    configmap1 = MagicMock(metadata=MagicMock(labels={"syntax-checking": "true", "config-type": "file"}), data={"key": "value"})
    configmap1.metadata.name = "cm1"
    configmap1.metadata.namespace = "Namespace1"
    mock_api_instance.list_namespaced_config_map.side_effect = [
        MagicMock(items=[configmap1]),
    ]

    # Ejecutando metodo
    configmap_source = KubernetesAdapter()
    main(configmap_source)

    # Verificando salida
    mock_kubernetes["mock_load_kube_config"].assert_called_once()

    mock_api_instance.list_namespace.assert_called_once()
    assert mock_api_instance.list_namespaced_config_map.call_count == 1

    mock_api_instance.replace_namespaced_config_map.assert_called_once_with(
        "cm1",
        "Namespace1",
        configmap1
    )

    assert configmap1.data == {"key": "value"}


def test_configmap_with_systax_checking_and_config_file_with_double_new_line(mock_kubernetes):
    mock_api_instance = mock_kubernetes["mock_api_instance"]

    # Workaround para poder agregar name al MagicMock
    namespace1 = MagicMock(metadata=MagicMock())
    namespace1.metadata.name = "Namespace1"
    mock_api_instance.list_namespace.return_value.items = [namespace1]

    # Workaround para poder agregar name al MagicMock
    configmap1 = MagicMock(metadata=MagicMock())
    configmap1.metadata.name = "cm1"
    configmap1.metadata.namespace = "Namespace1"
    configmap1.metadata.labels = {"syntax-checking": "true", "config-type": "file"}
    configmap1.data = {"index.html": "una linea\\nOtraLinea\\n\\nDos separaciones"}
    mock_api_instance.list_namespaced_config_map.side_effect = [
        MagicMock(items=[configmap1]),
    ]

    # Ejecutando el método principal
    configmap_source = KubernetesAdapter()
    main(configmap_source)

    # Verificando Todo
    mock_kubernetes["mock_load_kube_config"].assert_called_once()

    mock_api_instance.list_namespace.assert_called_once()
    assert mock_api_instance.list_namespaced_config_map.call_count == 1

    mock_api_instance.replace_namespaced_config_map.assert_called_once_with(
        "cm1",
        "Namespace1",
        configmap1
    )

    assert configmap1.data["index.html"] == "una linea\\nOtraLinea\\nDos separaciones"


def test_configmap_with_systax_checking_and_config_file_without_data(mock_kubernetes):
    mock_api_instance = mock_kubernetes["mock_api_instance"]

    # Workaround para poder agregar name al MagicMock
    namespace1 = MagicMock(metadata=MagicMock())
    namespace1.metadata.name = "Namespace1"
    mock_api_instance.list_namespace.return_value.items = [namespace1]

    # Workaround para poder agregar name al MagicMock
    configmap1 = MagicMock(metadata=MagicMock())
    configmap1.metadata.name = "cm1"
    configmap1.metadata.namespace = "Namespace1"
    configmap1.metadata.labels = {"syntax-checking": "true", "config-type": "file"}
    configmap1.data = {}
    mock_api_instance.list_namespaced_config_map.side_effect = [
        MagicMock(items=[configmap1]),
    ]

    # Ejecutando el método principal
    configmap_source = KubernetesAdapter()
    main(configmap_source)

    # Verificando Todo
    mock_kubernetes["mock_load_kube_config"].assert_called_once()

    mock_api_instance.list_namespace.assert_called_once()
    assert mock_api_instance.list_namespaced_config_map.call_count == 1

    mock_api_instance.replace_namespaced_config_map.assert_called_once_with(
        "cm1",
        "Namespace1",
        configmap1
    )

    assert configmap1.data["index.html"] == "archivo nuevo"


def test_configmap_with_systax_checking_and_config_env_with_data(mock_kubernetes):
    mock_api_instance = mock_kubernetes["mock_api_instance"]

    # Workaround para poder agregar name al MagicMock
    namespace1 = MagicMock(metadata=MagicMock())
    namespace1.metadata.name = "Namespace1"
    mock_api_instance.list_namespace.return_value.items = [namespace1]

    # Workaround para poder agregar name al MagicMock
    configmap1 = MagicMock(metadata=MagicMock())
    configmap1.metadata.name = "cm1"
    configmap1.metadata.labels = {"syntax-checking": "true", "config-type": "env"}
    configmap1.metadata.namespace = "Namespace1"
    configmap1.data = {
        "mikey": "un valor",
        "OTRAKEY": "otro valor",
        "CONSALTO": "Con\nSalto\\nDe Linea\\n\n\n"
    }
    mock_api_instance.list_namespaced_config_map.side_effect = [
        MagicMock(items=[configmap1]),
    ]

    # Ejecutando el método principal
    configmap_source = KubernetesAdapter()
    main(configmap_source)

    # Verificando Todo
    mock_kubernetes["mock_load_kube_config"].assert_called_once()

    mock_api_instance.list_namespace.assert_called_once()
    assert mock_api_instance.list_namespaced_config_map.call_count == 1

    mock_api_instance.replace_namespaced_config_map.assert_called_once_with(
        "cm1",
        "Namespace1",
        configmap1
    )

    assert configmap1.data.get("mikey") is None
    assert configmap1.data.get("MIKEY") == "un valor"
    assert configmap1.data.get("OTRAKEY") == "otro valor"
    assert configmap1.data.get("CONSALTO") == "ConSaltoDe Linea"


def test_configmap_with_systax_checking_and_config_env_without_data(mock_kubernetes):
    mock_api_instance = mock_kubernetes["mock_api_instance"]

    # Workaround para poder agregar name al MagicMock
    namespace1 = MagicMock(metadata=MagicMock())
    namespace1.metadata.name = "Namespace1"
    mock_api_instance.list_namespace.return_value.items = [namespace1]

    # Workaround para poder agregar name al MagicMock
    configmap1 = MagicMock(metadata=MagicMock())
    configmap1.metadata.name = "cm1"
    configmap1.metadata.namespace = "Namespace1"
    configmap1.metadata.labels = {"syntax-checking": "true", "config-type": "env"}
    configmap1.data = {}
    mock_api_instance.list_namespaced_config_map.side_effect = [
        MagicMock(items=[configmap1]),
    ]

    # Ejecutando el método principal
    configmap_source = KubernetesAdapter()
    main(configmap_source)

    # Verificando Todo
    mock_kubernetes["mock_load_kube_config"].assert_called_once()

    mock_api_instance.list_namespace.assert_called_once()
    assert mock_api_instance.list_namespaced_config_map.call_count == 1

    mock_api_instance.replace_namespaced_config_map.assert_called_once_with(
        "cm1",
        "Namespace1",
        configmap1
    )

    assert configmap1.data.get("CLAVE") == "MI VALOR"


def test_configmap_without_systax(mock_kubernetes):
    mock_api_instance = mock_kubernetes["mock_api_instance"]

    # Workaround para poder agregar name al MagicMock
    namespace1 = MagicMock(metadata=MagicMock())
    namespace1.metadata.name = "Namespace1"
    mock_api_instance.list_namespace.return_value.items = [namespace1]

    # Workaround para poder agregar name al MagicMock
    configmap1 = MagicMock(metadata=MagicMock())
    configmap1.metadata.name = "cm1"
    configmap1.metadata.namespace = "Namespace1"
    configmap1.metadata.labels = {"syntax-checking": "no"}
    configmap1.data = {}
    mock_api_instance.list_namespaced_config_map.side_effect = [
        MagicMock(items=[configmap1]),
    ]

    # Ejecutando el método principal
    configmap_source = KubernetesAdapter()
    main(configmap_source)

    # Verificando Todo
    mock_kubernetes["mock_load_kube_config"].assert_called_once()

    mock_api_instance.list_namespace.assert_called_once()
    assert mock_api_instance.list_namespaced_config_map.call_count == 1

    mock_api_instance.replace_namespaced_config_map.assert_not_called()


def test_configmap_with_systax_checking_and_config_not_match(mock_kubernetes):
    mock_api_instance = mock_kubernetes["mock_api_instance"]

    # Workaround para poder agregar name al MagicMock
    namespace1 = MagicMock(metadata=MagicMock())
    namespace1.metadata.name = "Namespace1"
    mock_api_instance.list_namespace.return_value.items = [namespace1]

    # Workaround para poder agregar name al MagicMock
    configmap1 = MagicMock(metadata=MagicMock())
    configmap1.metadata.name = "cm1"
    configmap1.metadata.namespace = "Namespace1"
    configmap1.metadata.labels = {"syntax-checking": "true", "config-type": "otracosa"}
    configmap1.data = {}
    mock_api_instance.list_namespaced_config_map.side_effect = [
        MagicMock(items=[configmap1]),
    ]

    # Ejecutando el método principal
    configmap_source = KubernetesAdapter()
    main(configmap_source)

    # Verificando Todo
    mock_kubernetes["mock_load_kube_config"].assert_called_once()

    mock_api_instance.list_namespace.assert_called_once()
    assert mock_api_instance.list_namespaced_config_map.call_count == 1

    mock_api_instance.replace_namespaced_config_map.assert_not_called()


