from typing import List, Optional

from src.aplicacion.puertos.bus_eventos import BusEventosPuerto
from src.aplicacion.puertos.repositorio import PedidoRepositorioPuerto
from src.dominio.entidades import EstadoPedido, Pedido


class CrearPedidoCasoUso:
    """Caso de uso para registrar e iniciar el flujo de un lote de producción."""

    def __init__(
        self, repositorio: PedidoRepositorioPuerto, bus_eventos: BusEventosPuerto
    ):
        self.repositorio = repositorio
        self.bus_eventos = bus_eventos

    async def ejecutar(
        self, pedido_id: str, producto: str, cantidad: int, precio_unitario: float
    ) -> Pedido:
        # 1. Instanciar la Entidad de Dominio
        nuevo_pedido = Pedido(
            pedido_id=pedido_id,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            estado=EstadoPedido.PENDIENTE,
        )

        # 2. Persistir a través del Puerto
        await self.repositorio.guardar(nuevo_pedido)

        # 3. Procesar reglas de negocio y disparar Evento de Dominio asíncrono
        evento = nuevo_pedido.procesar_pedido()
        await self.bus_eventos.publicar_evento(evento)

        # 4. Actualizar el estado procesado en persistencia
        await self.repositorio.guardar(nuevo_pedido)
        return nuevo_pedido


class ConsultarPedidoCasoUso:
    """Caso de uso para obtener estados y métricas de pedidos."""

    def __init__(self, repositorio: PedidoRepositorioPuerto):
        self.repositorio = repositorio

    async def obtener_por_id(self, pedido_id: str) -> Optional[Pedido]:
        return await self.repositorio.buscar_por_id(pedido_id)

    async def listar_historial(self, limit: int, offset: int) -> List[Pedido]:
        """Recupera el universo de datos aplicando los límites exigidos."""
        todos = await self.repositorio.listar_todos()
        # Simulación de paginación sobre el set de datos del puerto
        return todos[offset : offset + limit]
