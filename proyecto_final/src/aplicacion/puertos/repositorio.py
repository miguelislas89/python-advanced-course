from abc import ABC, abstractmethod
from typing import List, Optional

from src.dominio.entidades import Pedido


class PedidoRepositorioPuerto(ABC):
    """Puerto que define el contrato de almacenamiento de pedidos."""

    @abstractmethod
    async def guardar(self, pedido: Pedido) -> None:
        """Guarda un pedido en el sistema de persistencia."""
        pass

    @abstractmethod
    async def buscar_por_id(self, pedido_id: str) -> Optional[Pedido]:
        """Recupera un pedido mediante su identificador único."""
        pass

    @abstractmethod
    async def listar_todos(self) -> List[Pedido]:
        """Obtiene el historial completo de pedidos."""
        pass
