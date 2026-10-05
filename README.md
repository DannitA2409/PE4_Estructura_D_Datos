# Búsqueda de vuelos de costo mínimo

Práctica 04 de árboles y grafos. Datos ficticios, USD enteros.
Requiere Python 3.12 o posterior; sin paquetes externos.

## Ejecución

python vuelos.py --listar
python vuelos.py --desde GYE --hasta SCL
python vuelos.py --desde SCL --hasta GYE
python verificar.py

El archivo vuelos.csv contiene 6 aeropuertos y 11 rutas dirigidas.
No se modelan horarios, tasas, disponibilidad ni aerolíneas.
El algoritmo usa listas de adyacencia, Dijkstra y un min-heap.
verificar.py compara 36 pares con un oráculo exhaustivo y mide
30 lotes de 1000 consultas tras 1000 consultas de calentamiento.
mediciones.json conserva el resultado de la ejecución original.
Las mediciones nuevas dependen del equipo y reemplazan ese archivo.

## Repositorio

El ZIP incluye el directorio .git y un commit local verificable.
Tras extraer: git log --oneline y git status --short.

## Uso de IA

Codex en ChatGPT generó el 100 % del código Python del proyecto.
Se ejecutaron y comprobaron el programa y sus pruebas.
