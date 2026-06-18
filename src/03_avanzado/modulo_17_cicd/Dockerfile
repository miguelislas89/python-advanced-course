# =====================================================================
# ETAPA 1: BUILDER (Construcción de dependencias y empaquetado)
# =====================================================================
FROM python:3.10-slim AS builder

WORKDIR /app

# Instalamos herramientas mínimas de compilación si fuesen necesarias
RUN pip install --no-cache-dir poetry

# Copiamos archivos de configuración de dependencias
COPY pyproject.toml poetry.lock* ./

# Forzamos a Poetry a exportar o construir las ruedas en una carpeta local
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# =====================================================================
# ETAPA 2: RUNTIME (Entorno ligero final de producción)
# =====================================================================
FROM python:3.10-slim AS runtime

WORKDIR /app

# Copiamos únicamente los paquetes instalados en la etapa anterior
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiamos el código fuente de nuestra aplicación
COPY src/03_avanzado/modulo_17_cicd/ ./modulo_17_cicd/

EXPOSE 8080

# Comando de ejecución seguro
CMD ["python", "-m", "modulo_17_cicd.app"]
