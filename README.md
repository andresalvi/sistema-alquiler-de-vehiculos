Sistema de Alquiler de Vehículos

Proyecto académico para la asignatura Lógica de Programación.  
Ingeniería en Desarrollo de Software  
Universidad de El Salvador, Facultad Multidisciplinaria de Occidente

## Descripción

Sistema de gestión de alquiler de vehículos ejecutable en línea de comandos (CLI).  
Permite administrar un parque vehicular, realizar reservas con validación de disponibilidad por fechas, registrar devoluciones y persistir los datos en archivos JSON.

El desarrollo se divide en dos fases:

- **Fase 1**: Algoritmo en pseudocódigo (PSeInt) que demuestra la lógica de negocio y las validaciones.
- **Fase 2**: Implementación completa en Python aplicando fundamentos teóricos: estructuras de datos, modularidad, persistencia y principios de código limpio.

## Características

- Listar todos los vehículos con su estado (Disponible, Alquilado, En Mantenimiento)
- Agregar nuevos vehículos al catálogo
- Realizar reservas con validación de disponibilidad en un rango de fechas
- Devolver vehículos, actualizando su estado automáticamente
- Ver historial completo de reservas
- Persistencia automática en archivos JSON (los datos no se pierden al cerrar el programa)
- Código modular con separación de responsabilidades (clean code, DRY)

## Tecnologías y herramientas

- Python 3.10+ (tipado dinámico, fuerte, estructuras de datos nativas)
- Módulos estándar: json, datetime, os, typing
- PSeInt (para la Fase 1, opcional)
- Git para control de versiones

LOGICAPROYECTOALQUILER/
├── .venv/ # Entorno virtual de Python
├── pseint/ # Pseudocódigo de la Fase 1
│ └── SistemaAlquilerVehiculos_Fase1.psc
├── tests/ # Pruebas unitarias (futura Fase 3)
├── cli.py # Interfaz de línea de comandos (punto de entrada)
├── colors.py # (opcional) Colores para la terminal
├── config.py # Constantes (rutas, formato de fecha)
├── db.py # Persistencia (carga y guardado JSON)
├── models.py # Definición de constantes de estado
├── service.py # Lógica de negocio pura
├── repository.py # (opcional) Acceso a datos
├── requirements.txt # Dependencias (actualmente vacío)
├── .gitignore # Archivos ignorados por Git
└── README.md #
-----------------+
## Instalación y ejecución
