from dataclasses import dataclass, field
from typing import List


@dataclass
class EventoPedidoCreado:
    """Evento de dominio puro que captura un hecho relevante del negocio."""

    pedido_id: int
    producto: str


@dataclass
class PedidoAvanzado:
    """Entidad del núcleo de negocio. Maneja sus propios eventos."""

    pedido_id: int
    producto: str
    cantidad: int
    eventos: List[EventoPedidoCreado] = field(default_factory=list, init=False)

    def registrar_creacion(self) -> None:
        """Registra el hecho de que el pedido ha sido estructurado."""
        self.eventos.append(
            EventoPedidoCreado(pedido_id=self.pedido_id, producto=self.producto)
        )
