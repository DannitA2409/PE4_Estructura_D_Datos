"""Pruebas independientes y medición reproducible."""
import json
import platform
import statistics
import tempfile
from pathlib import Path
from time import perf_counter_ns
from vuelos import buscar, cargar

BASE = Path(__file__).parent
G = cargar(BASE / "vuelos.csv")
casos = [
    ("GYE", "BOG", (140, ["GYE", "CUE", "UIO", "BOG"])),
    ("GYE", "SCL", (275, ["GYE", "CUE", "UIO", "LIM", "SCL"])),
    ("GYE", "CUE", (35, ["GYE", "CUE"])),
    ("SCL", "GYE", (None, [])),
    ("GYE", "GYE", (0, ["GYE"])),
]
for a, b, esperado in casos:
    assert buscar(G, a, b) == esperado
    print(f"PASS {a} -> {b}: {esperado[0]}")
try:
    buscar(G, "XXX", "BOG")
    raise AssertionError("Aceptó nodo desconocido")
except ValueError:
    print("PASS aeropuerto desconocido")
with tempfile.TemporaryDirectory() as d:
    p = Path(d) / "mal.csv"
    for contenido in (
        "origen,destino,usd\nGYE,UIO,-1\n",
        "origen,destino,usd\nGYE,UIO,abc\n",
        "origen,destino,usd\n",
        "a,b,c\nGYE,UIO,10\n",
    ):
        p.write_text(contenido, encoding="utf-8")
        try:
            cargar(p)
            raise AssertionError("Aceptó base inválida")
        except ValueError:
            pass
print("PASS 4 validaciones de archivo")
# Oráculo independiente: enumera caminos simples.
def exhaustivo(g, a, b, vistos, costo=0):
    if a == b:
        return costo
    valores = [exhaustivo(g, v, b, vistos | {v}, costo + p)
               for v, p in g[a] if v not in vistos]
    return min(valores, default=float("inf"))
for a in G:
    for b in G:
        ref = exhaustivo(G, a, b, {a})
        esperado = None if ref == float("inf") else ref
        assert buscar(G, a, b)[0] == esperado
print("PASS oráculo exhaustivo: 36 pares")
# Tiempo de búsqueda: excluye carga e impresión.
for _ in range(1000):
    buscar(G, "GYE", "SCL")
medidas = []
for _ in range(30):
    inicio = perf_counter_ns()
    for _ in range(1000):
        buscar(G, "GYE", "SCL")
    medidas.append((perf_counter_ns() - inicio) / 1e6)
info = {
    "python": platform.python_version(),
    "sistema": platform.system(),
    "arquitectura": platform.machine(),
    "lotes": 30, "consultas_por_lote": 1000,
    "microsegundos_por_consulta": {
        "minimo": min(medidas),
        "mediana": statistics.median(medidas),
        "maximo": max(medidas),
    },
    "lotes_ms": medidas,
}
(BASE / "mediciones.json").write_text(
    json.dumps(info, indent=2), encoding="utf-8")
print("TIEMPOS (us/consulta):")
print(json.dumps(info["microsegundos_por_consulta"], indent=2))
print("Entorno:", info["python"], info["sistema"], info["arquitectura"])
