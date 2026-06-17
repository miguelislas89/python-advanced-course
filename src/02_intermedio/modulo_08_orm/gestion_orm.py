from datetime import datetime
from typing import List

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)


# =====================================================================
# 1. CONFIGURACIÓN DE LA BASE DE DATOS DECLARATIVA
# =====================================================================
class Base(DeclarativeBase):
    """Clase base declarativa para todos los modelos del ORM."""

    pass


# =====================================================================
# 2. MODELADO DE ENTIDADES Y RELACIONES
# =====================================================================
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # Relación 1:N hacia Ordenes
    orders: Mapped[List["Order"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relaciones cruzadas
    user: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)

    # 🌟 CORRECCIÓN: Envolvemos los tipos nativos dentro de Mapped[]
    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relación hacia la Orden contenedora
    order: Mapped["Order"] = relationship(back_populates="items")


# =====================================================================
# 3. PIPELINE DE EJECUCIÓN (CRUD Y TRANSACCIONES)
# =====================================================================
if __name__ == "__main__":
    print("=== INICIO LABORATORIO MÓDULO 8 (SQLALCHEMY 2.0) ===")

    # Creamos el motor de conexión apuntando a SQLite en memoria RAM
    engine = create_engine("sqlite:///:memory:", echo=False)

    # Inicializamos las tablas simulando la ejecución de una migración inicial
    Base.metadata.create_all(engine)

    # Configuramos la fábrica de sesiones
    SessionLocal = sessionmaker(bind=engine)

    # Ejecución de operaciones CRUD seguras bajo una sesión transaccional
    with SessionLocal() as session:
        print("\n➕ [CREATE] Insertando usuario y orden con sus respectivos ítems...")

        # 1. Crear el usuario (Distribuidor)
        nuevo_usuario = User(username="miguel_islas", email="miguel@flordelrio.com")

        # 2. Crear la orden asociada
        nueva_orden = Order(user=nuevo_usuario)

        # 3. Agregar los ítems del pedido (Lotes de Flor del Río)
        item_1 = OrderItem(
            order=nueva_orden,
            product_name="Shampoo de Mango 500ml",
            price=180.00,
            quantity=5,
        )
        item_2 = OrderItem(
            order=nueva_orden,
            product_name="Agua de Rosas 500ml",
            price=150.00,
            quantity=3,
        )

        # SQLAlchemy es inteligente: al agregar al usuario, guardará la cascada completa
        session.add(nuevo_usuario)
        session.commit()  # Consolidamos la transacción en la base de datos
        print("💾 Datos confirmados mediante COMMIT exitoso.")

        with SessionLocal() as session:
            print("\n🔍 [READ] Consultando base de datos relacional...")
            usuario_db = session.query(User).filter_by(username="miguel_islas").first()

        if usuario_db:
            print(
                f"👤 Usuario Encontrado: {usuario_db.username} " f"({usuario_db.email})"
            )
            for orden in usuario_db.orders:
                print(
                    f"  📦 Orden ID: {orden.id} | " f"Fecha UTC: {orden.fecha_creacion}"
                )
                for item in orden.items:
                    print(
                        f"    - Sub-Item: {item.product_name} | "
                        f"Cantidad: {item.quantity} | "
                        f"unit_price: ${item.price}"
                    )

        # 4. [UPDATE] Modificar la cantidad de un ítem de la orden
        print("\n🔄 [UPDATE] Modificando cantidad del ítem 1 en la orden...")
        primer_item = session.query(OrderItem).first()
        if primer_item:
            primer_item.quantity = 10  # Cambiamos de 5 a 10 unidades
            session.commit()
            print(
                f"📝 Ítem '{primer_item.product_name}' actualizado "
                f"a {primer_item.quantity} unidades."
            )

    # Verificación final y eliminación (DELETE)
    with SessionLocal() as session:
        print(
            "\n❌ [DELETE] Evaluando eliminación en cascada " "(Borrado de usuario)..."
        )
        usuario_a_borrar = session.query(User).first()
        if usuario_a_borrar:
            session.delete(usuario_a_borrar)
            session.commit()

        # Comprobamos si quedó algún ítem huérfano en la base de datos
        conteo_items = session.query(OrderItem).count()
        print(f"📊 Items restantes en la tabla 'order_items': {conteo_items}")
        print(
            "💡 Éxito: La cascada eliminó automáticamente las órdenes "
            "e ítems asociados."
        )

    print("====================================================")
