import csv
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

# =====================================================================
# 1. CONFIGURACIÓN DEL LOGGING ESTRUCTURADO
# =====================================================================
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] (%(filename)s): %(message)s",
    handlers=[logging.StreamHandler()],  # Envía los logs directo a consola
)


def ejecutar_pipeline_ingesta() -> None:
    """Pipeline de extracción, transformación y carga (ETL) local que

    lee un CSV, calcula métricas de negocio y exporta a JSON.
    """
    logging.info("🚀 Iniciando Pipeline de Ingesta del Módulo 6...")

    # 2. PATHLIB: Localización segura y dinámica de archivos
    ruta_raiz = Path(__file__).parent
    archivo_csv = ruta_raiz / "datos_origen.csv"
    archivo_output_json = ruta_raiz / "reporte_metricas.json"

    logging.debug(f"Ruta de lectura establecida: {archivo_csv}")

    # Control de excepciones preventivo usando Pathlib
    if not archivo_csv.exists():
        logging.critical(f"El archivo esencial {archivo_csv.name} no existe.")
        return

    registros_validos = []
    total_unidades_procesadas = 0

    # 3. PARSEO: Lectura y validación del archivo CSV
    try:
        with open(archivo_csv, mode="r", encoding="utf-8") as archivo:
            lector_csv = csv.DictReader(archivo)

            for fila in lector_csv:
                producto = fila["producto"]
                precio = float(fila["precio"])
                cantidad = int(fila["cantidad"])

                # Inyectamos niveles de logging basados en reglas de negocio
                if cantidad <= 0:
                    logging.warning(
                        f"Detectado producto sin stock: '{producto}' "
                        f"(Cantidad: {cantidad}). Omitiendo del cálculo."
                    )
                    continue

                costo_total_fila = round(precio * cantidad, 2)
                total_unidades_procesadas += cantidad

                registros_validos.append(
                    {
                        "id": fila["id"],
                        "producto": producto,
                        "total_venta": costo_total_fila,
                    }
                )
                logging.debug(f"Fila procesada con éxito: {producto}")

    except Exception as error:
        logging.error(f"Fallo durante el parseo del CSV: {error}")
        return

    # 4. DATETIME: Estampa de tiempo absoluta con zona horaria UTC
    timestamp_auditoria = datetime.now(timezone.utc).isoformat()

    # Consolidación de los metadatos y métricas finales
    reporte_final = {
        "fecha_ejecucion_utc": timestamp_auditoria,
        "metricas_globales": {
            "total_items_validos": len(registros_validos),
            "total_unidades_adquiridas": total_unidades_procesadas,
        },
        "detalle_productos": registros_validos,
    }

    # 5. SERIALIZACIÓN: Exportación limpia a formato JSON
    try:
        with open(archivo_output_json, mode="w", encoding="utf-8") as destino:
            json.dump(reporte_final, destino, indent=2, ensure_ascii=False)

        logging.info(
            f"🎉 Pipeline completado. Reporte exportado a: "
            f"{archivo_output_json.name}"
        )

    except Exception as error:
        logging.error(f"No se pudo escribir el archivo JSON de salida: {error}")


if __name__ == "__main__":
    ejecutar_pipeline_ingesta()
