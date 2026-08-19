from typing import Dict, List, Optional

from src.aplicacion.puertos.repositorio import PedidoRepositorioPuerto
from src.dominio.entidades import Pedido


class MemoriaPedidoRepositorioAdaptador(PedidoRepositorioPuerto):
    """Adaptador de infraestructura que implementa la persistencia en memoria."""

    def __init__(self) -> None:
        self._almacenamiento: Dict[str, Pedido] = {}

    async def guardar(self, pedido: Pedido) -> None:
        self._almacenamiento[pedido.pedido_id] = pedido

    async def buscar_por_id(self, pedido_id: str) -> Optional[Pedido]:
        return self._almacenamiento.get(pedido_id)

    async def listar_todos(self) -> List[Pedido]:
        return list(self._almacenamiento.values())
