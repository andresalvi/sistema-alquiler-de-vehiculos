# conftest.py
"""
Configuración global de infraestructura para las pruebas unitarias (fixtures).
Garantiza el aislamiento total redirigiendo el storage a un entorno temporal volátil.
"""

import pytest
import src.config as config

@pytest.fixture(scope="function", autouse=True)
def aislar_entorno_pruebas(tmp_path):
    """
    Modifica temporalmente los punteros físicos de los JSON de persistencia hacia
    un directorio virtual transitorio para no dañar los datos reales en producción.
    """
    # Salvaguarda de rutas reales
    original_vehiculos = config.ARCHIVO_VEHICULOS
    original_reservas = config.ARCHIVO_RESERVAS
    original_clientes = config.ARCHIVO_CLIENTES

    # Redireccionamiento seguro
    config.ARCHIVO_VEHICULOS = str(tmp_path / "test_vehiculos.json")
    config.ARCHIVO_RESERVAS = str(tmp_path / "test_reservas.json")
    config.ARCHIVO_CLIENTES = str(tmp_path / "test_clientes.json")
    
    yield  # Ejecución de bloque de pruebas internas

    # Restauración post-testing (Teardown)
    config.ARCHIVO_VEHICULOS = original_vehiculos
    config.ARCHIVO_RESERVAS = original_reservas
    config.ARCHIVO_CLIENTES = original_clientes