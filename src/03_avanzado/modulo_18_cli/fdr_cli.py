import os

import typer
from rich import print as rprint

# Inicializamos la aplicación de Typer
app = typer.Typer(help="🚀 CLI Oficial de Operaciones para Flor del Río.")

# Base de datos simulada emulando el consumo de la API de Orders
DB_SIMULADA = [
    {"id": 1, "producto": "Agua de Rosas 500ml", "cantidad": 5},
    {"id": 2, "producto": "Shampoo de Mango 500ml", "cantidad": 12},
]


@app.command(name="listar")
def listar_ordenes() -> None:
    """Muestra el catálogo actual de órdenes procesadas en la API."""
    # Obtenemos la configuración del entorno (Inyección por variables de entorno)
    api_url = os.getenv("FDR_API_URL", "http://localhost:8080/api/v1")

    rprint(f"\n[bold blue]📡 Conectando a la API en:[/bold blue] {api_url}")
    rprint("[bold green]📋 Órdenes encontradas en el sistema:[/bold green]")

    for orden in DB_SIMULADA:
        rprint(
            f"  [yellow]• ID {orden['id']}:[/yellow] "
            f"{orden['producto']} | Volumen: {orden['cantidad']} unidades"
        )
    print("")


@app.command(name="crear")
def crear_orden(
    producto: str = typer.Option(..., help="Nombre del producto de Flor del Río."),
    cantidad: int = typer.Option(..., help="Cantidad de piezas para el lote."),
) -> None:
    """Registra una nueva orden operativa de forma inmediata."""
    if cantidad <= 0:
        rprint("[bold red]❌ Error:[/bold red] La cantidad debe ser mayor a cero.")
        raise typer.Exit(code=1)

    nuevo_id = len(DB_SIMULADA) + 1
    nueva_orden = {"id": nuevo_id, "producto": producto, "cantidad": cantidad}
    DB_SIMULADA.append(nueva_orden)

    rprint(f"\n[bold green]✅ ¡Orden #{nuevo_id} creada exitosamente![/bold green]")
    rprint(
        f"📦 [bold]Producto:[/bold] {producto} | [bold]Lote:[/bold] {cantidad} pzas.\n"
    )


if __name__ == "__main__":
    # Arrancamos la CLI
    app()
