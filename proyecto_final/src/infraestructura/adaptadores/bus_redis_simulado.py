import json

from src.aplicacion.puertos.bus_eventos import BusEventosPuerto
from src.dominio.entidades import EventoPedidoCreado


class RedisBusEventosAdaptador(BusEventosPuerto):
    """Adaptador que emite eventos de dominio hacia canales Pub/Sub corporativos."""

    async def publicar_evento(self, evento: EventoPedidoCreado) -> None:
        canal_destino = "canal_orders_v1"
        payload = json.dumps(
            {
                "evento": "OrderCreated",
                "pedido_id": evento.pedido_id,
                "producto": evento.producto,
                "cantidad": evento.cantidad,
                "fecha": evento.fecha_disparo.isoformat(),
            }
        )
        # Simulación de telemetría de salida hacia el Broker de mensajería
        print(f"📢 [REDIS PUB/SUB] Evento publicado en '{canal_destino}': {payload}")
