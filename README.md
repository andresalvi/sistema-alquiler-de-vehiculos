Sistema de Alquiler de Vehículos

Proyecto académico para la asignatura Lógica de Programación135  
Ingeniería en Desarrollo de Software  
Universidad de El Salvador, Facultad Multidisciplinaria de Occidente

## Integrantes
Gerardo Andrés Rodriguez Herrador RH19056
Ramon fernando Panameño Rivas PR07005

## Descripción

Sistema de gestión de alquiler de vehículos ejecutable en línea de comandos (CLI).  
Permite administrar un lote vehicular, realizar reservas con validación de disponibilidad por fechas, registrar devoluciones y persistir los datos en archivos JSON.

El desarrollo se divide en 3 fases:

Fase 1: Algoritmo en pseudocódigo (PSeInt) que demuestra la lógica de negocio y las validaciones.
Fase 2: Implementación completa en Python aplicando fundamentos teóricos: estructuras de datos, modularidad, persistencia y principios de código limpio.
Fase 3: INTERFAZ CLI FASE 3

## Características

- Listar todos los vehículos con su estado (Disponible, Alquilado, En Mantenimiento)
- Agregar nuevos vehículos al catálogo
- Realizar reservas con validación de disponibilidad en un rango de fechas
- Devolver vehículos, actualizando su estado automáticamente
- Ver historial completo de reservas
- Persistencia automática en archivos JSON (los datos no se pierden al cerrar el programa)
- Código modular con separación de responsabilidades (clean code, DRY)

## Tecnologías y herramientas (fase1-2)

- Python 3.10+ (tipado dinámico, fuerte, estructuras de datos nativas)
- Módulos estándar: json, datetime, os, typing
- PSeInt (para la Fase 1, opcional)
- Git para control de versiones

SISTEMA-ALQUILER-DE-VEHICULOS/
├── .venv/ # Entorno virtual de Python
├── pseint/ # Pseudocódigo de la Fase 1
│ └── SistemaAlquilerVehiculos_Fase1.psc
├── tests/ # Pruebas unitarias (futura Fase 3)
├── cli.py # Interfaz de línea de comandos (punto de entrada)
├── colors.py # (opcional) Colores para la terminal
├── config.py # Constantes (rutas, formato de fecha)
├── models.py # Definición de constantes de estado
├── service.py # Lógica de negocio pura
├── repository.py # (opcional) Acceso a datos
├── requirements.txt # Dependencias
├── .gitignore # Archivos ignorados por Git
└── README.md #

# Sistema de Alquiler de Vehículos (CLI) - Fase 3

Aplicación empresarial interactiva en modo consola desarrollada en Python. El sistema implementa una arquitectura multicapa para el control transaccional de alquileres de flota vehicular, validación algorítmica de solapamiento de fechas y persistencia de datos orientada a documentos mediante archivos estructurados JSON.


Este sistema es una solución de software empresarial en modo consola (CLI) diseñada bajo el paradigma modular y el patrón arquitectónico por capas. Aplica de manera rigurosa el modelo **IPO (Input-Process-Output)**, garantizando una separación limpia entre la interfaz de usuario, la lógica de negocio y la persistencia de datos orientada a documentos (JSON).

---

##  Tecnologías Utilizadas

El ecosistema tecnológico del proyecto ha sido seleccionado para garantizar un desarrollo moderno, ligero y altamente testeable sin dependencias complejas de bases de datos tradicionales:

1.	Python 3.10+: Lenguaje de programación principal, aprovechando su tipado estático opcional (`typing`) para la robustez del código.
2.	JSON (JavaScript Object Notation): Formato de serialización ligero utilizado como mecanismo de persistencia de datos en archivos planos (`vehiculos.json` y `reservas.json`).
3.	Módulo Datetime: Biblioteca nativa de Python empleada para el parsing, formateo y cálculo de álgebra de intervalos temporales.
4.	Pytest: Framework avanzado de automatización de pruebas unitarias utilizado para validar la integridad de las reglas del negocio.
5.	Códigos de Escape ANSI: Tecnología de formateo cromático por terminal para optimizar la experiencia de usuario (UX).

---

##  Funcionalidades Implementadas

El sistema cubre de manera integrada el ciclo de vida operativo del arrendamiento automotriz, cumpliendo al 100% con las reglas de negocio establecidas:

•	Gestión de Flota (Alta y Consulta): Registro secuencial de vehículos validando duplicidad de matrículas y asignación de estados lógicos invariables (*Disponible*, *Alquilado*, *En Mantenimiento*).
•	Control Transaccional de Reservas: Motor de asignación automatizada que valida la disponibilidad de una unidad específica evaluando colisiones de fechas.
•	Cálculo de Superposición Temporal: Algoritmo booleano capaz de detectar si un vehículo cuenta con cruces de horarios en el rango solicitado
•	Recepción y Retorno de Unidades: Módulo de devoluciones que libera el estado del rodaje volviéndolo a colocar como *Disponible* de manera inmediata.
•	Bitácora Histórica: Reporte cronológico y numerado de todos los contratos y reservas emitidos en el sistema.

---

##  Interfaz CLI (Command Line Interface)

La capa de presentación (`src/cli.py`) se compone de un lazo de control cerrado (*Event Loop*) que renderiza un menú interactivo conducido por opciones numéricas. 

### Características de Diseño UX en Terminal:
•	Legibilidad Cromática: Uso de la librería utilitaria `colors.py` para codificar las respuestas del sistema mediante colores semánticos (Verde para éxitos, Rojo para errores severos, Amarillo para advertencias críticas y Cian para cabeceras informativas).
•	Sanitización de Entradas: Limpieza automática de espacios en blanco no deseados (`.strip()`) y conversión homogénea de caracteres a mayúsculas (`.upper()`) en identificadores clave como las placas.

##  Arquitectura del Sistema
El software está estructurado bajo los principios de **Separación de Responsabilidades (SoC)** y diseño guiado por capas:
•	`src/cli.py`: Capa de interacción y orquestación con el usuario (Interfaz Gráfica por Consola).
•	`src/service.py`: Capa lógica del dominio que gobierna las reglas operativas del negocio.
•	`src/repository.py`: Capa de abstracción de datos para el almacenamiento físico persistente.
•	`src/config.py` y `src/models.py`: Declaraciones estáticas del ecosistema.

---
# Manejo De errores y excepciones
Para migrar de un script convencional a un software robusto de producción, se reemplazaron los colapsos inesperados del programa por un sistema de **atrapado y traducción de excepciones**. Cuando el sistema intercepta una falla técnica interna, la procesa y le muestra un **mensaje amigable, descriptivo y guiado** al usuario:

•	Robustez en E/S (Entrada/Salida):Al leer o escribir archivos JSON, el sistema captura excepciones de tipo `IOError` o `json.JSONDecodeError` (archivos corruptos). En lugar de romper la ejecución, el programa notifica la anomalía con colores de alerta e inicializa de manera segura una estructura vacía en memoria para no interrumpir la operación del negocio.
•	Cláusulas de Guarda (*Guard Clauses*): Se implementaron validaciones previas para abortar flujos inválidos antes de procesar cálculos costosos (ej. evitar nombres de clientes vacíos, formatos de fecha incorrectos o placas inexistentes).
•	Restricciones de Tiempo Real: El motor de reservas rechaza amigablemente transacciones con fechas del pasado o cronologías invertidas (donde la fecha de inicio es posterior a la fecha de finalización).

#  Requisitos e Instalación

*HTTPS*

git clone https://github.com/andresalvi/sistema-alquiler-de-vehiculos

*ejecutar en el sistema*
python main.py

# 1. Clonación del Repositorio e Instanciación del Entorno

Garantice tener instalado Python 3.10 o superior en su estación de trabajo. Active su entorno virtual aislado (`.venv`) ejecutando en su terminal:

```bash
# Windows (Powershell)
.venv\Scripts\Activate.ps1

# Linux / MacOS
source .venv/bin/activate


# **Instalar dependencias del ecosistema**

pip install -r requirements.txt

#Lanzar la aplicación CLI
Inicie el programa principal ejecutando el módulo de interfaz:

python src/cli.py