# conftest.py
"""
Configuración global de infraestructura para las pruebas unitarias (fixtures).
Garantiza el aislamiento de datos entre el entorno de pruebas y el de producción.
"""

import pytest
import os
import src.config as config

@pytest.fixture(scope="function", autouse=True)
def aislar_entorno_pruebas(tmp_path):
    """
    Fixture de nivel de función. Modifica temporalmente las rutas de los archivos JSON 
    hacia un directorio volátil temporal del sistema operativo.
    De esta forma, los tests nunca alteran las bases de datos JSON reales del proyecto.
    """
    # Guardar las rutas reales originales
    ruta_original_vehiculos = config.ARCHIVO_VEHICULOS
    ruta_original_reservas = config.ARCHIVO_RESERVAS

    # Reasignar las variables de configuración a archivos temporales aislados
    archivo_temporal_vehiculos = str(tmp_path / "test_vehiculos.json")
    archivo_temporal_reservas = str(tmp_path / "test_reservas.json")
    
    config.ARCHIVO_VEHICULOS = archivo_temporal_vehiculos
    config.ARCHIVO_RESERVAS = archivo_temporal_reservas

    # Ceder el control de ejecución al test unitario correspondiente
    yield 

    # Bloque Teardown: Restaurar configuraciones de producción al finalizar el test
    config.ARCHIVO_VEHICULOS = ruta_original_vehiculos
    config.ARCHIVO_RESERVAS = ruta_original_reservas