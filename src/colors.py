# colors.py
"""
Módulo utilitario para estilizado de la interfaz de consola (CLI).
Aplica estilos ANSI para optimizar la legibilidad en terminales modernas.
"""

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

def pintar_exito(texto: str) -> str:
    return f"{GREEN}{texto}{RESET}"

def pintar_error(texto: str) -> str:
    return f"{RED}{texto}{RESET}"

def pintar_alerta(texto: str) -> str:
    return f"{YELLOW}{texto}{RESET}"

def pintar_info(texto: str) -> str:
    return f"{CYAN}{texto}{RESET}"