from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class EstadoPedido(str, Enum):
    """Representa los estados válidos de un pedido en la planta."""

    PENDIENTE = "PENDIENTE"
    PROCESADO = "PROCESADO"
    CANCELADO = "CANCELADO"


class EventoPedidoCreado(BaseModel):
    """Evento de dominio disparado cuando un pedido se consolida."""

    pedido_id: str
    producto: str
    cantidad: int
    fecha_disparo: datetime = Field(default_factory=datetime.utcnow)


class Pedido(BaseModel):
    """Entidad de Dominio Pura e Inmutable para la gestión de órdenes."""

    pedido_id: str
    producto: str
    cantidad: int
    precio_unitario: float
    estado: EstadoPedido = EstadoPedido.PENDIENTE
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)

    def calcular_total(self) -> float:
        """Regla de negocio: Calcula el costo total del lote."""
        return self.cantidad * self.precio_unitario

    def procesar_pedido(self) -> EventoPedidoCreado:
        """Cambia el estado de la orden y genera el evento correspondiente."""
        if self.estado == EstadoPedido.CANCELADO:
            raise ValueError("No se puede procesar una orden cancelada.")
        self.estado = EstadoPedido.PROCESADO
        return EventoPedidoCreado(
            pedido_id=self.pedido_id, producto=self.producto, cantidad=self.cantidad
        )
