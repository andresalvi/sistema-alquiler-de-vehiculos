# test_project.py
"""
Módulo de Verificación Automatizada (Unit Testing con pytest).
Valida las aserciones de lógica algorítmica críticas de la fase de evaluación.
"""

from datetime import datetime
import pytest
import src.service as service
from src.models import ESTADO_DISPONIBLE, ESTADO_ALQUILADO

def test_validacion_fechas_correctas_e_incorrectas():
    """Caso Integrante 1: Verifica el parsing y cláusula de guarda de inversión cronológica."""
    # Fechas válidas en orden lineal futuro (asumiendo año vigente o posterior)
    resultado_valido = service.validar_fechas("2026-12-01", "2026-12-05")
    assert resultado_valido is not None
    assert resultado_valido[0] < resultado_valido[1]

    # Fecha fin menor que fecha inicio (Inversión cronológica)
    resultado_invalido = service.validar_fechas("2026-12-10", "2026-12-05")
    assert resultado_invalido is None

def test_deteccion_colision_de_fechas():
    """Caso Integrante 2: Verifica que el algoritmo detecte cruces de reservas existentes."""
    reservas_mock = [
        {"placa": "ABC123", "fecha_inicio": "2026-07-10", "fecha_fin": "2026-07-20"}
    ]
    inicio_test = datetime.strptime("2026-07-15", "%Y-%m-%d")
    fin_test = datetime.strptime("2026-07-25", "%Y-%m-%d")

    # Debería retornar False debido a que se solapan del 15 al 20
    disponible = service.verificar_disponibilidad("ABC123", inicio_test, fin_test, reservas_mock)
    assert disponible is False

def test_procesamiento_exitoso_reserva():
    """Caso Integrante 3: Valida el ciclo completo de mutación de estado lógico de una unidad."""
    vehiculos_mock = {
        "XYZ789": {"marca": "Mazda", "modelo": "3", "tipo": "Sedán", "estado": ESTADO_DISPONIBLE}
    }
    reservas_mock = []

    exito, mensaje = service.procesar_reserva(
        "Roberto Carlos", "XYZ789", "2026-08-01", "2026-08-05", vehiculos_mock, reservas_mock
    )
    
    assert exito is True
    # El estado interno del vehículo debió mutar transaccionalmente a Alquilado
    assert vehiculos_mock["XYZ789"]["estado"] == ESTADO_ALQUILADO
    assert len(reservas_mock) == 1