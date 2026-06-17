import pytest
from hypothesis import given
from hypothesis import strategies as st

from .calculador_descuentos import calcular_precio_final


# =====================================================================
# 1. PYTEST: PRUEBAS PARAMETRIZADAS (EJEMPLOS DE NEGOCIO)
# =====================================================================
@pytest.mark.parametrize(
    "precio, cantidad, esperado",
    [
        (100.0, 5, 500.0),  # Sin descuento: 100 * 5 = 500
        (100.0, 10, 900.0),  # 10% desc: 90 * 10 = 900
        (100.0, 50, 4000.0),  # 20% desc: 80 * 50 = 4000
    ],
)
def test_calcular_precio_final_ejemplos(precio: float, cantidad: int, esperado: float):
    """Valida los umbrales de descuento mediante ejemplos específicos."""
    assert calcular_precio_final(precio, cantidad) == esperado


def test_calcular_precio_final_excepcion():
    """Valida que valores negativos disparen la excepción correspondiente."""
    with pytest.raises(ValueError, match="no pueden ser negativos"):
        calcular_precio_final(-10.0, 5)


# =====================================================================
# 2. HYPOTHESIS: PROPERTY-BASED TESTING (PRUEBAS DE PROPIEDADES)
# =====================================================================
@given(
    st.floats(min_value=0.0, max_value=10000.0),
    st.integers(min_value=0, max_value=1000),
)
def test_propiedad_precio_final_siempre_positivo(precio: float, cantidad: int):
    """Garantiza que con cualquier dato válido, el costo total calculado

    nunca sea negativo y sea un número consistente.
    """
    resultado = calcular_precio_final(precio, cantidad)
    assert resultado >= 0.0
    assert isinstance(resultado, (int, float))
