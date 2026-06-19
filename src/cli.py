# cli.py
"""
Capa de Presentación CLI (Command Line Interface).
Maneja de manera exclusiva el ciclo de vida interactivo y la captura de inputs del usuario.
"""

import sys
import os

# Truco de entorno: Añadir el directorio raíz al path de Python si se arranca desde src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
        print(f"🔹 Placa: [ {placa} ] | {datos['marca']} {datos['modelo']} ({datos['tipo']}) -> Estado: {datos['estado']}")

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

def ejecutar_realizar_reserva(vehiculos: dict, reservas: list) -> tuple:
    print(pintar_info("\n--- APARTADO Y GESTION DE RESERVAS ---"))
    cliente = input("Nombre completo del Cliente: ").strip()
    placa = input("Placa del rodaje solicitado: ").strip().upper()
    f_ini = input("Fecha de inicio del alquiler (YYYY-MM-DD): ").strip()
    f_fin = input("Fecha de cierre del alquiler (YYYY-MM-DD): ").strip()

    if not cliente or not placa:
        print(pintar_error("Datos obligatorios omitidos."))
        return vehiculos, reservas

    exito, mensaje = service.procesar_reserva(cliente, placa, f_ini, f_fin, vehiculos, reservas)
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
        print(f"{i}. Cliente: {res['cliente']} | Auto: {res['placa']} | Ciclo: {res['fecha_inicio']} a {res['fecha_fin']}")

def menu_principal():
    """Lazo de control cerrado (*Event Loop*) de la CLI."""
    vehiculos_raw = cargar_datos(ARCHIVO_VEHICULOS, "vehiculos")
    reservas_raw = cargar_datos(ARCHIVO_RESERVAS, "reservas")
    
    # Casting explícito inicializador
    vehiculos, reservas = service.inicializar_datos_ejemplo(vehiculos_raw, reservas_raw)

    while True:
        print("\n" + "="*45)
        print("    SISTEMA DE ARRENDAMIENTO AUTOMOTRIZ")
        print("="*45)
        print("1. Listar Unidades de Flota")
        print("2. Registrar Vehiculo")
        print("3. Generar Reserva de Alquiler")
        print("4. Procesar Devolucion de Vehiculo")
        print("5. Historial de Transacciones")
        print("6. Cerrar Sesion y Guardar")
        print("="*45)
        
        opcion = input("Escriba su opcion elegida: ").strip()
        
        if opcion == "1":
            ejecutar_listar_vehiculos(vehiculos)
        elif opcion == "2":
            vehiculos = ejecutar_agregar_vehiculo(vehiculos)
            guardar_datos(ARCHIVO_VEHICULOS, vehiculos)
        elif opcion == "3":
            vehiculos, reservas = ejecutar_realizar_reserva(vehiculos, reservas)
        elif opcion == "4":
            vehiculos = ejecutar_devolucion(vehiculos)
        elif opcion == "5":
            ejecutar_historial(reservas)
        elif opcion == "6":
            print(pintar_exito("Sincronizando almacenamiento físico... ¡Proceso Concluido con Éxito!"))
            break
        else:
            print(pintar_error("Opción incorrecta. Elija un dígito entre 1 y 6."))

if __name__ == "__main__":
    menu_principal()