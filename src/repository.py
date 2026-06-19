# repository.py
"""
Capa de Persistencia (Data Access Layer).
Gestiona la lectura y escritura de estructuras serializadas en archivos JSON.
"""

import json
import os
from typing import Dict, List, Any, Union

def cargar_datos(archivo: str, tipo: str) -> Union[Dict[str, Any], List[Any]]:
    """
    Carga de forma segura flujos de datos estructurados desde un almacenamiento físico JSON.
    Implementa manejo de excepciones robusto ante fallas de Entrada/Salida o corrupción del archivo.
    """
    if not os.path.exists(archivo):
        return {} if tipo == "vehiculos" else []
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        # Cláusula de contingencia ante fallos de integridad de datos
        print(f"\n[Error de Datos] No se pudo parsear {archivo}: {e}. Estructura vacía inicializada.")
        return {} if tipo == "vehiculos" else []

def guardar_datos(archivo: str, datos: Union[Dict[str, Any], List[Any]]) -> None:
    """
    Persiste en disco un objeto en formato legible (indentado) bajo codificación UTF-8.
    """
    try:
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"\n[Excepción E/S] Falló la escritura en disco de {archivo}: {e}")