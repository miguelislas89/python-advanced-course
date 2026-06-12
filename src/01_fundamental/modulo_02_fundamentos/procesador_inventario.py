import json
import os
from typing import Any, Dict, List


def analizar_inventario_local(ruta_archivo: str) -> Dict[str, Any]:
    """Carga un archivo JSON de inventario, procesa sus elementos aplicando

    filtros de stock y genera métricas financieras agrupadas.
    """
    print(f"⚙️ Abriendo origen de datos en: {ruta_archivo}")

    try:
        # Validación preventiva antes de interactuar con el sistema
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(
                f"El archivo no existe en la ruta: '{ruta_archivo}'"
            )

        # El uso de 'with' garantiza el cierre automático del archivo
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            datos: List[Dict[str, Any]] = json.load(archivo)

        # Inicialización de variables y estructuras de agregación
        productos_activos: int = 0
        capital_total_inventario: float = 0.0
        categorias_detectadas: set = set()

        # Iteración sobre la colección de diccionarios
        for item in datos:
            stock: int = item.get("stock", 0)
            precio: float = item.get("precio_unitario", 0.0)

            # Implementación de Structural Pattern Matching (Python 3.10+)
            match stock:
                case 0:
                    print(
                        f"⚠️ Alerta Operativa: '{item.get('producto')}' "
                        f"no tiene existencias en almacén."
                    )
                case _ if stock > 0:
                    productos_activos += 1
                    capital_total_inventario += stock * precio
                    if "categoria" in item:
                        categorias_detectadas.add(item["categoria"])

        return {
            "status": "SUCCESS",
            "productos_disponibles": productos_activos,
            "valor_monetario_total": round(capital_total_inventario, 2),
            "categorias_mapeadas": list(categorias_detectadas),
        }

    except FileNotFoundError as error_ruta:
        print(f"❌ Error de Sistema de Archivos: {error_ruta}")
        return {"status": "FAILED", "error": "Archivo no localizado"}

    except json.JSONDecodeError as error_json:
        print(
            f"❌ Error de Estructura: Formato inválido. " f"Línea: {error_json.lineno}"
        )
        return {"status": "FAILED", "error": "Estructura JSON corrupta"}

    except Exception as error_inesperado:
        print(f"❌ Fallo crítico no controlado: {error_inesperado}")
        return {"status": "FAILED", "error": str(error_inesperado)}


if __name__ == "__main__":
    print("=== INICIO LABORATORIO MÓDULO 2 ===")

    # Cálculo dinámico de la ruta para evitar fallos de contexto
    directorio_actual = os.path.dirname(__file__)
    ruta_datos = os.path.join(directorio_actual, "inventario.json")

    resultado_analisis = analizar_inventario_local(ruta_datos)

    print(
        f"📊 Resultados del Procesamiento:\n"
        f"{json.dumps(resultado_analisis, indent=2, ensure_ascii=False)}"
    )
    print("===================================")
