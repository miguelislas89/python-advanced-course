from abc import ABC, abstractmethod

from src.dominio.entidades import EventoPedidoCreado


class BusEventosPuerto(ABC):
    """Puerto para el despacho asíncrono de eventos de dominio."""

    @abstractmethod
    async def publicar_evento(self, evento: EventoPedidoCreado) -> None:
        """Envía el evento al broker de mensajería (Redis/RabbitMQ)."""
        pass
