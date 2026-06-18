# =====================================================================
# ETAPA 1: BUILDER (Construcción de dependencias)
# =====================================================================
FROM python:3.10-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# =====================================================================
# ETAPA 2: RUNTIME (Entorno protegido y sin privilegios)
# =====================================================================
FROM python:3.10-slim AS runtime

WORKDIR /app

# 🌟 HARDENING: Creamos un usuario del sistema sin privilegios (appuser)
RUN useradd -u 10001 -m appuser && chown -R appuser:appuser /app

# Copiamos las dependencias optimizadas de la etapa anterior
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiamos todo el árbol de código fuente avanzado al contenedor
COPY src/ /app/src/

# Cambiamos el contexto de ejecución al usuario seguro antes de arrancar
USER appuser

# Comando de ejecución usando la bandera de módulo apuntando a seguridad
CMD ["python", "-m", "src.03_avanzado.modulo_19_seguridad.app_segura"]
