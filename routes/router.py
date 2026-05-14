from fastapi import APIRouter, BackgroundTasks
from models import OptimizationRequest
from service import generate_distance_matrix, save_routes_to_db, solver  

router = APIRouter()

@router.post("/optimize-routes")
async def optimize_routes(request: OptimizationRequest):
    """
    Recibe pedidos y vehículos, y devuelve la secuencia óptima de paradas.
    """
    
    # 1. PASO: Generar Matriz de Distancia (Llamada a OSRM)
    # Aquí consultarías tu contenedor Docker de OSRM para saber 
    # cuánto se tarda de cada punto a todos los demás.
    matrix = generate_distance_matrix(request.orders, request.depot)
    
    # 2. PASO: Resolver el VRP con Google OR-Tools
    # Aquí llamas a la lógica matemática que asigna órdenes a vehículos.
    result = solver.solve_vrp(matrix, request.orders, request.vehicles)
    
    # 3. PASO: Guardar en Base de Datos (PostgreSQL/PostGIS)
    # Persistir la ruta generada para que los conductores la vean.
    await save_routes_to_db(result)
    
    return {
        "status": "success",
        "total_vehicles_used": len(result.routes),
        "routes": result.routes  # Lista de órdenes ordenadas por vehículo
    }