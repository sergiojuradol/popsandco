import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="POPS & CO - Control Operativo e Inventarios",
    page_icon="🍿",
    layout="wide"
)

# ---------------------------------------------------------
# INICIALIZACIÓN DEL INVENTARIO EN TIEMPO REAL (SESIÓN)
# ---------------------------------------------------------
if 'inventario_mp' not in st.session_state:
    st.session_state['inventario_mp'] = {
        "Maíz (kg)": 50.0,
        "Aceite (L)": 20.0,
        "Flavacol (g)": 1000.0,
        "Sazonador Cheddar (g)": 2000.0,
        "Sazonador Queso Jalapeño (g)": 1500.0,
        "Sazonador Habanero (g)": 1500.0,
        "Sazonador Adobo (g)": 1500.0,
    }

if 'inventario_indirectos' not in st.session_state:
    st.session_state['inventario_indirectos'] = {
        "Bolsas Celofán (pzs)": 1000,
        "Etiquetas Tradicional (pzs)": 300,
        "Etiquetas Cheddar (pzs)": 300,
        "Etiquetas Queso Jalapeño (pzs)": 300,
        "Etiquetas Habanero (pzs)": 300,
        "Etiquetas Adobo (pzs)": 300,
    }

if 'inventario_pt' not in st.session_state:
    st.session_state['inventario_pt'] = {
        "Tradicional (pkts)": 0,
        "Cheddar (pkts)": 0,
        "Queso Jalapeño (pkts)": 0,
        "Habanero (pkts)": 0,
        "Adobado (pkts)": 0,
    }

if 'historial_mermas' not in st.session_state:
    st.session_state['historial_mermas'] = []

st.title("🍿 POPS & CO - Sistema Interno de Gestión Operativa")
st.markdown("---")

# Menú de Navegación Lateral
modulo = st.sidebar.radio(
    "Navegación / Módulos:",
    [
        "📊 Inventario en Tiempo Real",
        "➕ Entrada / Compras de Insumos",
        "🏭 Registrar Lote de Producción",
        "⚠️ Registro de Mermas y Diferencias"
    ]
)

# ---------------------------------------------------------
# MÓDULO 1: INVENTARIO EN TIEMPO REAL
# ---------------------------------------------------------
if modulo == "📊 Inventario en Tiempo Real":
    st.header("📦 Caja General de Inventarios (Stock Actual)")
    st.caption("Existencias actualizadas automáticamente tras cada compra, lote producido o merma.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🌾 Materia Prima Directa")
        df_mp = pd.DataFrame(
            list(st.session_state['inventario_mp'].items()),
            columns=["Insumo", "Cantidad Disponible"]
        )
        st.dataframe(df_mp, use_container_width=True, hide_index=True)

    with col2:
        st.subheader("🛍️ Empaques y Material Indirecto")
        df_ind = pd.DataFrame(
            list(st.session_state['inventario_indirectos'].items()),
            columns=["Material", "Piezas Disponibles"]
        )
        st.dataframe(df_ind, use_container_width=True, hide_index=True)

    with col3:
        st.subheader("🍿 Producto Terminado (Listo p/ Venta)")
        df_pt = pd.DataFrame(
            list(st.session_state['inventario_pt'].items()),
            columns=["Sabor", "Paquetes Listos"]
        )
        st.dataframe(df_pt, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# MÓDULO 2: ENTRADA Y COMPRAS DE INSUMOS
# ---------------------------------------------------------
elif modulo == "➕ Entrada / Compras de Insumos":
    st.header("🛒 Registro de Compras e Entradas al Almacén")
    st.caption("Deposita nuevo inventario para incrementar automáticamente el stock de la caja principal.")

    tipo_insumo = st.selectbox("Categoría de Compra", ["Materia Prima Directa", "Material Indirecto / Empaque"])

    if tipo_insumo == "Materia Prima Directa":
        item_select = st.selectbox("Selecciona Insumo", list(st.session_state['inventario_mp'].keys()))
        cant_agregar = st.number_input("Cantidad a agregar (kg / L / g)", min_value=0.0, step=1.0)
        
        if st.button("➕ Depositar a Materia Prima"):
            st.session_state['inventario_mp'][item_select] += cant_agregar
            st.success(f"¡Se agregaron {cant_agregar} a {item_select}! Stock actualizado.")

    else:
        item_select = st.selectbox("Selecciona Material", list(st.session_state['inventario_indirectos'].keys()))
        cant_agregar = st.number_input("Cantidad a agregar (piezas)", min_value=0, step=10)
        
        if st.button("➕ Depositar a Empaques"):
            st.session_state['inventario_indirectos'][item_select] += cant_agregar
            st.success(f"¡Se agregaron {cant_agregar} pzs a {item_select}! Stock actualizado.")

# ---------------------------------------------------------
# MÓDULO 3: REGISTRAR LOTE Y DEDUCCIÓN AUTOMÁTICA
# ---------------------------------------------------------
elif modulo == "🏭 Registrar Lote de Producción":
    st.header("⚙️ Registro de Lote y Explosión de Insumos")
    st.caption("Captura las unidades producidas y los insumos consumidos. El sistema descontará el almacén y detectará mermas.")

    st.subheader("1. Paquetes Producidos por Sabor")
    c1, c2, c3, c4, c5 = st.columns(5)
    up_trad = c1.number_input("Tradicional", min_value=0, value=40)
    up_ched = c2.number_input("Cheddar", min_value=0, value=60)
    up_qjal = c3.number_input("Queso Jalapeño", min_value=0, value=30)
    up_hab = c4.number_input("Habanero", min_value=0, value=40)
    up_ado = c5.number_input("Adobado", min_value=0, value=30)

    total_pkts = up_trad + up_ched + up_qjal + up_hab + up_ado

    st.markdown("---")
    st.subheader("2. Consumo Real Medido (Conteo Antes / Después)")
    
    col_a, col_b = st.columns(2)
    with col_a:
        maiz_usado = st.number_input("Maíz Consumido (kg)", min_value=0.0, value=10.0, step=0.5)
        aceite_usado = st.number_input("Aceite Consumido (L)", min_value=0.0, value=5.0, step=0.5)
        bolsas_usadas = st.number_input("Bolsas Utilizadas (pzs)", min_value=0, value=total_pkts + 10) # Ejemplo de 10 bolsas mermadas
        mo_fija = st.number_input("Mano de Obra del Lote ($)", min_value=0.0, value=350.0)

    with col_b:
        saz_ched_g = st.number_input("Sazonador Cheddar Usado (g)", min_value=0.0, value=450.0)
        saz_qjal_g = st.number_input("Sazonador Q. Jalapeño Usado (g)", min_value=0.0, value=220.0)
        saz_hab_g = st.number_input("Sazonador Habanero Usado (g)", min_value=0.0, value=300.0)
        saz_ado_g = st.number_input("Sazonador Adobo Usado (g)", min_value=0.0, value=220.0)

    if st.button("🚀 Procesar Lote, Descontar Insumos y Guardar"):
        if total_pkts > 0:
            # 1. Descuento de Materia Prima
            st.session_state['inventario_mp']["Maíz (kg)"] -= maiz_usado
            st.session_state['inventario_mp']["Aceite (L)"] -= aceite_usado
            st.session_state['inventario_mp']["Sazonador Cheddar (g)"] -= saz_ched_g
            st.session_state['inventario_mp']["Sazonador Queso Jalapeño (g)"] -= saz_qjal_g
            st.session_state['inventario_mp']["Sazonador Habanero (g)"] -= saz_hab_g
            st.session_state['inventario_mp']["Sazonador Adobo (g)"] -= saz_ado_g

            # 2. Descuento de Empaques
            st.session_state['inventario_indirectos']["Bolsas Celofán (pzs)"] -= bolsas_usadas
            st.session_state['inventario_indirectos']["Etiquetas Tradicional (pzs)"] -= up_trad
            st.session_state['inventario_indirectos']["Etiquetas Cheddar (pzs)"] -= up_ched
            st.session_state['inventario_indirectos']["Etiquetas Queso Jalapeño (pzs)"] -= up_qjal
            st.session_state['inventario_indirectos']["Etiquetas Habanero (pzs)"] -= up_hab
            st.session_state['inventario_indirectos']["Etiquetas Adobo (pzs)"] -= up_ado

            # 3. Suma a Producto Terminado
            st.session_state['inventario_pt']["Tradicional (pkts)"] += up_trad
            st.session_state['inventario_pt']["Cheddar (pkts)"] += up_ched
            st.session_state['inventario_pt']["Queso Jalapeño (pkts)"] += up_qjal
            st.session_state['inventario_pt']["Habanero (pkts)"] += up_hab
            st.session_state['inventario_pt']["Adobado (pkts)"] += up_ado

            # 4. Cálculo de Merma de Bolsas
            merma_bolsas = bolsas_usadas - total_pkts
            if merma_bolsas > 0:
                st.session_state['historial_mermas'].append({
                    "Concepto": "Merma de Bolsas de Celofán",
                    "Diferencia / Cantidad": f"{merma_bolsas} pzs",
                    "Detalle": f"Se usaron {bolsas_usadas} bolsas para obtener {total_pkts} paquetes terminados."
                })

            st.balloons()
            st.success(f"✅ ¡Lote procesado exitosamente! Se agregaron {total_pkts} paquetes al inventario y se descontó la materia prima.")
            if merma_bolsas > 0:
                st.warning(f"⚠️ Se detectó una merma de {merma_bolsas} bolsas de celofán, la cual se registró en el Módulo de Mermas.")

        else:
            st.error("Ingresa al menos 1 paquete producido para procesar el lote.")

# ---------------------------------------------------------
# MÓDULO 4: REGISTRO DE MERMAS Y DIFERENCIAS
# ---------------------------------------------------------
elif modulo == "⚠️ Registro de Mermas y Diferencias":
    st.header("📋 Historial de Mermas, Pérdidas y Excedentes")
    st.caption("Auditoría de diferencias registradas entre el consumo real vs. producto obtenido.")

    if len(st.session_state['historial_mermas']) > 0:
        df_mermas = pd.DataFrame(st.session_state['historial_mermas'])
        st.dataframe(df_mermas, use_container_width=True, hide_index=True)
    else:
        st.info("👌 No hay mermas ni diferencias pendientes registradas hasta el momento.")
