from models.result import SolverResult


def save_routes_to_db(result: SolverResult) -> None:
    """
    Persiste las rutas generadas en PostgreSQL/PostGIS.

    MODO DUMMY: imprime el resultado en consola.
    Reemplazar por la implementación real cuando el contenedor PostgreSQL esté activo.
    """
    print("[DB] Guardando resultado de optimización...")
    for route in result.routes:
        print(
            f"  Vehículo {route.vehicle_id}: "
            f"{len(route.stops)} paradas | "
            f"{route.total_distance_m} m de distancia total"
        )
        for stop in route.stops:
            print(f"    [{stop.sequence}] Orden {stop.order_id}")

    # -------------------------------------------------------------------------
    # IMPLEMENTACIÓN REAL — descomentar cuando el contenedor PostgreSQL esté levantado
    # -------------------------------------------------------------------------
    # import asyncpg
    #
    # conn = await asyncpg.connect(
    #     "postgresql://rutas:rutas123@localhost:5432/rutas"
    # )
    # async with conn.transaction():
    #     for route in result.routes:
    #         route_id = await conn.fetchval(
    #             "INSERT INTO routes (vehicle_id, total_distance_m) VALUES ($1, $2) RETURNING id",
    #             route.vehicle_id, route.total_distance_m,
    #         )
    #         for stop in route.stops:
    #             await conn.execute(
    #                 "INSERT INTO route_stops (route_id, order_id, sequence) VALUES ($1, $2, $3)",
    #                 route_id, stop.order_id, stop.sequence,
    #             )
    # await conn.close()
