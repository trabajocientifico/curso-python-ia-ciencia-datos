import streamlit as st
import math

# ─── Configuración de la página ───────────────────────────────────────────────
st.set_page_config(
    page_title="Convertidor de Temperaturas",
    page_icon="🌡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── CSS Personalizado ────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600&display=swap');

    /* Fondo y paleta general */
    :root {
        --bg:        #0d0f14;
        --card:      #161a23;
        --border:    #2a2f3d;
        --accent-c:  #38bdf8;   /* Celsius  – azul frío  */
        --accent-f:  #fb923c;   /* Fahrenheit – naranja  */
        --accent-k:  #a78bfa;   /* Kelvin   – violeta    */
        --text:      #e2e8f0;
        --muted:     #64748b;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: var(--bg);
        color: var(--text);
    }

    /* Quitar fondo blanco del root de Streamlit */
    .stApp { background-color: var(--bg); }

    /* ── Título principal ── */
    .titulo-principal {
        font-family: 'Space Mono', monospace;
        font-size: 2.4rem;
        font-weight: 700;
        letter-spacing: -1px;
        text-align: center;
        margin-bottom: 0.2rem;
        background: linear-gradient(135deg, var(--accent-c), var(--accent-f), var(--accent-k));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitulo {
        text-align: center;
        color: var(--muted);
        font-size: 0.9rem;
        margin-bottom: 2rem;
        letter-spacing: 0.05em;
    }

    /* ── Tarjeta de resultado ── */
    .result-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.6rem 2rem;
        margin: 0.7rem 0;
        display: flex;
        align-items: center;
        gap: 1.2rem;
        transition: transform 0.2s;
    }
    .result-card:hover { transform: translateY(-2px); }

    .result-icon {
        font-size: 2rem;
        flex-shrink: 0;
    }

    .result-label {
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--muted);
        margin-bottom: 0.15rem;
    }

    .result-value {
        font-family: 'Space Mono', monospace;
        font-size: 2rem;
        font-weight: 700;
    }

    .result-value.celsius    { color: var(--accent-c); }
    .result-value.fahrenheit { color: var(--accent-f); }
    .result-value.kelvin     { color: var(--accent-k); }

    /* ── Separador ── */
    .divider {
        border: none;
        border-top: 1px solid var(--border);
        margin: 1.5rem 0;
    }

    /* ── Info pills ── */
    .pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        justify-content: center;
        margin-top: 1.5rem;
    }
    .pill {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 999px;
        padding: 0.3rem 1rem;
        font-size: 0.78rem;
        color: var(--muted);
        font-family: 'Space Mono', monospace;
    }

    /* Forzar colores en widgets de Streamlit */
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        background-color: var(--card) !important;
        color: var(--text) !important;
        border-color: var(--border) !important;
        border-radius: 10px !important;
    }

    /* Slider */
    .stSlider > div { padding: 0 0.5rem; }

    /* Botón */
    .stButton > button {
        background: linear-gradient(135deg, #1e3a5f, #2d1b69);
        color: var(--text);
        border: 1px solid var(--border);
        border-radius: 10px;
        font-family: 'Space Mono', monospace;
        font-size: 0.85rem;
        letter-spacing: 0.05em;
        width: 100%;
        padding: 0.6rem;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.85; }

    /* Ocultar la barra de menú y el footer de Streamlit */
    #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─── Funciones de conversión ───────────────────────────────────────────────────
def celsius_to_fahrenheit(c: float) -> float:
    return c * 9 / 5 + 32

def celsius_to_kelvin(c: float) -> float:
    return c + 273.15

def fahrenheit_to_celsius(f: float) -> float:
    return (f - 32) * 5 / 9

def fahrenheit_to_kelvin(f: float) -> float:
    return fahrenheit_to_celsius(f) + 273.15

def kelvin_to_celsius(k: float) -> float:
    return k - 273.15

def kelvin_to_fahrenheit(k: float) -> float:
    return celsius_to_fahrenheit(kelvin_to_celsius(k))

def convert(value: float, from_unit: str) -> dict:
    """Retorna un dict con los tres valores convertidos."""
    if from_unit == "Celsius (°C)":
        return {
            "C": value,
            "F": celsius_to_fahrenheit(value),
            "K": celsius_to_kelvin(value),
        }
    elif from_unit == "Fahrenheit (°F)":
        return {
            "C": fahrenheit_to_celsius(value),
            "F": value,
            "K": fahrenheit_to_kelvin(value),
        }
    else:  # Kelvin
        return {
            "C": kelvin_to_celsius(value),
            "F": kelvin_to_fahrenheit(value),
            "K": value,
        }


# ─── UI ───────────────────────────────────────────────────────────────────────
st.markdown('<div class="titulo-principal">🌡️ Convertidor de Temperaturas</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Celsius · Fahrenheit · Kelvin — conversión instantánea</div>', unsafe_allow_html=True)

# Columnas para entrada
col1, col2 = st.columns([2, 2])

with col1:
    unidad = st.selectbox(
        "Unidad de origen",
        ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"],
        key="unidad"
    )

with col2:
    # Rangos de entrada según unidad
    rangos = {
        "Celsius (°C)":    (-273.15, 1_000_000.0, 0.0),
        "Fahrenheit (°F)": (-459.67, 1_800_032.0, 32.0),
        "Kelvin (K)":      (0.0,     1_000_273.15, 273.15),
    }
    min_v, max_v, def_v = rangos[unidad]

    valor = st.number_input(
        "Valor a convertir",
        min_value=min_v,
        max_value=max_v,
        value=def_v,
        step=0.01,
        format="%.4f",
        key="valor"
    )

# Validación Kelvin negativo
if unidad == "Kelvin (K)" and valor < 0:
    st.error("⚠️ El Kelvin no puede ser negativo (cero absoluto = 0 K).")
    st.stop()

# ── Cálculo ──
resultados = convert(valor, unidad)

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("##### Resultados de la conversión")

# ── Tarjetas de resultado ──
def fmt(n: float) -> str:
    """Formatea con hasta 6 decimales, eliminando ceros al final."""
    if math.isnan(n) or math.isinf(n):
        return "∞"
    s = f"{n:.6f}".rstrip("0").rstrip(".")
    return s

cards = [
    ("🧊", "Celsius",     "°C", fmt(resultados["C"]), "celsius"),
    ("🔥", "Fahrenheit",  "°F", fmt(resultados["F"]), "fahrenheit"),
    ("🔭", "Kelvin",      " K", fmt(resultados["K"]), "kelvin"),
]

for icono, nombre, simbolo, val, css_class in cards:
    st.markdown(f"""
    <div class="result-card">
        <div class="result-icon">{icono}</div>
        <div>
            <div class="result-label">{nombre}</div>
            <div class="result-value {css_class}">{val} {simbolo}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Tabla de referencia rápida ──
with st.expander("📋  Tabla de referencia rápida"):
    referencias = {
        "Punto de referencia": [
            "Cero absoluto",
            "Congelación del agua",
            "Temperatura corporal",
            "Ebullición del agua",
            "Superficie del Sol (aprox.)",
        ],
        "°C":  [-273.15, 0,   37,   100,  5_500],
        "°F":  [-459.67, 32, 98.6,  212,  9_932],
        "K":   [0,      273.15, 310.15, 373.15, 5_773.15],
    }
    st.dataframe(referencias, use_container_width=True, hide_index=True)


# ── Píldoras de fórmulas ──
st.markdown("""
<div class="pill-row">
    <span class="pill">°F = °C × 9/5 + 32</span>
    <span class="pill">°C = (°F − 32) × 5/9</span>
    <span class="pill">K = °C + 273.15</span>
    <span class="pill">°C = K − 273.15</span>
</div>
""", unsafe_allow_html=True)
