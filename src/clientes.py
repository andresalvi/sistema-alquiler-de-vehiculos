"""
Gestión de clientes y persistencia.
"""

from typing import Dict, Tuple, Optional

from src.config import ARCHIVO_CLIENTES
from src.repository import cargar_datos, guardar_datos


def inicializar_clientes() -> dict:
    """
    Carga los clientes desde disco.
    Si el archivo está vacío, retorna un diccionario vacío.
    """
    clientes = cargar_datos(ARCHIVO_CLIENTES, "clientes")

    if not isinstance(clientes, dict):
        clientes = {}
        guardar_datos(ARCHIVO_CLIENTES, clientes)

    return clientes


def registrar_cliente(
        dui: str,
        nombre: str,
        telefono: str,
        correo: str,
        clientes: dict
) -> Tuple[bool, str]:
    """
    Registra un cliente nuevo.
    """

    dui = dui.strip()

    if not dui:
        return False, "Debe ingresar un DUI."

    if dui in clientes:
        return False, "Ya existe un cliente con ese DUI."

    clientes[dui] = {
        "nombre": nombre.strip(),
        "telefono": telefono.strip(),
        "correo": correo.strip()
    }

    guardar_datos(ARCHIVO_CLIENTES, clientes)

    return True, "Cliente registrado correctamente."


def buscar_cliente(
        dui: str,
        clientes: dict
) -> Optional[dict]:
    """
    Busca un cliente por DUI.
    """

    return clientes.get(dui.strip())


def editar_cliente(
        dui: str,
        nombre: str,
        telefono: str,
        correo: str,
        clientes: dict
) -> Tuple[bool, str]:

    if dui not in clientes:
        return False, "Cliente inexistente."

    clientes[dui]["nombre"] = nombre.strip()
    clientes[dui]["telefono"] = telefono.strip()
    clientes[dui]["correo"] = correo.strip()

    guardar_datos(ARCHIVO_CLIENTES, clientes)

    return True, "Cliente actualizado correctamente."


def listar_clientes(
        clientes: dict
) -> None:

    if not clientes:
        print("No existen clientes registrados.")
        return

    for dui, datos in clientes.items():
        print(
            f"DUI: {dui} | "
            f"Nombre: {datos['nombre']} | "
            f"Teléfono: {datos['telefono']} | "
            f"Correo: {datos['correo']}"
        )


def eliminar_cliente(
        dui: str,
        clientes: dict,
        reservas: list
) -> Tuple[bool, str]:
    """
    Elimina un cliente únicamente si no posee reservas activas.
    """

    if dui not in clientes:
        return False, "Cliente inexistente."

    nombre_cliente = clientes[dui]["nombre"]

    for reserva in reservas:
        if reserva["cliente"] == nombre_cliente:
            return (
                False,
                "No puede eliminarse un cliente con reservas registradas."
            )

    del clientes[dui]

    guardar_datos(ARCHIVO_CLIENTES, clientes)

    return True, "Cliente eliminado correctamente."