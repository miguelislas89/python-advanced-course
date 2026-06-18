import os
import sys
from concurrent import futures

# Inyectamos el path local de forma dinámica
ruta_actual = os.path.dirname(os.path.abspath(__file__))
if ruta_actual not in sys.path:
    sys.path.append(ruta_actual)

# 🌟 Usamos # noqa: E402 para que Ruff entienda que este import va aquí a propósito
import grpc  # noqa: E402
import pedidos_pb2  # noqa: E402
import pedidos_pb2_grpc  # noqa: E402


class ServicioPedidos(pedidos_pb2_grpc.DespachadorPedidosServicer):
    """Implementación del contrato autogenerado de gRPC para Flor del Río."""

    # 🌟 Usamos # noqa: N802 porque gRPC obliga a heredar este nombre en CamelCase
    def CrearPedidoBinario(self, request, context):  # noqa: N802
        print(f"📥 [gRPC SERVER] Petición binaria recibida. ID: {request.pedido_id}")
        print(f"📦 Producto: '{request.producto}' | Volumen: {request.cantidad} pzas.")

        return pedidos_pb2.RespuestaPedido(
            estatus=f"Pedido {request.pedido_id} alojado en buffer gRPC exitosamente.",
            procesado=True,
        )


def arrancar_servidor_grpc() -> None:
    print("=== INICIO SERVIDOR gRPC (MÓDULO 20) ===")
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    pedidos_pb2_grpc.add_DespachadorPedidosServicer_to_server(
        ServicioPedidos(), servidor
    )

    servidor.add_insecure_port("[::]:50051")
    servidor.start()
    print("🚀 Servidor gRPC corriendo en modo seguro sobre el puerto 50051...")
    print("====================================================")
    servidor.wait_for_termination()


if __name__ == "__main__":
    arrancar_servidor_grpc()
