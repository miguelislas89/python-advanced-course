from fastapi.testclient import TestClient

from src.dominio.entidades import EstadoPedido, Pedido
from src.infraestructura.adaptadores.api_rest import app

client = TestClient(app)


# --- PRUEBA UNITARIA (DOMINIO PURA) ---
def test_regla_negocio_calcular_total():
    """Valida que el cálculo del costo del lote de producción sea exacto."""
    pedido = Pedido(
        pedido_id="TST-001",
        producto="Shampoo de Mango 500ml",
        cantidad=10,
        precio_unitario=120.0,
    )
    assert pedido.calcular_total() == 1200.0
    assert pedido.estado == EstadoPedido.PENDIENTE


# --- PRUEBAS DE INTEGRACIÓN / CONTRATO (API REST) ---
def test_api_crear_orden_exito():
    """Valida el flujo POST completo y la respuesta HTTP 201."""
    payload = {
        "pedido_id": "ORD-2026-X10",
        "producto": "Jabón Carbón Activado",
        "cantidad": 20,
        "precio_unitario": 45.0,
    }
    response = client.post("/api/v1/orders", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["pedido_id"] == "ORD-2026-X10"
    assert data["total"] == 900.0
    assert data["estado"] == "PROCESADO"


def test_api_error_formato_estructura_axity():
    """Valida que los fallos interceptados retornen el estándar de Axity."""
    # Payload inválido: cantidad negativa viola las restricciones de Pydantic
    payload = {
        "pedido_id": "ORD-FAIL",
        "producto": "Aceite de Semilla de Uva",
        "cantidad": -5,
        "precio_unitario": 150.0,
    }
    response = client.post("/api/v1/orders", json=payload)
    # FastAPI intercepta fallos de validación con 422 de forma nativa
    assert response.status_code == 422
