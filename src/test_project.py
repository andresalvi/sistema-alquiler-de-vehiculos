# test_project.py
"""
Módulo de Verificación Automatizada (Unit Testing con pytest).
Garantiza el cumplimiento estricto de las firmas de funciones de negocio del software.
"""

from datetime import datetime
import pytest
import src.service as service
from src.models import ESTADO_DISPONIBLE, ESTADO_ALQUILADO

def test_validacion_fechas_correctas_e_incorrectas():
    """Valida los filtros temporales correctos y de orden cronológico lineal inverso."""
    # Rango en orden lineal correcto futuro
    resultado_valido = service.validar_fechas("2026-12-01", "2026-12-05")
    assert resultado_valido is not None
    assert resultado_valido[0] < resultado_valido[1]

    # Inversión cronológica inválida
    resultado_invalido = service.validar_fechas("2026-12-10", "2026-12-05")
    assert resultado_invalido is None

def test_deteccion_colision_de_fechas():
    """Valida el motor algebraico booleano contra colisiones de reserva."""
    reservas_mock = [
        {"placa": "ABC123", "fecha_inicio": "2026-07-10", "fecha_fin": "2026-07-20"}
    ]
    inicio_test = datetime.strptime("2026-07-15", "%Y-%m-%d")
    fin_test = datetime.strptime("2026-07-25", "%Y-%m-%d")

    disponible = service.verificar_disponibilidad("ABC123", inicio_test, fin_test, reservas_mock)
    assert disponible is False

def test_procesamiento_exitoso_reserva():
    """Verifica el flujo atómico integral conectando vehículos, reservas y clientes."""
    vehiculos_mock = {
        "XYZ789": {"marca": "Mazda", "modelo": "3", "tipo": "Sedán", "estado": ESTADO_DISPONIBLE}
    }
    clientes_mock = {
        "01234567-8": {"nombre": "Roberto Carlos", "telefono": "7777-7777", "correo": "roberto@mail.com"}
    }
    reservas_mock = []

    exito, mensaje = service.procesar_reserva(
        "01234567-8", "XYZ789", "2026-08-01", "2026-08-05", vehiculos_mock, reservas_mock, clientes_mock
    )
    
    assert exito is True
    assert vehiculos_mock["XYZ789"]["estado"] == ESTADO_ALQUILADO
    assert len(reservas_mock) == 1
    assert reservas_mock[0]["cliente"] == "Roberto Carlos"

def test_falla_reserva_cliente_no_registrado():
    """Asegura el rechazo transaccional preventivo ante un DUI inexistente en memoria."""
    vehiculos_mock = {
        "XYZ789": {"marca": "Mazda", "modelo": "3", "tipo": "Sedán", "estado": ESTADO_DISPONIBLE}
    }
    clientes_mock = {}  # Entorno sin clientes registrados
    reservas_mock = []

    exito, mensaje = service.procesar_reserva(
        "99999999-9", "XYZ789", "2026-08-01", "2026-08-05", vehiculos_mock, reservas_mock, clientes_mock
    )
    
    assert exito is False
    assert "no pertenece a ningún cliente registrado" in mensaje