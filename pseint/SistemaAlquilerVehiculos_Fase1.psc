Algoritmo SistemaAlquilerVehiculos_Fase1
    // ============================================================
    // DEFINICIÓN DE ESTRUCTURAS DE DATOS (Arreglos paralelos)
    // Capacidad máxima en esta prueba es de 5 vehículos y 10 reservas 
    Dimension vehiculos_placa[5], vehiculos_marca[5], vehiculos_estado[5]
    Dimension reservas_cliente[10], reservas_placa[10], reservas_inicio[10], reservas_fin[10]
    
    // Variables para conteo
    Definir total_vehiculos, total_reservas Como Entero
    Definir opcion, i, encontrado Como Entero
    

    // INICIALIZACIÓN DE DATOS DE EJEMPLO (Para probar)
    
    total_vehiculos <- 5
    total_reservas <- 0
    
    // Cargar 5 vehículos de ejemplo
    vehiculos_placa[1] <- "ABC123"
    vehiculos_marca[1] <- "Toyota"
    vehiculos_estado[1] <- "Disponible"
    
    vehiculos_placa[2] <- "DEF456"
    vehiculos_marca[2] <- "Honda"
    vehiculos_estado[2] <- "Disponible"
    
    vehiculos_placa[3] <- "GHI789"
    vehiculos_marca[3] <- "Chevrolet"
    vehiculos_estado[3] <- "En Mantenimiento"
    
    vehiculos_placa[4] <- "JKL012"
    vehiculos_marca[4] <- "Nissan"
    vehiculos_estado[4] <- "Disponible"
    
    vehiculos_placa[5] <- "MNO345"
    vehiculos_marca[5] <- "Ford"
    vehiculos_estado[5] <- "Alquilado"
    
    // MENÚ PRINCIPAL
    
    Repetir
        Escribir "========================"
        Escribir " SISTEMA DE ALQUILER"
        Escribir "========================"
        Escribir "1. Ver disponibilidad de vehículos"
        Escribir "2. Realizar una reserva"
        Escribir "3. Salir"
        Escribir "Seleccione una opción: "
        Leer opcion
        
        Segun opcion Hacer
            Caso 1:
                // MÓDULO 1: CONSULTAR DISPONIBILIDAD
                Escribir "--- LISTADO DE VEHÍCULOS ---"
                Para i <- 1 Hasta total_vehiculos Con Paso 1 Hacer
                    Escribir "Vehículo ", i, ": ", vehiculos_placa[i], " - ", vehiculos_marca[i], " - Estado: ", vehiculos_estado[i]
                FinPara
                
            Caso 2:
                // MÓDULO 2: REALIZAR RESERVA
                Escribir "--- NUEVA RESERVA ---"
                
                // === FASE ENTRADA (INPUT) ===
                Definir nombre_cliente Como Cadena
                Definir placa_buscar Como Cadena
                Definir dia_inicio, dia_fin Como Entero
                Definir disponible, fechas_validas Como Logico
                
                Escribir "Nombre del cliente: "
                Leer nombre_cliente
                Escribir "Placa del vehículo (ej. ABC123): "
                Leer placa_buscar
                Escribir "Día de inicio (1 a 30): "
                Leer dia_inicio
                Escribir "Día de fin (1 a 30): "
                Leer dia_fin
                
                // Validar que las fechas sean lógicas
                fechas_validas <- Verdadero
                Si dia_inicio > dia_fin Entonces
                    Escribir "ERROR: La fecha de inicio no puede ser mayor a la fecha de fin."
                    fechas_validas <- Falso
                Sino
                    Si dia_inicio < 1 O dia_inicio > 30 O dia_fin < 1 O dia_fin > 30 Entonces
                        Escribir "ERROR: Las fechas deben estar entre 1 y 30."
                        fechas_validas <- Falso
                    FinSi
                FinSi
                
                Si fechas_validas Entonces
                    // === FASE PROCESAMIENTO (PROCESS) ===
                    // 1. Buscar el vehículo por su placa
                    encontrado <- 0
                    i <- 1
                    Mientras i <= total_vehiculos Y encontrado = 0 Hacer
                        Si vehiculos_placa[i] = placa_buscar Entonces
                            encontrado <- i
                        Sino
                            i <- i + 1
                        FinSi
                    FinMientras
                    
                    Si encontrado = 0 Entonces
                        Escribir "ERROR: No existe un vehículo con la placa ", placa_buscar
                    Sino
                        // Verificar estado actual del vehículo
                        Si vehiculos_estado[encontrado] <> "Disponible" Entonces
                            Escribir "ERROR: El vehículo no está disponible actualmente. Estado: ", vehiculos_estado[encontrado]
                        Sino
                            // 2. Validar que no haya reservas que se crucen con las fechas pedidas
                            disponible <- Verdadero
                            Para i <- 1 Hasta total_reservas Con Paso 1 Hacer
                                Si reservas_placa[i] = placa_buscar Entonces
                                    // Verificar superposición de intervalos [inicio, fin]
                                    // Dos intervalos se cruzan si: (inicio1 <= fin2) Y (fin1 >= inicio2)
                                    Si (dia_inicio <= reservas_fin[i]) Y (dia_fin >= reservas_inicio[i]) Entonces
                                        disponible <- Falso
                                        Escribir "El vehículo ya está reservado del día ", reservas_inicio[i], " al ", reservas_fin[i]
                                    FinSi
                                FinSi
                            FinPara
                            
                            Si disponible = Verdadero Entonces
                                // === FASE SALIDA (OUTPUT) - Guardar reserva y actualizar estado ===
                                total_reservas <- total_reservas + 1
                                reservas_cliente[total_reservas] <- nombre_cliente
                                reservas_placa[total_reservas] <- placa_buscar
                                reservas_inicio[total_reservas] <- dia_inicio
                                reservas_fin[total_reservas] <- dia_fin
                                
                                // Cambiar estado del vehículo a "Alquilado"
                                vehiculos_estado[encontrado] <- "Alquilado"
                                
                                Escribir "¡RESERVA EXITOSA!"
                                Escribir "Cliente: ", nombre_cliente
                                Escribir "Vehículo: ", vehiculos_marca[encontrado], " (", placa_buscar, ")"
                                Escribir "Período: día ", dia_inicio, " al día ", dia_fin
                            Sino
                                Escribir "ERROR: El vehículo no está disponible en las fechas solicitadas."
                            FinSi
                        FinSi
                    FinSi
                FinSi
                
            Caso 3:
                Escribir "Saliendo del sistema..."
            De Otro Modo:
                Escribir "Opción inválida. Intente de nuevo."
        FinSegun
    Hasta Que opcion = 3
FinAlgoritmo
