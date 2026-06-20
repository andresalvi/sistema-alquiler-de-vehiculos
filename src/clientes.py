# clientes.py
"""
Capa de Dominio y Gestión de Clientes.
Administra el ciclo CRUD completo para las identidades del sistema.
"""

from typing import Dict, Tuple, Optional
from src.config import ARCHIVO_CLIENTES
from src.repository import cargar_datos, guardar_datos
from src.models import LONGITUD_DUI  # Importamos la constante 

def inicializar_clientes() -> dict:
    """Carga los clientes desde disco. Inicializa un diccionario vacío en caso de ausencia."""
    clientes = cargar_datos(ARCHIVO_CLIENTES, "clientes")
    if not isinstance(clientes, dict):
        clientes = {}
        guardar_datos(ARCHIVO_CLIENTES, clientes)
    return clientes

def registrar_cliente(dui: str, nombre: str, telefono: str, correo: str, clientes: dict) -> Tuple[bool, str]:
    """Valida la estructura del DUI e inscribe un nuevo perfil de cliente."""
    dui_limpio = dui.strip().replace("-", "")  # Remueve espacios y guiones para validar pureza numérica

    if not dui_limpio:
        return False, "Debe ingresar un documento de identidad (DUI) válido."
    
    # Validación estricta usando la constante de models.py
    if len(dui_limpio) != LONGITUD_DUI or not dui_limpio.isdigit():
        return False, f"El DUI debe contener exactamente {LONGITUD_DUI} dígitos numéricos."

    # Guardamos con el formato estándar original con guion para la visualización (Ej: 00000000-0)
    dui_formateado = f"{dui_limpio[:8]}-{dui_limpio[8:]}"

    if dui_formateado in clientes:
        return False, "Ya existe un cliente registrado con ese número de DUI."

    clientes[dui_formateado] = {
        "nombre": nombre.strip(),
        "telefono": telefono.strip(),
        "correo": correo.strip()
    }
    guardar_datos(ARCHIVO_CLIENTES, clientes)
    return True, "Cliente registrado correctamente en el sistema."

def buscar_cliente(dui: str, clientes: dict) -> Optional[dict]:
    """Recupera los atributos de un cliente manejando variaciones con o sin guion."""
    dui_limpio = dui.strip().replace("-", "")
    if len(dui_limpio) == 9:
        dui = f"{dui_limpio[:8]}-{dui_limpio[8:]}"
    return clientes.get(dui)

def editar_cliente(dui: str, nombre: str, telefono: str, correo: str, clientes: dict) -> Tuple[bool, str]:
    """Modifica de forma segura los campos específicos de un cliente."""
    dui_limpio = dui.strip().replace("-", "")
    dui_formateado = f"{dui_limpio[:8]}-{dui_limpio[8:]}" if len(dui_limpio) == 9 else dui.strip()

    if dui_formateado not in clientes:
        return False, "El cliente solicitado no existe."

    clientes[dui_formateado]["nombre"] = nombre.strip()
    clientes[dui_formateado]["telefono"] = telefono.strip()
    clientes[dui_formateado]["correo"] = correo.strip()
    
    guardar_datos(ARCHIVO_CLIENTES, clientes)
    return True, "Información del cliente actualizada correctamente."

def listar_clientes(clientes: dict) -> None:
    """Muestra en consola de forma estructurada el total de clientes cargados."""
    if not clientes:
        print("No existen clientes registrados.")
        return
    for dui, datos in clientes.items():
        print(f"👤 DUI: {dui} | Nombre: {datos['nombre']} | Tel: {datos['telefono']} | Correo: {datos['correo']}")

def eliminar_cliente(dui: str, clientes: dict, reservas: list) -> Tuple[bool, str]:
    """Remueve una entidad del sistema aplicando reglas de integridad referencial con reservas."""
    dui_limpio = dui.strip().replace("-", "")
    dui_formateado = f"{dui_limpio[:8]}-{dui_limpio[8:]}" if len(dui_limpio) == 9 else dui.strip()

    if dui_formateado not in clientes:
        return False, "El cliente solicitado no existe."

    nombre_cliente = clientes[dui_formateado]["nombre"]
    
    for res in reservas:
        if res.get("dui_cliente") == dui_formateado or res.get("cliente") == nombre_cliente:
            return False, "Restricción de Integridad: No puede eliminarse un cliente con transacciones activas."

    del clientes[dui_formateado]
    guardar_datos(ARCHIVO_CLIENTES, clientes)
    return True, "Cliente dado de baja del sistema exitosamente."