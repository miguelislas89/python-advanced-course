import os
import sys

# Inyectamos el path local
ruta_actual = os.getenv(
    "FDR_MODULO_20_PATH", os.path.dirname(os.path.abspath(__file__))
)
if ruta_actual not in sys.path:
    sys.path.append(ruta_actual)

# 🌟 Bypass controlado de importación
import grpc  # noqa: E402
import pedidos_pb2  # noqa: E402
import pedidos_pb2_grpc  # noqa: E402


def ejecutar_cliente_y_publicar_evento() -> None:
    print("=== INICIO CLIENTE INTEROPERABLE (MÓDULO 20) ===")

    with grpc.insecure_channel("localhost:50051") as canal:
        stub = pedidos_pb2_grpc.DespachadorPedidosStub(canal)

        solicitud = pedidos_pb2.SolicitudPedido(
            pedido_id=999, producto="Agua de Rosas 500ml", cantidad=50
        )

        print("📡 Enviando payload binario comprimido mediante gRPC...")
        respuesta = stub.CrearPedidoBinario(solicitud)
        print(f"✨ Respuesta del Servidor gRPC: {respuesta.estatus}")

    # 🌟 CORRECCIÓN: Rompemos la línea larga para no violar E501
    print("\n📬 [BROKER] Conectando al bus de eventos...")
    canal_evento = "canal_ordenes_flor_del_rio"
    evento_payload = (
        f"{{'evento': 'OrderCreated', 'id': 999, 'item': '{solicitud.producto}'}}"
    )

    print(f"📢 [EVENTO PUBLICADO] Canal: '{canal_evento}'")
    print(f"📝 Payload: {evento_payload}")
    print("====================================================")


if __name__ == "__main__":
    ejecutar_cliente_y_publicar_evento()
