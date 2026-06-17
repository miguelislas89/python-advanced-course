from typing import List

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field

# =====================================================================
# 1. CONFIGURACIÓN CENTRAL Y SEGURIDAD JWT
# =====================================================================
app = FastAPI(
    title="Flor del Río - API de Automatización de Órdenes",
    version="1.0.0",
    docs_url="/docs",
)

SECURITY_JWT_SECRET = "FLOR_DEL_RIO_SUPER_SECRET_KEY_2026"
ALGORITHM = "HS256"
seguridad_bearer = HTTPBearer()


def verificar_token_jwt(token: str) -> str:
    """Verifica la autenticidad del token JWT puro desvinculando

    el Depends para cumplir con la regla B008 de Ruff.
    """
    try:
        payload = jwt.decode(token, SECURITY_JWT_SECRET, algorithms=[ALGORITHM])
        return payload.get("sub", "INVITADO")
    except jwt.PyJWTError:
        # 🌟 CORRECCIÓN B904: Añadimos 'from None' para un rastreo limpio
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de acceso inválido o expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None


# =====================================================================
# 2. ESQUEMAS DE VALIDACIÓN (PYDANTIC V2)
# =====================================================================
class LoginRequest(BaseModel):
    username: str
    password: str


class OrderCreateIn(BaseModel):
    product_name: str = Field(min_length=3, max_length=50)
    price: float = Field(gt=0, description="El precio debe ser mayor a cero")
    quantity: int = Field(ge=1, description="Debe adquirir mínimo 1 unidad")


class OrderOut(BaseModel):
    id: int
    product_name: str
    price: float
    quantity: int
    owner: str


# Base de datos simulada en memoria para el laboratorio
DB_TEMPORAL_ORDERS: List[OrderOut] = [
    OrderOut(
        id=1,
        product_name="Shampoo de Mango 500ml",
        price=180.0,
        quantity=5,
        owner="miguel_islas",
    )
]


# =====================================================================
# 3. ENDPOINTS DE LA API (CRUD & AUTENTICACIÓN)
# =====================================================================
@app.post("/auth/login", tags=["Autenticación"])
def login(payload: LoginRequest):
    """Autentica a un distribuidor y emite un Token JWT firmado."""
    # Validación mock de credenciales corporativas
    if payload.username == "miguel" and payload.password == "admin123":
        token_firmado = jwt.encode(
            {"sub": payload.username}, SECURITY_JWT_SECRET, algorithm=ALGORITHM
        )
        return {"access_token": token_firmado, "token_type": "bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de acceso incorrectas.",
    )


@app.get("/api/orders", response_model=List[OrderOut], tags=["Órdenes"])
def listar_ordenes(usuario_autenticado: str = Depends(verificar_token_jwt)):
    """Retorna el histórico de órdenes. Requiere token de autenticación JWT."""
    return DB_TEMPORAL_ORDERS


@app.post(
    "/api/orders",
    response_model=OrderOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Órdenes"],
)
def crear_orden(
    payload: OrderCreateIn, usuario_autenticado: str = Depends(verificar_token_jwt)
):
    """Crea una nueva orden de distribución previa validación de Pydantic."""
    nuevo_id = len(DB_TEMPORAL_ORDERS) + 1
    nueva_orden = OrderOut(
        id=nuevo_id,
        product_name=payload.product_name,
        price=payload.price,
        quantity=payload.quantity,
        owner=usuario_autenticado,
    )
    DB_TEMPORAL_ORDERS.append(nueva_orden)
    return nueva_orden
