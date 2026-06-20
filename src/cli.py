# cli.py
"""
Capa de Presentación CLI (Command Line Interface).
Maneja de manera exclusiva el ciclo de vida interactivo y la captura de inputs del usuario.
"""

import sys
import os

# Truco de entorno: Añadir el directorio raíz al path de Python si se arranca desde src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.clientes import (
    inicializar_clientes,
    registrar_cliente,
    buscar_cliente,
    editar_cliente,
    listar_clientes,
    eliminar_cliente
)
from src.config import ARCHIVO_VEHICULOS, ARCHIVO_RESERVAS
from src.repository import cargar_datos, guardar_datos
from src.models import ESTADO_DISPONIBLE, ESTADO_ALQUILADO, ESTADO_MANTENIMIENTO
from src.colors import pintar_exito, pintar_error, pintar_alerta, pintar_info
import src.service as service


def ejecutar_listar_vehiculos(vehiculos: dict) -> None:
    print(pintar_info("\n--- LISTADO GENERAL DE FLOTA ---"))
    if not vehiculos:
        print(pintar_alerta("Cero unidades registradas."))
        return
    for placa, datos in vehiculos.items():
        print(f"Placa: [ {placa} ] | {datos['marca']} {datos['modelo']} ({datos['tipo']}) -> Estado: {datos['estado']}")


def ejecutar_agregar_vehiculo(vehiculos: dict) -> dict:
    print(pintar_info("\n--- ALTA DE NUEVO VEHICULO ---"))
    placa = input("Identificador de Placa (Ej: ABC123): ").strip().upper()
    if not placa or placa in vehiculos:
        print(pintar_error("Error: Entrada vacia o matricula ya registrada."))
        return vehiculos

    marca = input("Marca comercial: ").strip()
    modelo = input("Modelo / Linea: ").strip()
    tipo = input("Tipologia (SUV/Sedán/PickUp): ").strip()
    print(f"Estados validos: 1. {ESTADO_DISPONIBLE} | 2. {ESTADO_MANTENIMIENTO}")
    opt_est = input("Seleccione estado inicial (por defecto Disponible): ").strip()
    estado = ESTADO_MANTENIMIENTO if opt_est == "2" else ESTADO_DISPONIBLE

    vehiculos[placa] = {"marca": marca, "modelo": modelo, "tipo": tipo, "estado": estado}
    print(pintar_exito(f"Vehiculo registrado: {placa}"))
    return vehiculos


def ejecutar_listar_clientes(clientes: dict) -> None:
    print(pintar_info("\n--- LISTADO GENERAL DE CLIENTES ---"))
    listar_clientes(clientes)


def ejecutar_agregar_cliente(clientes: dict) -> dict:
    print(pintar_info("\n--- ALTA DE NUEVO CLIENTE ---"))
    dui = input("DUI de Identificación (Ej: 00000000-0): ").strip()
    nombre = input("Nombre completo: ").strip()
    telefono = input("Número telefónico: ").strip()
    correo = input("Correo electrónico: ").strip()

    exito, mensaje = registrar_cliente(dui, nombre, telefono, correo, clientes)
    if exito:
        print(pintar_exito(mensaje))
    else:
        print(pintar_error(f"Error: {mensaje}"))
    return clientes


def ejecutar_buscar_cliente(clientes: dict) -> None:
    print(pintar_info("\n--- BUSQUEDA ESPECIFICA DE CLIENTE ---"))
    dui = input("Ingrese el DUI del cliente a consultar: ").strip()
    datos = buscar_cliente(dui, clientes)
    if datos:
        print(pintar_exito(f"Encontrado -> Nombre: {datos['nombre']} | Tel: {datos['telefono']} | Correo: {datos['correo']}"))
    else:
        print(pintar_error("No se encontró ningún cliente vinculado a ese documento."))


def ejecutar_editar_cliente(clientes: dict) -> dict:
    print(pintar_info("\n--- EDICION DE DATOS DE CLIENTE ---"))
    dui = input("Ingrese el DUI del cliente que desea actualizar: ").strip()
    datos = buscar_cliente(dui, clientes)
    if not datos:
        print(pintar_error("El cliente referenciado no existe."))
        return clientes

    print(pintar_alerta(f"Modificando registro actual de: {datos['nombre']}"))
    nombre = input(f"Nombre [{datos['nombre']}]: ").strip() or datos['nombre']
    telefono = input(f"Teléfono [{datos['telefono']}]: ").strip() or datos['telefono']
    correo = input(f"Correo [{datos['correo']}]: ").strip() or datos['correo']

    exito, mensaje = editar_cliente(dui, nombre, telefono, correo, clientes)
    if exito:
        print(pintar_exito(mensaje))
    else:
        print(pintar_error(mensaje))
    return clientes


def ejecutar_eliminar_cliente(clientes: dict, reservas: list) -> dict:
    print(pintar_info("\n--- REMOCION DE CLIENTE DEL SISTEMA ---"))
    dui = input("Ingrese el DUI del cliente a dar de baja: ").strip()
    exito, mensaje = eliminar_cliente(dui, clientes, reservas)
    if exito:
        print(pintar_exito(mensaje))
    else:
        print(pintar_error(mensaje))
    return clientes


def ejecutar_realizar_reserva(vehiculos: dict, reservas: list, clientes: dict) -> tuple:
    print(pintar_info("\n--- APARTADO Y GESTION DE RESERVAS ---"))
    dui_cliente = input("DUI del Cliente Registrado: ").strip()
    
    # Recordatorio de placas disponibles en tiempo real
    print(pintar_info("\n--- UNIDADES DISPONIBLES PARA SELECCIÓN ---"))
    unidades_disponibles = False
    for placa_id, datos_v in vehiculos.items():
        if datos_v["estado"] == ESTADO_DISPONIBLE:
            print(f"Placa: [ {placa_id} ] -> {datos_v['marca']} {datos_v['modelo']} ({datos_v['tipo']})")
            unidades_disponibles = True
            
    if not unidades_disponibles:
        print(pintar_alerta("Advertencia: No hay vehículos disponibles en este momento."))
    print("-" * 45)

    placa = input("Placa de vehiculo solicitado: ").strip().upper()
    f_ini = input("Fecha de inicio del alquiler (YYYY-MM-DD): ").strip()
    f_fin = input("Fecha de cierre del alquiler (YYYY-MM-DD): ").strip()

    if not dui_cliente or not placa:
        print(pintar_error("Datos obligatorios omitidos."))
        return vehiculos, reservas

    exito, mensaje = service.procesar_reserva(dui_cliente, placa, f_ini, f_fin, vehiculos, reservas, clientes)
    if exito:
        print(pintar_exito(f"OK {mensaje}"))
        guardar_datos(ARCHIVO_VEHICULOS, vehiculos)
        guardar_datos(ARCHIVO_RESERVAS, reservas)
    else:
        print(pintar_error(f"x Requisito Violado: {mensaje}"))
    
    return vehiculos, reservas


def ejecutar_devolucion(vehiculos: dict) -> dict:
    print(pintar_info("\n--- RETORNO Y RECEPCIÓN DE VEHÍCULOS ---"))
    placa = input("Ingrese la placa de la unidad entregada: ").strip().upper()
    if placa not in vehiculos:
        print(pintar_error("El vehiculo referenciado no pertenece a la empresa."))
        return vehiculos

    if vehiculos[placa]["estado"] != ESTADO_ALQUILADO:
        print(pintar_alerta(f"Transaccion invalida. El estado es: {vehiculos[placa]['estado']}"))
        return vehiculos

    vehiculos[placa]["estado"] = ESTADO_DISPONIBLE
    print(pintar_exito(f"Unidad {placa} liberada de obligaciones contractuales. Estado: {ESTADO_DISPONIBLE}"))
    guardar_datos(ARCHIVO_VEHICULOS, vehiculos)
    return vehiculos


def ejecutar_historial(reservas: list) -> None:
    print(pintar_info("\n--- BITACORA HISTORICA DE CONTRATOS ---"))
    if not reservas:
        print(pintar_alerta("Historial sin transacciones registradas."))
        return
    for i, res in enumerate(reservas, 1):
        print(f"{i}. Cliente: {res['cliente']} (DUI: {res.get('dui_cliente', 'N/A')}) | Auto: {res['placa']} | Ciclo: {res['fecha_inicio']} a {res['fecha_fin']}")


def menu_principal():
    """Lazo de control cerrado (*Event Loop*) de la CLI."""
    clientes = inicializar_clientes()
    vehiculos_raw = cargar_datos(ARCHIVO_VEHICULOS, "vehiculos")
    reservas_raw = cargar_datos(ARCHIVO_RESERVAS, "reservas")
    
    # Casting inicializador
    vehiculos, reservas = service.inicializar_datos_ejemplo(vehiculos_raw, reservas_raw)

    while True:
        print("\n" + "="*45)
        print("       SISTEMA DE ALQUILER DE VEHICULOS")
        print("="*45)
        print("1. Listar Unidades de Flota")
        print("2. Registrar Vehiculo")
        print("3. Listar Clientes")
        print("4. Registrar Cliente")
        print("5. Buscar Cliente por DUI")
        print("6. Editar Datos de Cliente")
        print("7. Eliminar Cliente")
        print("8. Generar Reserva de Alquiler de Vehiculo")
        print("9. Procesar Devolucion de Vehiculo")
        print("10. Historial de Transacciones")
        print("11. Cerrar Sesion y Guardar")
        print("="*45)
        
        opcion = input("Escriba su opcion elegida: ").strip()
        
        if opcion == "1":
            ejecutar_listar_vehiculos(vehiculos)
        elif opcion == "2":
            vehiculos = ejecutar_agregar_vehiculo(vehiculos)
            guardar_datos(ARCHIVO_VEHICULOS, vehiculos)
        elif opcion == "3":
            ejecutar_listar_clientes(clientes)
        elif opcion == "4":
            clientes = ejecutar_agregar_cliente(clientes)
        elif opcion == "5":
            ejecutar_buscar_cliente(clientes)
        elif opcion == "6":
            clientes = ejecutar_editar_cliente(clientes)
        elif opcion == "7":
            clientes = ejecutar_eliminar_cliente(clientes, reservas)
        elif opcion == "8":
            vehiculos, reservas = ejecutar_realizar_reserva(vehiculos, reservas, clientes)
        elif opcion == "9":
            vehiculos = ejecutar_devolucion(vehiculos)
        elif opcion == "10":
            ejecutar_historial(reservas)
        elif opcion == "11":
            print(pintar_exito("Sincronizando almacenamiento físico... ¡Proceso Concluido con Éxito!"))
            break
        else:
            print(pintar_error("Opción incorrecta. Elija un dígito entre 1 y 11."))


if __name__ == "__main__":
    menu_principal()