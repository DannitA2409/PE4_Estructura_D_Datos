import argparse
import csv
import heapq
from pathlib import Path


def cargar(ruta):
    grafo = {}
    with open(ruta, encoding="utf-8", newline="") as f:
        lector = csv.DictReader(f)
        if lector.fieldnames != ["origen", "destino", "usd"]:
            raise ValueError("Cabecera CSV incorrecta")
        for fila in lector:
            a = fila["origen"].strip().upper()
            b = fila["destino"].strip().upper()
            precio = int(fila["usd"])
            if not a or not b or precio < 0:
                raise ValueError("Ruta o precio inválidos")
            grafo.setdefault(a, []).append((b, precio))
            grafo.setdefault(b, [])
    if not grafo:
        raise ValueError("Base vacía")
    return grafo


def buscar(grafo, origen, destino):
    if origen not in grafo or destino not in grafo:
        raise ValueError("Aeropuerto desconocido")
    dist = {origen: 0}
    previo = {}
    cola = [(0, origen)]
    while cola:
        costo, actual = heapq.heappop(cola)
        if costo != dist[actual]:
            continue
        if actual == destino:
            camino = [actual]
            while actual != origen:
                actual = previo[actual]
                camino.append(actual)
            return costo, camino[::-1]
        for vecino, precio in grafo[actual]:
            nuevo = costo + precio
            if nuevo < dist.get(vecino, float("inf")):
                dist[vecino] = nuevo
                previo[vecino] = actual
                heapq.heappush(cola, (nuevo, vecino))
    return None, []


def main():
    p = argparse.ArgumentParser()
    base = Path(__file__).with_name("vuelos.csv")
    p.add_argument("--datos", default=str(base))
    p.add_argument("--listar", action="store_true")
    p.add_argument("--desde")
    p.add_argument("--hasta")
    args = p.parse_args()
    try:
        g = cargar(args.datos)
        if args.listar:
            print("BASE FICTICIA | precios en USD")
            print(f"Aeropuertos: {len(g)}")
            print("Rutas: " + str(sum(map(len, g.values()))))
            for a, salidas in sorted(g.items()):
                texto = "; ".join(
                    f"{b}: ${c}" for b, c in salidas)
                print(f"{a} -> {texto or 'sin salidas'}")
        if bool(args.desde) != bool(args.hasta):
            raise ValueError("Indique origen y destino")
        if args.desde and args.hasta:
            a = args.desde.strip().upper()
            b = args.hasta.strip().upper()
            costo, ruta = buscar(g, a, b)
            if costo is None:
                print(f"Sin conexión: {a} -> {b}")
            else:
                print("Ruta: " + " -> ".join(ruta))
                print(f"Costo mínimo: ${costo:.2f} USD")
                escalas = max(0, len(ruta) - 2)
                print(f"Escalas: {escalas}")
        elif not args.listar:
            p.print_help()
    except (ValueError, OSError, KeyError) as e:
        p.exit(2, f"Error: {e}\n")


if __name__ == "__main__":
    main()
