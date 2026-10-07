import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración inicial de la página
st.set_page_config(
    page_title="POPS & CO - Control Operativo y Financiero",
    page_icon="🍿",
    layout="wide"
)

# ---------------------------------------------------------
# INICIALIZACIÓN DE ESTADOS (MEMORIA TEMPORAL)
# ---------------------------------------------------------
if 'inventario_mp' not in st.session_state:
    st.session_state['inventario_mp'] = {
        "Maíz": {"cant_kg": 20.0, "costo_promedio_kg": 18.00},
        "Aceite": {"cant_l": 10.0, "costo_promedio_l": 37.50},
        "Flavacol": {"cant_g": 1000.0, "costo_promedio_kg": 130.00},
        "Sazonador Cheddar": {"cant_g": 1000.0, "costo_promedio_kg": 160.00},
        "Sazonador Queso Jalapeño": {"cant_g": 1000.0, "costo_promedio_kg": 155.00},
        "Sazonador Habanero": {"cant_g": 1000.0, "costo_promedio_kg": 175.00},
        "Sazonador Adobo": {"cant_g": 1000.0, "costo_promedio_kg": 155.00},
    }

if 'inventario_indirectos' not in st.session_state:
    st.session_state['inventario_indirectos'] = {
        "Bolsas Celofán 20x35 (pzs)": {"cant": 2000, "costo_u": 0.40},
        "Etiquetas 120g Tradicional (pzs)": {"cant": 500, "costo_u": 1.75},
        "Etiquetas 120g Cheddar (pzs)": {"cant": 500, "costo_u": 1.75},
        "Etiquetas 120g Queso Jalapeño (pzs)": {"cant": 500, "costo_u": 1.75},
        "Etiquetas 120g Habanero (pzs)": {"cant": 500, "costo_u": 1.75},
        "Etiquetas 120g Adobo (pzs)": {"cant": 500, "costo_u": 1.75},
        "Etiquetas 65g (pzs)": {"cant": 200, "costo_u": 1.25},
    }

if 'inventario_pt' not in st.session_state:
    st.session_state['inventario_pt'] = {
        "Tradicional (120g)": {"cant": 0, "precio_dist": 14.00, "costo_directo_u": 5.20},
        "Cheddar (120g)": {"cant": 0, "precio_dist": 17.00, "costo_directo_u": 7.10},
        "Queso Jalapeño (120g)": {"cant": 0, "precio_dist": 17.00, "costo_directo_u": 7.05},
        "Habanero (120g)": {"cant": 0, "precio_dist": 17.00, "costo_directo_u": 7.25},
        "Adobado (120g)": {"cant": 0, "precio_dist": 17.00, "costo_directo_u": 7.05},
        "Pedido Especial (65g)": {"cant": 0, "precio_dist": 10.00, "costo_directo_u": 3.80},
    }

if 'historial_movimientos_mp' not in st.session_state:
    f_apertura = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.session_state['historial_movimientos_mp'] = [
        {"Fecha": f_apertura, "Insumo": "Maíz", "Tipo": "Entrada Inicial", "Cantidad": "20.0 kg", "Detalle": "Inventario inicial de apertura"},
        {"Fecha": f_apertura, "Insumo": "Aceite", "Tipo": "Entrada Inicial", "Cantidad": "10.0 L", "Detalle": "Inventario inicial de apertura"},
    ]

if 'historial_mermas' not in st.session_state:
    st.session_state['historial_mermas'] = []

if 'historial_ventas' not in st.session_state:
    st.session_state['historial_ventas'] = []

if 'historial_lotes' not in st.session_state:
    st.session_state['historial_lotes'] = []


# ---------------------------------------------------------
# MENÚ LATERAL Y NAVEGACIÓN
# ---------------------------------------------------------
st.sidebar.title("🍿 POPS & CO")
modulo = st.sidebar.radio(
    "Menú de Navegación:",
    [
        "🏠 Inicio / Bienvenido",
        "📦 Inventario de Producto Terminado",
        "🌾 Materia Prima (Físico y Movimientos)",
        "🛒 Compras e Ingreso de Insumos",
        "🏭 Registrar Lote de Producción y Costos",
        "🛍️ Punto de Venta y Margen de Ganancia",
        "💰 Costos Promedio, BOM y Valuación",
        "⚠️ Control de Mermas y Diferencias"
    ]
)

# ---------------------------------------------------------
# MÓDULO 0: INICIO / INTERFAZ PRINCIPAL
# ---------------------------------------------------------
if modulo == "🏠 Inicio / Bienvenido":
    
    # Encabezado con Logo y Eslogan
    col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
    with col_logo2:
        try:
            st.image("POPS & CO.png", use_column_width=True)
        except:
            st.markdown("<h1 style='text-align: center; color: #E63946;'>🍿 POPS & CO 🍿</h1>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: #555555; font-style: italic;'>« De puñito en puñito sabe mejor »</h3>", unsafe_allow_html=True)
    st.markdown("---")

    # Atajos de Acceso Rápido
    st.subheader("🚀 ¿Qué deseas hacer hoy?")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.info("### 🏭 Fabricación\nRegistra un nuevo lote de producción, calcula el consumo real de maíz, empaques, mano de obra y gas.")
    
    with col_b:
        st.success("### 🛍️ Ventas\nRegistra salidas de mercancía a distribuidores y consulta el margen bruto por paquete.")

    with col_c:
