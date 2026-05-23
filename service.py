# service.py
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from models import ESTADO_DISPONIBLE, ESTADO_ALQUILADO
from config import FORMATO_FECHA

def validar_fechas(fecha_inicio_str, fecha_fin_str):
    # ... (código completo)

def verificar_disponibilidad(vehiculo_placa, inicio, fin, reservas):
    # ... (código completo)

def realizar_reserva_logic(vehiculos, reservas, cliente, placa, fecha_inicio_str, fecha_fin_str):
    # Lógica pura, sin input() ni print() (solo retorna éxito/error y datos modificados)
    # ... (adaptar la función del monólito)
