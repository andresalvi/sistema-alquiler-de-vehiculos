# service.py
"""
Capa de Servicios Lógicos de Negocio (Domain Logic Layer).
Aplica abstracciones, algoritmos de colisión de fechas y mutaciones de estado puras.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from src.config import FORMATO_FECHA
from src.models import ESTADO_DISPONIBLE, ESTADO_ALQUILADO, ESTADO_MANTENIMIENTO
from src.repository import guardar_datos
from src.config import ARCHIVO_VEHICULOS, ARCHIVO_RESERVAS

def inicializar_datos_ejemplo(vehiculos: Dict, reservas: List) -> Tuple[Dict, List]:
    """Inicializa registros ficticios bajo demandas del ciclo académico si el storage esta virgen."""
    if not vehiculos:
        vehiculos = {
            "ABC123": {"marca": "Toyota", "modelo": "Corolla", "tipo": "Sedán", "estado": ESTADO_DISPONIBLE},
            "DEF456": {"marca": "Honda", "modelo": "Civic", "tipo": "Sedán", "estado": ESTADO_DISPONIBLE},
            "GHI789": {"marca": "Chevrolet", "modelo": "Spark", "tipo": "Hatchback", "estado": ESTADO_MANTENIMIENTO},
            "JKL012": {"marca": "Nissan", "modelo": "X-Trail", "tipo": "SUV", "estado": ESTADO_DISPONIBLE},
            "MNO345": {"marca": "Ford", "modelo": "Fiesta", "tipo": "Hatchback", "estado": ESTADO_ALQUILADO}
        }
        guardar_datos(ARCHIVO_VEHICULOS, vehiculos)
    if not reservas:
        reservas = []
        guardar_datos(ARCHIVO_RESERVAS, reservas)
    return vehiculos, reservas

def validar_fechas(fecha_inicio_str: str, fecha_fin_str: str) -> Optional[Tuple[datetime, datetime]]:
    """
    Parsea cadenas a objetos datetime evaluando reglas restrictivas temporales.
    Aplica cláusulas de guarda (*Guard Clauses*) para abortar flujos erróneos tempranamente.
    """
    try:
        inicio = datetime.strptime(fecha_inicio_str, FORMATO_FECHA)
        fin = datetime.strptime(fecha_fin_str, FORMATO_FECHA)
    except ValueError:
        return None  # Formato incorrecto detectado

    if inicio > fin:
        return None  # Inconsistencia lógica lineal de tiempo

    hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if inicio < hoy:
        return None  # Restricción de negocio: Prohibido reservar en el pasado

    return inicio, fin

def verificar_disponibilidad(vehiculo_placa: str, inicio: datetime, fin: datetime, reservas: List[Dict[str, Any]]) -> bool:
    """
    Evalúa solapamientos de intervalos cerrados de fechas utilizando álgebra booleana.
    Fórmula de colisión de intervalos: (InicioA <= FinB) AND (FinA >= InicioB)
    """
    for res in reservas:
        if res["placa"] == vehiculo_placa:
            res_inicio = datetime.strptime(res["fecha_inicio"], FORMATO_FECHA)
            res_fin = datetime.strptime(res["fecha_fin"], FORMATO_FECHA)
            
            # Condición crítica de solapamiento temporal
            if inicio <= res_fin and fin >= res_inicio:
                return False
    return True

def procesar_reserva(dui_cliente: str, placa: str, f_ini: str, f_fin: str, vehiculos: Dict, reservas: List, clientes: Dict) -> Tuple[bool, str]:
    """
    Procesa de manera atómica la lógica pura de la reserva sin intervención directa de inputs de consola.
    Retorna una tupla (EstadoBooleano de éxito, MensajeDescriptivo).
    """
    # Cláusula de guarda: Validar existencia del cliente
    if dui_cliente not in clientes:
        return False, f"El DUI '{dui_cliente}' no pertenece a ningún cliente registrado."

    if placa not in vehiculos:
        return False, f"La placa {placa} no se encuentra dada de alta en el sistema."

    if vehiculos[placa]["estado"] != ESTADO_DISPONIBLE:
        return False, f"Vehículo no disponible para arriendo directo. Estado actual: {vehiculos[placa]['estado']}"

    fechas = validar_fechas(f_ini, f_fin)
    if not fechas:
        return False, "Fechas inconsistentes, vencidas o formato erroneo (Debe ser YYYY-MM-DD)."

    inicio, fin = fechas
    if not verificar_disponibilidad(placa, inicio, fin, reservas):
        return False, "Conflicto temporal: El vehiculo ya cuenta con reservas activas en ese rango."

    # Bloque transaccional simulado sobre estructuras de memoria internas
    nueva_reserva = {
        "cliente": clientes[dui_cliente]["nombre"],
        "dui_cliente": dui_cliente,
        "placa": placa,
        "fecha_inicio": f_ini,
        "fecha_fin": f_fin,
        "fecha_reserva": datetime.now().strftime(FORMATO_FECHA)
    }
    reservas.append(nueva_reserva)
    vehiculos[placa]["estado"] = ESTADO_ALQUILADO
    
    return True, "Reserva confirmada exitosamente."