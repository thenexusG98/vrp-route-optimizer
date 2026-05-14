from typing import List

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

from models import Order, Vehicle
from models.result import RouteStop, VehicleRoute, SolverResult

# Factor de escala para convertir floats (kg) a enteros requeridos por OR-Tools
_SCALE = 100


def solve_vrp(
    distance_matrix: List[List[int]],
    orders: List[Order],
    vehicles: List[Vehicle],
) -> SolverResult | None:
    """
    Resuelve el Vehicle Routing Problem (VRP) con restricciones de capacidad.

    Convención del índice en la matriz:
        0       → depósito
        1..n    → órdenes (mismo orden que `orders`)
    """
    n_locations = len(distance_matrix)  # depot + órdenes
    n_vehicles = len(vehicles)
    depot_index = 0

    # Demandas por nodo (peso escalado a entero). El depósito tiene demanda 0.
    demands = [0] + [int(o.weight * _SCALE) for o in orders]
    vehicle_capacities = [int(v.capacity_weight * _SCALE) for v in vehicles]

    # --- Crear el modelo de rutas ---
    manager = pywrapcp.RoutingIndexManager(n_locations, n_vehicles, depot_index)
    routing = pywrapcp.RoutingModel(manager)

    # Callback de distancia
    def distance_callback(from_index, to_index):
        return distance_matrix[manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]

    transit_idx = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_idx)

    # Restricción de capacidad (peso)
    def demand_callback(from_index):
        return demands[manager.IndexToNode(from_index)]

    demand_idx = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_idx,
        0,                   # sin slack de capacidad
        vehicle_capacities,
        True,                # iniciar carga en cero
        "Capacity",
    )

    # Parámetros de búsqueda
    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_params.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_params.time_limit.seconds = 10

    solution = routing.SolveWithParameters(search_params)

    if solution is None:
        return None

    return _extract_solution(manager, routing, solution, orders, vehicles)


def _extract_solution(manager, routing, solution, orders: List[Order], vehicles: List[Vehicle]) -> SolverResult:
    vehicle_routes: List[VehicleRoute] = []

    for v_idx, vehicle in enumerate(vehicles):
        index = routing.Start(v_idx)
        stops: List[RouteStop] = []
        seq = 0
        total_dist = 0

        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            if node != 0:  # saltar depósito
                stops.append(RouteStop(order_id=orders[node - 1].id, sequence=seq))
                seq += 1
            prev_index = index
            index = solution.Value(routing.NextVar(index))
            total_dist += routing.GetArcCostForVehicle(prev_index, index, v_idx)

        # Solo incluir vehículos con al menos una parada
        if stops:
            vehicle_routes.append(
                VehicleRoute(
                    vehicle_id=vehicle.id,
                    stops=stops,
                    total_distance_m=total_dist,
                )
            )

    return SolverResult(routes=vehicle_routes)