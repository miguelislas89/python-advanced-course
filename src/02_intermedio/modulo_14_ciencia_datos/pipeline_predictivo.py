import os

import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier


# =====================================================================
# 1. INGENIERÍA DE DATOS: GENERACIÓN Y LIMPIEZA DEL DATASET
# =====================================================================
def simular_y_limpiar_datos() -> pd.DataFrame:
    """Genera un archivo CSV simulando el histórico de control de calidad

    de Flor del Río y lo procesa en un DataFrame de Pandas.
    """
    # Histórico: [Concentración %, Temperatura °C, Estado_Lote]
    datos_crudos = {
        "concentracion_esencia": [85.0, 40.0, 90.0, 35.0, 88.0, 42.0],
        "temperatura_proceso": [22.5, 45.0, 24.0, 48.0, 21.0, 50.0],
        "aprobado": [1, 0, 1, 0, 1, 0],  # 1 = Aprobado, 0 = Rechazado
    }

    df = pd.DataFrame(datos_crudos)

    # Simulación de limpieza básica: Asegurar que no existan nulos
    df = df.dropna()
    return df


# =====================================================================
# 2. ENTRENAMIENTO Y SERIALIZACIÓN (JOBLIB)
# =====================================================================
def entrenar_motor_calidad(df: pd.DataFrame, ruta_modelo: str) -> None:
    """Entrena un Clasificador de Árbol de Decisión y lo guarda en disco."""
    # 🌟 CORRECCIÓN: Usamos minúsculas para cumplir con la regla N806 de Ruff
    x_datos = df[["concentracion_esencia", "temperatura_proceso"]]
    y = df["aprobado"]

    # Instanciamos y entrenamos el clasificador clásico
    modelo = DecisionTreeClassifier(max_depth=3, random_state=42)
    modelo.fit(x_datos, y)
    print("🎯 Modelo entrenado con éxito usando scikit-learn.")


# =====================================================================
# 3. PIPELINE DE INFERENCIA BÁSICA
# =====================================================================
def ejecutar_inferencia(ruta_modelo: str, nueva_medicion: list) -> int:
    """Carga el modelo de disco y predice si el lote será aprobado."""
    if not os.path.exists(ruta_modelo):
        raise FileNotFoundError("El modelo especificado no existe.")

    # Cargamos el archivo serializado
    modelo_cargado = joblib.load(ruta_modelo)

    # Convertimos la nueva muestra en el formato esperado (DataFrame con nombres)
    columnas = ["concentracion_esencia", "temperatura_proceso"]
    df_muestra = pd.DataFrame([nueva_medicion], columns=columnas)

    # Ejecutamos la predicción (Inferencia)
    prediccion = modelo_cargado.predict(df_muestra)
    return int(prediccion[0])


# =====================================================================
# 4. CONTROLADOR PRINCIPAL
# =====================================================================
if __name__ == "__main__":
    print("=== INICIO LABORATORIO MÓDULO 14 (CIENCIA DE DATOS) ===")

    archivo_modelo = "modelo_calidad_flor_del_rio.joblib"

    # Ejecutamos limpieza y entrenamiento
    dataset_limpio = simular_y_limpiar_datos()
    entrenar_motor_calidad(dataset_limpio, archivo_modelo)

    # --- SIMULACIÓN DE INFERENCIA EN PRODUCCIÓN ---
    print("\n🔮 Recibiendo telemetría de un nuevo lote en la planta...")
    # Caso 1: Alta concentración, temperatura óptima y templada
    nuevo_lote_bueno = [87.5, 23.0]
    resultado_bueno = ejecutar_inferencia(archivo_modelo, nuevo_lote_bueno)
    estado_bueno = "🟢 APROBADO" if resultado_bueno == 1 else "🔴 RECHAZADO"
    print(f"Resultado Inferencia Lote A: {estado_bueno}")

    # Caso 2: Baja concentración, sobrecalentamiento en la destilación
    nuevo_lote_malo = [38.0, 49.5]
    resultado_malo = ejecutar_inferencia(archivo_modelo, nuevo_lote_malo)
    estado_malo = "🟢 APROBADO" if resultado_malo == 1 else "🔴 RECHAZADO"
    print(f"Resultado Inferencia Lote B: {estado_malo}")

    print("====================================================")
