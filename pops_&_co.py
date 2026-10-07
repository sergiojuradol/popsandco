import streamlit as st
import pandas as pd

# Configuración inicial de la aplicación
st.set_page_config(
    page_title="POPS & CO - Control Operativo e Inventarios",
    page_icon="🍿",
    layout="wide"
)

# ---------------------------------------------------------
# INICIALIZACIÓN DEL INVENTARIO Y COSTOS PROMEDIO
# ---------------------------------------------------------
if 'inventario_mp' not in st.session_state:
    st.session_state['inventario_mp'] = {
        "Maíz": {"cant_kg": 20.0, "costo_promedio_kg": 18.00}, # $360 costal 20kg
        "Aceite": {"cant_l": 10.0, "costo_promedio_l": 37.50}, # ~$35 a $40 / L
        "Flavacol": {"cant_g": 1000.0, "costo_promedio_kg": 130.00},
        "Sazonador Cheddar": {"cant_g": 1000.0, "costo_promedio_kg": 160.00},
        "Sazonador Queso Jalapeño": {"cant_g": 1000.0, "costo_promedio_kg": 155.00},
        "Sazonador Habanero": {"cant_g": 1000.0, "costo_promedio_kg": 175.00},
        "Sazonador Adobo": {"cant_g": 1000.0, "costo_promedio_kg": 155.00},
    }

if 'inventario_indirectos' not in st.session_state:
    st.session_state['inventario_indirectos'] = {
        "Bolsas Celofán 20x35 (pzs)": {"cant": 2000, "costo_u": 0.40}, # Caja de 2000 pzs
        "Etiquetas 120g Tradicional (pzs)": {"cant": 500, "costo_u": 1.75},
        "Etiquetas 120g Cheddar (pzs)": {"cant": 500, "costo_u": 1.75},
        "Etiquetas 120g Queso Jalapeño (pzs)": {"cant": 500, "costo_u": 1.75},
        "Etiquetas 120g Habanero (pzs)": {"cant": 500, "costo_u": 1.75},
        "Etiquetas 120g Adobo (pzs)": {"cant": 500, "costo_u": 1.75},
        "Etiquetas 65g (pzs)": {"cant": 200, "costo_u": 1.25},
    }

if 'inventario_pt' not in st.session_state:
    st.session_state['inventario_pt'] = {
        "Tradicional (120g)": {"cant": 0, "precio_dist": 14.00},
        "Cheddar (120g)": {"cant": 0, "precio_dist": 17.00},
        "Queso Jalapeño (120g)": {"cant": 0, "precio_dist": 17.00},
        "Habanero (120g)": {"cant": 0, "precio_dist": 17.00},
        "Adobado (120g)": {"cant": 0, "precio_dist": 17.00},
        "Pedido Especial (65g)": {"cant": 0, "precio_dist": 10.00},
    }

if 'historial_mermas' not in st.session_state:
    st.session_state['historial_mermas'] = []

if 'historial_ventas' not in st.session_state:
    st.session_state['historial_ventas'] = []

st.title("🍿 POPS & CO - Sistema de Gestión Operativa")
st.markdown("---")

# Menú Lateral
modulo = st.sidebar.radio(
    "Navegación / Módulos:",
    [
        "📊 Caja de Inventario y Costos Promedio",
        "🛒 Compras e Ingreso de Insumos",
        "🏭 Registrar Lote de Producción y Prorrateo",
        "🛍️ Punto de Venta a Distribuidores",
        "⚠️ Control de Mermas y Diferencias"
    ]
)

# ---------------------------------------------------------
# MÓDULO 1: CAJA DE INVENTARIO Y COSTOS PROMEDIO
# ---------------------------------------------------------
if modulo == "📊 Caja de Inventario y Costos Promedio":
    st.header("📦 Caja General de Inventario (Stock en Tiempo Real)")
    st.caption("Existencias actualizadas dinámicamente con sus costos unitarios promediados.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🌾 Materia Prima Directa")
        filas_mp = []
        for k, v in st.session_state['inventario_mp'].items():
            if "cant_kg" in v:
                filas_mp.append({"Insumo": k, "Cantidad": f"{v['cant_kg']:.2f} kg", "Costo Promedied": f"${v['costo_promedio_kg']:.2f} / kg"})
            elif "cant_l" in v:
                filas_mp.append({"Insumo": k, "Cantidad": f"{v['cant_l']:.2f} L", "Costo Promedied": f"${v['costo_promedio_l']:.2f} / L"})
            else:
                costo_kg = v.get('costo_promedio_kg', 0)
                filas_mp.append({"Insumo": k, "Cantidad": f"{v['cant_g']:.0f} g", "Costo Promedied": f"${costo_kg:.2f} / kg"})
        st.dataframe(pd.DataFrame(filas_mp), use_container_width=True, hide_index=True)

    with col2:
        st.subheader("🛍️ Empaques e Indirectos")
        filas_ind = []
        for k, v in st.session_state['inventario_indirectos'].items():
            filas_ind.append({"Material": k, "Piezas": v['cant'], "Costo Unitario": f"${v['costo_u']:.2f}"})
        st.dataframe(pd.DataFrame(filas_ind), use_container_width=True, hide_index=True)

    with col3:
        st.subheader("🍿 Producto Terminado")
        filas_pt = []
        for k, v in st.session_state['inventario_pt'].items():
            filas_pt.append({"Sabor": k, "Paquetes Listos": f"{v['cant']} pkts", "Precio Dist.": f"${v['precio_dist']:.2f}"})
        st.dataframe(pd.DataFrame(filas_pt), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# MÓDULO 2: COMPRAS E INGRESO DE INSUMOS
# ---------------------------------------------------------
elif modulo == "🛒 Compras e Ingreso de Insumos":
    st.header("🛒 Registrar Compra de Materia Prima / Empaques")
    st.caption("Actualiza las existencias y calcula el **Costo Unitario Promedio Ponderado**.")

    cat_compra = st.radio("Categoría de Compra", ["Materia Prima Directa", "Empaques / Etiquetas"], horizontal=True)

    if cat_compra == "Materia Prima Directa":
        insumo_sel = st.selectbox("Selecciona Insumo Comprado", list(st.session_state['inventario_mp'].keys()))

        if insumo_sel == "Maíz":
            col1, col2 = st.columns(2)
            kg_comprados = col1.number_input("Kilos de Maíz Comprados", min_value=1.0, value=20.0, step=1.0)
            precio_total = col2.number_input("Precio Total Pagado ($)", min_value=0.0, value=360.0)

            if st.button("➕ Registar Compra de Maíz"):
                curr_kg = st.session_state['inventario_mp']['Maíz']['cant_kg']
                curr_costo = st.session_state['inventario_mp']['Maíz']['costo_promedio_kg']
                nuevo_total_kg = curr_kg + kg_comprados
                nuevo_costo_prom = ((curr_kg * curr_costo) + precio_total) / nuevo_total_kg

                st.session_state['inventario_mp']['Maíz']['cant_kg'] = nuevo_total_kg
                st.session_state['inventario_mp']['Maíz']['costo_promedio_kg'] = nuevo_costo_prom
                st.success(f"✅ ¡Maíz actualizado! Nuevo Stock: {nuevo_total_kg:.2f} kg | Costo Promedio: ${nuevo_costo_prom:.2f} / kg")

        elif insumo_sel == "Aceite":
            col1, col2 = st.columns(2)
            litros_comprados = col1.number_input("Litros de Aceite Comprados", min_value=0.5, value=10.0, step=0.5)
            precio_total = col2.number_input("Precio Total Pagado ($)", min_value=0.0, value=375.0)

            if st.button("➕ Registrar Compra de Aceite"):
                curr_l = st.session_state['inventario_mp']['Aceite']['cant_l']
                curr_costo = st.session_state['inventario_mp']['Aceite']['costo_promedio_l']
                nuevo_total_l = curr_l + litros_comprados
                nuevo_costo_prom = ((curr_l * curr_costo) + precio_total) / nuevo_total_l

                st.session_state['inventario_mp']['Aceite']['cant_l'] = nuevo_total_l
                st.session_state['inventario_mp']['Aceite']['costo_promedio_l'] = nuevo_costo_prom
                st.success(f"✅ ¡Aceite actualizado! Nuevo Stock: {nuevo_total_l:.2f} L | Costo Promedio: ${nuevo_costo_prom:.2f} / L")

        else:
            col1, col2 = st.columns(2)
            kilos_comprados = col1.number_input(f"Kilos de {insumo_sel} Comprados", min_value=0.1, value=1.0, step=0.1)
            precio_total = col2.number_input("Precio Total Pagado ($)", min_value=0.0, value=160.0)

            if st.button(f"➕ Registrar Compra de {insumo_sel}"):
                gramos_nuevos = kilos_comprados * 1000.0
                curr_g = st.session_state['inventario_mp'][insumo_sel]['cant_g']
                curr_costo_kg = st.session_state['inventario_mp'][insumo_sel]['costo_promedio_kg']
                nuevo_total_g = curr_g + gramos_nuevos
                nuevo_costo_prom_kg = (((curr_g / 1000.0) * curr_costo_kg) + precio_total) / (nuevo_total_g / 1000.0)

                st.session_state['inventario_mp'][insumo_sel]['cant_g'] = nuevo_total_g
                st.session_state['inventario_mp'][insumo_sel]['costo_promedio_kg'] = nuevo_costo_prom_kg
                st.success(f"✅ ¡{insumo_sel} actualizado! Nuevo Stock: {nuevo_total_g:.0f} g | Costo Promedio: ${nuevo_costo_prom_kg:.2f} / kg")

    else:
        mat_sel = st.selectbox("Selecciona Material Indirecto", list(st.session_state['inventario_indirectos'].keys()))
        col1, col2 = st.columns(2)
        pzs_compradas = col1.number_input("Piezas Compradas", min_value=1, value=2000 if "Bolsas" in mat_sel else 500)
        precio_total = col2.number_input("Precio Total Pagado ($)", min_value=0.0, value=800.0 if "Bolsas" in mat_sel else 875.0)

        if st.button(f"➕ Registrar Compra de {mat_sel}"):
            curr_pzs = st.session_state['inventario_indirectos'][mat_sel]['cant']
            curr_costo_u = st.session_state['inventario_indirectos'][mat_sel]['costo_u']
            nuevo_total_pzs = curr_pzs + pzs_compradas
            nuevo_costo_u = ((curr_pzs * curr_costo_u) + precio_total) / nuevo_total_pzs

            st.session_state['inventario_indirectos'][mat_sel]['cant'] = nuevo_total_pzs
            st.session_state['inventario_indirectos'][mat_sel]['costo_u'] = nuevo_costo_u
            st.success(f"✅ ¡{mat_sel} actualizado! Nuevo Stock: {nuevo_total_pzs} pzs | Costo Unitario Promedio: ${nuevo_costo_u:.2f} / pza")

# ---------------------------------------------------------
# MÓDULO 3: REGISTRO DE LOTE Y PRORRATEO
# ---------------------------------------------------------
elif modulo == "🏭 Registrar Lote de Producción y Prorrateo":
    st.header("⚙️ Registro de Lote de Producción")
    st.caption("Procesa la corrida, prorratea mano de obra/insumos, descuenta stock y detecta mermas.")

    st.subheader("1. Paquetes Producidos por Sabor (120g)")
    c1, c2, c3, c4, c5 = st.columns(5)
    up_trad = c1.number_input("Tradicional", min_value=0, value=40)
    up_ched = c2.number_input("Cheddar", min_value=0, value=65)
    up_qjal = c3.number_input("Queso Jalapeño", min_value=0, value=25)
    up_hab = c4.number_input("Habanero", min_value=0, value=45)
    up_ado = c5.number_input("Adobado", min_value=0, value=35)

    up_65g = st.number_input("Paquetes de Pedido Especial (65g - Opcional)", min_value=0, value=0)

    total_pkts_120 = up_trad + up_ched + up_qjal + up_hab + up_ado
    total_pkts_general = total_pkts_120 + up_65g

    # Consumos teóricos según recetas reales
    maiz_teorico_kg = ((total_pkts_120 * 120.0) + (up_65g * 65.0)) / 1000.0
    aceite_teorico_l = total_pkts_general / 39.0

    st.markdown("---")
    st.subheader("2. Consumo Medido Real (Conteo Físico)")
    col_a, col_b = st.columns(2)

    with col_a:
        maiz_real = st.number_input("Maíz Consumido Real (kg)", min_value=0.0, value=float(maiz_teorico_kg))
        aceite_real = st.number_input("Aceite Consumido Real (L)", min_value=0.0, value=float(aceite_teorico_l))
        bolsas_reales = st.number_input("Bolsas Celofán Utilizadas (pzs)", min_value=0, value=total_pkts_general + 5)
        mo_fija = st.number_input("Mano de Obra del Lote ($)", min_value=0.0, value=350.0)

    with col_b:
        flavacol_real_g = st.number_input("Flavacol Usado (g)", min_value=0.0, value=up_trad * 11.76)
        saz_ched_real = st.number_input("Sazonador Cheddar Usado (g)", min_value=0.0, value=up_ched * (1000.0 / 85.0))
        saz_qjal_real = st.number_input("Sazonador Q. Jalapeño Usado (g)", min_value=0.0, value=up_qjal * (1000.0 / 85.0))
        saz_hab_real = st.number_input("Sazonador Habanero Usado (g)", min_value=0.0, value=up_hab * (1000.0 / 85.0))
        saz_ado_real = st.number_input("Sazonador Adobo Usado (g)", min_value=0.0, value=up_ado * (1000.0 / 85.0))

    if st.button("🚀 Procesar Lote, Descontar Insumos y Prorratear"):
        if total_pkts_general > 0:
            # 1. Descuentos de Materia Prima
            st.session_state['inventario_mp']["Maíz"]["cant_kg"] -= maiz_real
            st.session_state['inventario_mp']["Aceite"]["cant_l"] -= aceite_real
            st.session_state['inventario_mp']["Flavacol"]["cant_g"] -= flavacol_real_g
            st.session_state['inventario_mp']["Sazonador Cheddar"]["cant_g"] -= saz_ched_real
            st.session_state['inventario_mp']["Sazonador Queso Jalapeño"]["cant_g"] -= saz_qjal_real
            st.session_state['inventario_mp']["Sazonador Habanero"]["cant_g"] -= saz_hab_real
            st.session_state['inventario_mp']["Sazonador Adobo"]["cant_g"] -= saz_ado_real

            # 2. Descuentos de Empaques
            st.session_state['inventario_indirectos']["Bolsas Celofán 20x35 (pzs)"]["cant"] -= bolsas_reales
            st.session_state['inventario_indirectos']["Etiquetas 120g Tradicional (pzs)"]["cant"] -= up_trad
            st.session_state['inventario_indirectos']["Etiquetas 120g Cheddar (pzs)"]["cant"] -= up_ched
            st.session_state['inventario_indirectos']["Etiquetas 120g Queso Jalapeño (pzs)"]["cant"] -= up_qjal
            st.session_state['inventario_indirectos']["Etiquetas 120g Habanero (pzs)"]["cant"] -= up_hab
            st.session_state['inventario_indirectos']["Etiquetas 120g Adobo (pzs)"]["cant"] -= up_ado
            if up_65g > 0:
                st.session_state['inventario_indirectos']["Etiquetas 65g (pzs)"]["cant"] -= up_65g

            # 3. Sumar a Producto Terminado
            st.session_state['inventario_pt']["Tradicional (120g)"]["cant"] += up_trad
            st.session_state['inventario_pt']["Cheddar (120g)"]["cant"] += up_ched
            st.session_state['inventario_pt']["Queso Jalapeño (120g)"]["cant"] += up_qjal
            st.session_state['inventario_pt']["Habanero (120g)"]["cant"] += up_hab
            st.session_state['inventario_pt']["Adobado (120g)"]["cant"] += up_ado
            st.session_state['inventario_pt']["Pedido Especial (65g)"]["cant"] += up_65g

            # 4. Auditoría de Mermas
            dif_bolsas = bolsas_reales - total_pkts_general
            if dif_bolsas > 0:
                st.session_state['historial_mermas'].append({
                    "Concepto": "Merma de Bolsas Celofán",
                    "Cantidad": f"{dif_bolsas} pzs",
                    "Detalle": f"Se usaron {bolsas_reales} bolsas para obtener {total_pkts_general} paquetes terminados."
                })

            dif_maiz = maiz_real - maiz_teorico_kg
            if abs(dif_maiz) > 0.1:
                st.session_state['historial_mermas'].append({
                    "Concepto": "Diferencia en Consumo de Maíz",
                    "Cantidad": f"{dif_maiz:.2f} kg",
                    "Detalle": f"Consumo real ({maiz_real:.2f}kg) vs Teórico ({maiz_teorico_kg:.2f}kg)."
                })

            st.balloons()
            st.success(f"✅ ¡Lote procesado exitosamente! Se agregaron {total_pkts_general} paquetes al inventario final.")
        else:
            st.error("Ingresa al menos 1 paquete producido para procesar el lote.")

# ---------------------------------------------------------
# MÓDULO 4: PUNTO DE VENTA A DISTRIBUIDORES
# ---------------------------------------------------------
elif modulo == "🛍️ Punto de Venta a Distribuidores":
    st.header("🛍️ Registro de Ventas a Distribuidores")
    st.caption("Descuenta paquetes listos del inventario de Producto Terminado.")

    sabor_venta = st.selectbox("Selecciona Producto / Sabor", list(st.session_state['inventario_pt'].keys()))
    stock_disp = st.session_state['inventario_pt'][sabor_venta]['cant']
    precio_u = st.session_state['inventario_pt'][sabor_venta]['precio_dist']

    st.info(f"💡 Disponible en Almacén: **{stock_disp} paquetes** | Precio Distribuidor: **${precio_u:.2f} / pza**")

    col_v1, col_v2 = st.columns(2)
    cant_vender = col_v1.number_input("Cantidad a Vender (pkts)", min_value=1, max_value=max(1, stock_disp), value=min(10, max(1, stock_disp)))
    cliente = col_v2.text_input("Nombre de Distribuidor / Cliente", value="Distribuidor General")

    total_cobrar = cant_vender * precio_u
    st.markdown(f"### Total a Cobrar: **${total_cobrar:.2f}**")

    if st.button("💵 Confirmar y Registrar Venta"):
        if stock_disp >= cant_vender:
            st.session_state['inventario_pt'][sabor_venta]['cant'] -= cant_vender
            st.session_state['historial_ventas'].append({
                "Cliente": cliente,
                "Producto": sabor_venta,
                "Cantidad": cant_vender,
                "Total Cobrado": f"${total_cobrar:.2f}"
            })
            st.success(f"✅ ¡Venta registrada! Se descontaron {cant_vender} pkts de {sabor_venta}.")
        else:
            st.error("No hay suficiente stock en producto terminado para cubrir esta venta.")

    if len(st.session_state['historial_ventas']) > 0:
        st.markdown("---")
        st.subheader("📋 Historial de Ventas Recientes")
        st.dataframe(pd.DataFrame(st.session_state['historial_ventas']), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# MÓDULO 5: CONTROL DE MERMAS Y DIFERENCIAS
# ---------------------------------------------------------
elif modulo == "⚠️ Control de Mermas y Diferencias":
    st.header("📋 Historial de Mermas y Desperdicios")
    st.caption("Bitácora de mermas detectadas automáticamente en los lotes de producción.")

    if len(st.session_state['historial_mermas']) > 0:
        st.dataframe(pd.DataFrame(st.session_state['historial_mermas']), use_container_width=True, hide_index=True)
    else:
        st.info("👌 No hay mermas registradas por el momento.")
