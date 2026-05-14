import math
from typing import List

from models import Order, Location

# URL base del contenedor Docker OSRM
OSRM_BASE_URL = "http://localhost:5000"


def generate_distance_matrix(orders: List[Order], depot: Location) -> List[List[int]]:
    """
    Genera la matriz de distancias (en metros) entre el depósito y todas las órdenes.
    - Índice 0   → depósito
    - Índice 1..n → órdenes (mismo orden que la lista recibida)

    MODO DUMMY: calcula distancia euclidea aproximada sobre la esfera terrestre.
    Reemplazar por la implementación real de OSRM cuando el contenedor esté activo.
    """
    locations = [depot] + [o.location for o in orders]
    n = len(locations)

    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dlat = (locations[i].lat - locations[j].lat) * 111_000
                dlon = (
                    (locations[i].lon - locations[j].lon)
                    * math.cos(math.radians(locations[i].lat))
                    * 111_000
                )
                matrix[i][j] = int(math.sqrt(dlat**2 + dlon**2))

    return matrix

    # -------------------------------------------------------------------------
    # IMPLEMENTACIÓN REAL — descomentar cuando el contenedor OSRM esté levantado
    # -------------------------------------------------------------------------
    # import httpx
    #
    # locations = [depot] + [o.location for o in orders]
    # coords = ";".join(f"{loc.lon},{loc.lat}" for loc in locations)
    # url = f"{OSRM_BASE_URL}/table/v1/driving/{coords}?annotations=distance"
    #
    # response = httpx.get(url, timeout=30)
    # response.raise_for_status()
    # data = response.json()
    #
    # return [[int(d) for d in row] for row in data["distances"]]
