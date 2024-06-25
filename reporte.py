#!/usr/bin/env python3
import csv
from collections import defaultdict
import os

def procesar_archivo(ruta_archivo, tiempo_por_asignado):
    try:
        with open(ruta_archivo, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                asignado_a = row['Assigned To']
                tiempo_ejecucion_str = row['Tiempo Ejecución']
                if tiempo_ejecucion_str:
                    try:
                        tiempo_ejecucion = float(tiempo_ejecucion_str.replace(',', '.'))
                        tiempo_por_asignado[asignado_a] += tiempo_ejecucion
                    except ValueError:
                        print(f'Valor inválido para Tiempo Ejecución: {tiempo_ejecucion_str}')
        return True
    except FileNotFoundError:
        return False

def leer_tiempos():
    # Obtiene el directorio de descargas del usuario actual
    directorio_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
    ruta_descargas = os.path.join(directorio_descargas, "Mes FEBRERO.csv")
    
    # Obtiene la ruta del script actual
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    ruta_local = os.path.join(ruta_script, 'Mes FEBRERO.csv')
    
    tiempo_por_asignado = defaultdict(float)
    
    if not procesar_archivo(ruta_descargas, tiempo_por_asignado):
        print(f'La ruta {ruta_descargas} no se pudo encontrar. Intentando con la ruta local.')
        if not procesar_archivo(ruta_local, tiempo_por_asignado):
            print(f'La ruta local {ruta_local} tampoco se pudo encontrar.')
    
    return tiempo_por_asignado

def leer_asignados():
    # Obtiene la ruta del script actual
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    ruta_asignados = os.path.join(ruta_script, 'assigned_to_filter.csv')
    
    if not os.path.isfile(ruta_asignados):
        print(f'El archivo {ruta_asignados} no se pudo encontrar.')
        return set()
    
    asignados = set()
    with open(ruta_asignados, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            asignado_a = row['Assigned To']
            asignados.add(asignado_a)
    return asignados

def filtrar_resultados(tiempo_por_asignado, asignados_filtrar):
    filtrado = {asignado_a: tiempo_por_asignado.get(asignado_a, 0) for asignado_a in asignados_filtrar}
    return filtrado

def mostrar_resultados(tiempo_por_asignado):
    print("Reporte de horas:")
    for asignado_a, total_tiempo in tiempo_por_asignado.items():
        nombre = asignado_a.split('<')[0].strip()  # Extrae el nombre sin el correo electrónico
        print(f'{nombre}: {total_tiempo} horas')
    
    # Personas con más de 9 horas
    mas_nueve = [(asignado_a.split('<')[0].strip(), total_tiempo) for asignado_a, total_tiempo in tiempo_por_asignado.items() if total_tiempo > 9]
    menos_nueve = [(asignado_a.split('<')[0].strip(), total_tiempo) for asignado_a, total_tiempo in tiempo_por_asignado.items() if total_tiempo < 9]
    
    if mas_nueve or menos_nueve:
        print("\nNovedades:")

    if mas_nueve:
        print("Personas con más de 9 horas:")
        for nombre, total_tiempo in mas_nueve:
            print(f' -{nombre}: {total_tiempo} horas')

    if menos_nueve:
        print("Personas con menos de 9 horas:")
        for nombre, total_tiempo in menos_nueve:
            print(f' -{nombre}: {total_tiempo} horas')

# Mostrar los resultados filtrados
mostrar_resultados(filtrar_resultados(leer_tiempos(), leer_asignados()))
