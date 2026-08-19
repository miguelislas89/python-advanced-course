from typing import List

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from src.aplicacion.casos_uso.gestion_pedidos import (
    ConsultarPedidoCasoUso,
    CrearPedidoCasoUso,
)
from src.infraestructura.adaptadores.bus_redis_simulado import RedisBusEventosAdaptador
from src.infraestructura.adaptadores.persistencia_memoria import (
    MemoriaPedidoRepositorioAdaptador,
)

# 🌟 Configuración de la API y Swagger según Axity (Documentación viva y unificada)
app = FastAPI(
    title="Flor del Río - Core Orders API",
    description="Servicio Core bajo Arquitectura Hexagonal y lineamientos Axity.",
    version="1.0.0",
    docs_url="/api/v1/docs",  # URL Base controlada para documentación
    openapi_url="/api/v1/openapi.json",
)

# Inicialización de dependencias y adaptadores de infraestructura
repo_adaptador = MemoriaPedidoRepositorioAdaptador()
bus_adaptador = RedisBusEventosAdaptador()

crear_use_case = CrearPedidoCasoUso(repo_adaptador, bus_adaptador)
consultar_use_case = ConsultarPedidoCasoUso(repo_adaptador)


# --- MODELOS DE ENTRADA/SALIDA (DTOs) ---
class PedidoRequestDTO(BaseModel):
    pedido_id: str = Field(..., json_schema_extra={"example": "ORD-2026-001"})
    producto: str = Field(..., json_schema_extra={"example": "Agua de Rosas 500ml"})
    cantidad: int = Field(..., gt=0, json_schema_extra={"example": 150})
    precio_unitario: float = Field(..., gt=0.0, json_schema_extra={"example": 85.50})


class PedidoResponseDTO(BaseModel):
    pedido_id: str
    producto: str
    cantidad: int
    total: float
    estado: str


# --- MIDDLEWARE DE GESTIÓN DE ERRORES FORMATO AXITY ---
@app.exception_handler(HTTPException)
async def axity_http_exception_handler(request, exc: HTTPException):
    """Intercepta errores y devuelve la estructura corporativa."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "errorCode": f"ERR_{exc.status_code}",
            "errorMessage": exc.detail,
            "userError": (
                "Ocurrió un problema al procesar su solicitud. "
                "Verifique los parámetros."
            ),
            "info": "https://api.flordelrio.com/help",
        },
    )


# --- ENDPOINTS (PATRÓN MICROSERVICIOS AXITY V1) ---


@app.post(
    "/api/v1/orders",
    response_model=PedidoResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar una nueva orden corporativa",
)
async def registrar_orden(dto: PedidoRequestDTO):
    """Mapea el verbo POST para operaciones de persistencia inicial."""
    try:
        pedido_procesado = await crear_use_case.ejecutar(
            pedido_id=dto.pedido_id,
            producto=dto.producto,
            cantidad=dto.cantidad,
            precio_unitario=dto.precio_unitario,
        )
        return PedidoResponseDTO(
            pedido_id=pedido_procesado.pedido_id,
            producto=pedido_procesado.producto,
            cantidad=pedido_procesado.cantidad,
            total=pedido_procesado.calcular_total(),
            estado=pedido_procesado.estado.value,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get(
    "/api/v1/orders",
    response_model=List[PedidoResponseDTO],
    status_code=status.HTTP_200_OK,
    summary="Obtener catálogo de órdenes paginado",
)
async def consultar_ordenes_paginadas(
    limit: int = Query(default=25, ge=1, le=100, description="Registros por petición"),
    offset: int = Query(
        default=0, ge=0, description="Registros a omitir desde el origen"
    ),
):
    """Mapea el verbo GET aplicando QueryString obligatorio para paginación."""
    pedidos = await consultar_use_case.listar_historial(limit=limit, offset=offset)
    return [
        PedidoResponseDTO(
            pedido_id=p.pedido_id,
            producto=p.producto,
            cantidad=p.cantidad,
            total=p.calcular_total(),
            estado=p.estado.value,
        )
        for p in pedidos
    ]
