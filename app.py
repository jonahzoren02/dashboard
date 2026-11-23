from streamlit.elements.lib.color_util import Color
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from dataPrincipal import enviar_data

def imprimir_data(*args):
    n = 1
    print("-------INFORMACION-------")
    for ele in args:
        print("###ELemento ", n)
        print(ele)
        print("#############")
        n += 1

# Configuración de página
st.set_page_config(
    page_title="LABET - Panel de gestión comercial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Estilos CSS personalizados para replicar exactamente el diseño de la imagen
st.markdown(
    """
<style>
    /* Ocultar elementos predeterminados de Streamlit si se desea una vista limpia */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 900px;
        margin: 0 auto;
    }

    /* Contenedor Superior Oscuro (Banner Principal) */
    .header-card {
        background-color: #0b1d28;
        border-radius: 16px;
        padding: 24px 28px;
        color: #ffffff;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }

    .brand-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
    }

    .brand-left {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .brand-icon {
        background-color: #00b074;
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }

    .brand-title {
        font-weight: 800;
        font-size: 17px;
        line-height: 1.1;
        letter-spacing: 0.5px;
    }

    .brand-sub {
        color: #00d293;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.2px;
    }

    .demo-badge {
        background-color: #064e3b;
        color: #10b981;
        border: 1px solid #059669;
        border-radius: 6px;
        padding: 2px 10px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    .main-title {
        font-size: 26px;
        font-weight: 700;
        color: #ffffff;
        margin: 0 0 4px 0;
    }

    .main-subtitle {
        color: #7d96a6;
        font-size: 13px;
        margin-bottom: 22px;
    }

    .unit-label {
        color: #7d96a6;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.2px;
        margin-bottom: 10px;
        text-transform: uppercase;
    }

    /* Estilos de botones de Unidad de Negocio (Replicando el banner de LABET) */
    div[data-testid="stButton"] > button[kind="primary"] {
        background-color: #00b074 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 10px 16px !important;
        box-shadow: 0 4px 12px rgba(0, 176, 116, 0.25) !important;
    }

    div[data-testid="stButton"] > button[kind="secondary"] {
        background-color: #142834 !important;
        color: #d1d5db !important;
        border: 1px solid #1e3a4b !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 10px 16px !important;
    }

    div[data-testid="stButton"] > button[kind="secondary"]:hover {
        background-color: #1c3646 !important;
        color: #ffffff !important;
        border-color: #00b074 !important;
    }

    /* Tarjeta Blanca: Resumen Ejecutivo */
    .white-card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 24px;
        border: 1px solid #edf2f7;
        box-shadow: 0 2px 12px rgba(0,0,0,0.03);
        margin-bottom: 20px;
    }

    .card-title {
        font-size: 18px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 18px;
    }

    .kpi-title {
        color: #64748b;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 4px;
    }

    .kpi-value {
        color: #0f172a;
        font-size: 26px;
        font-weight: 700;
        line-height: 1.2;
    }

    .kpi-delta-green {
        color: #10b981;
        font-size: 12px;
        font-weight: 600;
        margin-top: 2px;
    }

    .kpi-sub-text {
        color: #64748b;
        font-size: 12px;
        margin-top: 2px;
    }

    .badge-meta {
        display: inline-block;
        background-color: #dcfce7;
        color: #15803d;
        border-radius: 12px;
        padding: 2px 10px;
        font-size: 11px;
        font-weight: 600;
        margin-top: 4px;
    }

    .disclaimer-text {
        color: #94a3b8;
        font-size: 12px;
        margin-bottom: 10px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Lista maestra para ordenar los meses de manera cronológica
ORDEN_MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Setiembre", "Octubre", "Noviembre", "Diciembre"
]

# Paleta de colores para cada mes similar a la imagen
PALETA_MESES = {
    "Enero": "#2563eb",       # Azul
    "Febrero": "#8b5cf6",     # Morado
    "Marzo": "#f97316",       # Naranja
    "Abril": "#10b981",       # Verde esmeralda
    "Mayo": "#ef4444",        # Rojo
    "Junio": "#eab308",       # Amarillo/Ámbar
    "Julio": "#ec4899",       # Rosa
    "Agosto": "#0284c7",      # Azul brillante
    "Setiembre": "#7c3aed",   # Violeta
    "Octubre": "#ea580c",     # Naranja oscuro
    "Noviembre": "#16a34a",   # Verde
    "Diciembre": "#dc2626",   # Rojo oscuro
}


# Carga de datos con auto-invalidación de caché si el archivo cambia
@st.cache_data
def cargar_datos():
    df = enviar_data()

    # Convertir mes a categórico ordenado
    if "MES" in df.columns:
        meses_presentes = [m for m in ORDEN_MESES if m in df["MES"].values]
        df["MES"] = pd.Categorical(df["MES"], categories=meses_presentes, ordered=True)

    return df

with st.spinner("Cargando tablero LABET..."):
    df_raw = cargar_datos()

# Inicializar estado de sesión para Unidad de Negocio si no existe
if "unidad_negocio" not in st.session_state:
    st.session_state["unidad_negocio"] = "Consolidado"

# -------------------------------------------------------------
# ENCABEZADO SUPERIOR OSCURO (BANNER LABET)
# -------------------------------------------------------------
st.markdown(
    """
<div class="header-card">
    <div class="brand-row">
        <div class="brand-left">
            <div class="brand-icon">📈</div>
            <div>
                <div class="brand-title">LABET</div>
                <div class="brand-sub">BUSINESS INTELLIGENCE</div>
            </div>
        </div>
        <div class="demo-badge">DEMO v1</div>
    </div>
    <div class="main-title">Panel de gestión comercial</div>
    <div class="main-subtitle">Visión estratégica • Resultados • Rentabilidad</div>
    <div class="unit-label">UNIDAD DE NEGOCIO</div>
</div>
""",
    unsafe_allow_html=True,
)

# Cuadrícula 2x2 para seleccionar la Unidad de Negocio (replicando los botones del banner)
unidades = [
    ("Consolidado", "Aves y Cerdos"),
    ("Ganadería", "Mascotas"),
]

col_u1, col_u2 = st.columns(2)

def set_unidad(nueva_unidad):
    st.session_state["unidad_negocio"] = nueva_unidad

# Fila 1 de botones
with col_u1:
    activo_cons = st.session_state["unidad_negocio"] == "Consolidado"
    label_cons = "✔ Consolidado" if activo_cons else "Consolidado"
    if st.button(label_cons, key="btn_cons", type="primary" if activo_cons else "secondary", width="stretch"):
        set_unidad("Consolidado")
        st.rerun()

with col_u2:
    activo_aves = st.session_state["unidad_negocio"] == "Aves y Cerdos"
    label_aves = "✔ Aves y Cerdos" if activo_aves else "Aves y Cerdos"
    if st.button(label_aves, key="btn_aves", type="primary" if activo_aves else "secondary", width="stretch"):
        set_unidad("Aves y Cerdos")
        st.rerun()

# Fila 2 de botones
col_u3, col_u4 = st.columns(2)
with col_u3:
    activo_gan = st.session_state["unidad_negocio"] == "Ganadería"
    label_gan = "✔ Ganadería" if activo_gan else "Ganadería"
    if st.button(label_gan, key="btn_gan", type="primary" if activo_gan else "secondary", width="stretch"):
        set_unidad("Ganadería")
        st.rerun()

with col_u4:
    activo_masc = st.session_state["unidad_negocio"] == "Mascotas"
    label_masc = "✔ Mascotas" if activo_masc else "Mascotas"
    if st.button(label_masc, key="btn_masc", type="primary" if activo_masc else "secondary", width="stretch"):
        set_unidad("Mascotas")
        st.rerun()

# st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 4. FILTRADO POR UNIDAD DE NEGOCIO
# -------------------------------------------------------------
# Datos sin registros de ventas
df_ventas = df_raw[
    df_raw["RV_TOTAL"].notna()
    & ~(df_raw["VENDEDOR"] == "NO REGISTRADO")
]
df_filtrado_unidad = df_ventas.copy()
unidad_actual = st.session_state["unidad_negocio"]

if unidad_actual == "Aves y Cerdos":
    df_filtrado_unidad = df_filtrado_unidad[
        df_filtrado_unidad["LINEA"].isin(["Aves & Cerdos"])
    ]
elif unidad_actual == "Ganadería":
    df_filtrado_unidad = df_filtrado_unidad[
        df_filtrado_unidad["LINEA"].isin(["Ganadería"])
    ]
elif unidad_actual == "Mascotas":
    df_filtrado_unidad = df_filtrado_unidad[
        df_filtrado_unidad["LINEA"] == "Mascotas"
    ]
# Si es Consolidado, mantiene todas las líneas

# -------------------------------------------------------------
# 5. SECCIÓN RESUMEN EJECUTIVO (TARJETA BLANCA CON SELECTOR DE AÑO)
# -------------------------------------------------------------
anios_disponibles = sorted(df_filtrado_unidad["AÑO"].dropna().unique().tolist(), reverse=True)
if not anios_disponibles:
    anios_disponibles = [2026]

col_titulo, col_anio = st.columns([2, 1])
with col_titulo:
    st.subheader(
        "**Resumen anual**",
        width="content"
        )
with col_anio:
    anio_sel = st.selectbox("Año", anios_disponibles, index=0, label_visibility="collapsed")

# Filtrado por año seleccionado
df_anio_curr = df_filtrado_unidad[df_filtrado_unidad["AÑO"] == anio_sel]

# Datos del año anterior para calcular comparaciones
anio_prev = "2025"
df_anio_prev = df_filtrado_unidad[df_filtrado_unidad["AÑO"] == anio_prev]

# Métricas Calculadas - Volumen de productos
total_volumen = df_anio_curr["CANTIDAD"].sum()
total_volumen_ant = df_anio_prev["CANTIDAD"].sum() if not df_anio_prev.empty else 0
dif_volumen = total_volumen - total_volumen_ant

# Métrica Calculadas - Ventas totales
total_venta = df_anio_curr["RV_TOTAL"].sum()
total_venta_ant = df_anio_prev["RV_TOTAL"].sum() if not df_anio_prev.empty else 0
dif_venta = total_venta - total_venta_ant

# Métrica Calculadas - Cantidad de clientes
partner_curr = df_anio_curr["PARTNER"].nunique()
partner_prev = df_anio_prev["PARTNER"].nunique()
partner_diff = partner_curr - partner_prev

# Métrica Calculadas - Volumen de ventas
sales_curr_vol = df_anio_curr["RV_TOTAL"].count()
sales_prev_vol = df_anio_prev["RV_TOTAL"].count()
sales_diff_vol = sales_curr_vol - sales_prev_vol

# Cuadrícula 2x2 para las tarjetas de KPI
kpi_c1, kpi_c2 = st.columns(2)
with kpi_c1:
    st.metric(
        "Venta anual",
        f"S/ {total_venta:,.0f}",
        delta= f"S/ {dif_venta:,.0f}",
        # delta_arrow= "down",
        icon= "💸",
        border= True,
        # chart_data= [4,1,5,3,8,4,9,2,4,8,2,2],
        # chart_type= "area",
        delta_description="vs. año anterior"
        )

with kpi_c2:
    st.metric(
        "Volumen anual",
        f"{total_volumen:,.0f} Und",
        delta= dif_volumen,
        # delta_arrow= "down",
        icon= "🚀",
        border= True,
        # chart_data= [4,1,5,3,8,4,9,2,4,8,2,2],
        # chart_type= "area",
        delta_description="vs. año anterior"
        )

kpi_c3, kpi_c4 = st.columns(2)
with kpi_c3:
    st.metric(
        "Cantidad de Partner",
        f"{partner_curr:,.0f}",
        delta= partner_diff,
        # delta_arrow= "down",
        icon= "💼",
        border= True,
        # chart_data= [4,1,5,3,8,4,9,2,4,8,2,2],
        # chart_type= "area",
        delta_description="vs. año anterior"
        )

with kpi_c4:
    st.metric(
        "Cantidad de ventas",
        f"{sales_curr_vol:,.0f}",
        delta= sales_diff_vol,
        # delta_arrow= "down",
        icon= "🛒",
        border= True,
        # chart_data= [4,1,5,3,8,4,9,2,4,8,2,2],
        # chart_type= "area",
        delta_description="vs. año anterior"
        )

st.markdown("<hr style='margin: 25px 0 20px 0; border: 0; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 6. SECCIÓN EVOLUCIÓN DE VENTAS (GRÁFICO DE BARRAS MULTICOLOR)
# -------------------------------------------------------------
c_ev_title, c_ev_switch = st.columns([2, 1])

with c_ev_title:
    st.markdown(
        "***Gráfico Anual por Venta o Volumen***"
    )

with c_ev_switch:
    # Selector de píldora interactivo Ventas vs Volumen
    modo_vista = st.segmented_control(
        "Modo de métrica",
        options=["Ventas", "Volumen"],
        default="Ventas",
        label_visibility="collapsed"
    )
    if not modo_vista:
        modo_vista = "Ventas"

#st.markdown("<div class='disclaimer-text'>Valores demostrativos, no corresponden a registros reales.</div>", unsafe_allow_html=True)

# Agrupación por mes para el gráfico
mes_cantidad = (
    df_anio_curr.groupby("MES", observed=True)["CANTIDAD"]
    .sum()
    .reset_index()
)

mes_ventas = (
    df_anio_curr.groupby("MES", observed=True)["RV_TOTAL"]
    .sum()
    .reset_index()
)

# Asegurar orden cronológico de los meses
meses_en_datos = [m for m in ORDEN_MESES if m in mes_cantidad["MES"].values]
mes_cantidad["MES_CAT"] = pd.Categorical(mes_cantidad["MES"], categories=meses_en_datos, ordered=True)
mes_ventas["MES_CAT"] = pd.Categorical(mes_ventas["MES"], categories=meses_en_datos, ordered=True)
mes_cantidad = mes_cantidad.sort_values("MES_CAT")
mes_ventas = mes_ventas.sort_values("MES_CAT")

if modo_vista == "Ventas":
    #mes_cantidad["VALOR_MOSTRADO"] = (mes_cantidad["CANTIDAD"] * 2.67) / 1000
    mes_cantidad["VALOR_MOSTRADO"] = mes_ventas["RV_TOTAL"]
    y_title = "Ventas (Miles S/.)"
    formato_hover = "S/ %{y:,.1f}"
else:
    #mes_cantidad["VALOR_MOSTRADO"] = mes_cantidad["CANTIDAD"] / 1000
    mes_cantidad["VALOR_MOSTRADO"] = mes_cantidad["CANTIDAD"]
    y_title = "Volumen (Miles de Und)"
    formato_hover = "%{y:,.1f} und"

# Asignar color específico a cada mes según la paleta de la imagen
colores = [PALETA_MESES.get(mes, "#3b82f6") for mes in mes_cantidad["MES"]]

fig_bar = go.Figure(
    data=[
        go.Bar(
            x=mes_cantidad["MES"],
            y=mes_cantidad["VALOR_MOSTRADO"],
            text=mes_cantidad["VALOR_MOSTRADO"] // 1000000 if modo_vista == "Ventas" else mes_cantidad["VALOR_MOSTRADO"],
            textposition="outside",
            texttemplate="S/ %{text:,.0f} M" if modo_vista == "Ventas" else "%{text:,.0f} U",
            textfont=dict(color="black", size=12),
            marker_color=colores,
            marker_line_width=0,
            opacity=0.95,
            hovertemplate="<b>%{x}</b><br>" + formato_hover + "<extra></extra>",
        )
    ]
)

fig_bar.update_layout(
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    margin=dict(l=10, r=10, t=10, b=30),
    height=320,
    xaxis=dict(
        showgrid=False,
        categoryorder="array",
        categoryarray=ORDEN_MESES,
        tickfont=dict(size=12, color="#64748b"),
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#f1f5f9",
        gridwidth=1,
        griddash="dot",
        tickfont=dict(size=12, color="#64748b"),
    ),
    showlegend=False,
)

st.plotly_chart(fig_bar, use_container_width=True)


# ------------------------------------------------------------
# SECCION MENSUAL
# ------------------------------------------------------------
meses_anio_curr = [m for m in ORDEN_MESES if m in df_anio_curr["MES"].values]
df_anio_curr["MES"] = pd.Categorical(df_anio_curr["MES"], categories=meses_anio_curr, ordered=True)

mes_titulo_col,mes_sel_col = st.columns([2, 1])
with mes_titulo_col:
    st.subheader(
        "**Resumen ejecutivo**",
        width="content"
        )
with mes_sel_col:
    mes_sel = st.selectbox("Mes", meses_anio_curr, index=0, label_visibility="collapsed")
    if not mes_sel:
        mes_sel = "Enero"

indice_mes = ORDEN_MESES.index(mes_sel)
mes_prev = ORDEN_MESES[indice_mes - 1]

mes_subtitle_col,mes_comp_col = st.columns([2, 1])
with mes_subtitle_col:
    st.markdown(
        "***Comparador***",
        width="content"
        )
with mes_comp_col:
    mes_comparador = st.segmented_control(
        "Comparacion",
        width="stretch",
        options=["Mes anterior", "Año anterior"],
        default="Mes anterior",
        label_visibility="collapsed"
    )
    if not mes_comparador:
        mes_comparador = "Mes anterior"

df_mes_curr = df_anio_curr[df_anio_curr["MES"] == mes_sel]
df_mes_prev = df_anio_curr[df_anio_curr["MES"] == mes_prev]
df_mes_anio_prev = df_anio_prev[df_anio_prev["MES"] == mes_sel]
if mes_sel == "Enero":
    df_mes_prev = df_anio_prev[df_anio_prev["MES"] == mes_prev]

sales_mes_curr = df_mes_curr["RV_TOTAL"].sum() # Mes seleccionado
sales_mes_prev = df_mes_prev["RV_TOTAL"].sum() # Mes anterior al seleccionado
sales_mes_anio_prev = df_mes_anio_prev["RV_TOTAL"].sum()

volume_mes_curr = df_mes_curr["CANTIDAD"].sum()
volume_mes_prev = df_mes_prev["CANTIDAD"].sum()
volume_mes_anio_prev = df_mes_anio_prev["CANTIDAD"].sum()

sales_mes_diff = sales_mes_curr - sales_mes_prev
volume_mes_diff = volume_mes_curr - volume_mes_prev

df_vendedores_mes = (
    df_mes_curr.groupby("VENDEDOR", as_index=False)[["RV_TOTAL"]]
    .sum()
    .sort_values(by="RV_TOTAL", ascending=False)
    .reset_index(drop=True)
)
df_productos_mes = (
    df_mes_curr.groupby("PRODUCTO", as_index=False)[["CANTIDAD"]]
    .sum()
    .sort_values(by="CANTIDAD", ascending=False)
    .reset_index(drop=True)
)

# PKI TOP VENDEDOR - PRODUCTO
df_sales_top_mes = df_vendedores_mes.head(1)
vendedor_top_mes = df_sales_top_mes["VENDEDOR"].iloc[0]
venta_top_mes = df_sales_top_mes["RV_TOTAL"].iloc[0]
df_volume_top_mes = df_productos_mes.head(1)
producto_top_mes = df_volume_top_mes["PRODUCTO"].iloc[0]
volume_top_mes = df_volume_top_mes["CANTIDAD"].iloc[0]

if mes_comparador == "Año anterior":
    sales_mes_diff = sales_mes_curr - sales_mes_anio_prev
    volume_mes_diff = volume_mes_curr - volume_mes_anio_prev

# Cuadrícula 2x2 para las tarjetas de KPI
mes_kpi_col1, mes_kpi_col2 = st.columns(2)
with mes_kpi_col1:
    st.metric(
        "Venta mensual",
        f"S/ {sales_mes_curr:,.0f}",
        delta= f"S/ {sales_mes_diff:,.0f}",
        delta_arrow= "up" if sales_mes_diff > 0 else "down",
        delta_color= "green" if sales_mes_diff > 0 else "red",
        icon= "💸",
        border= True,
        # chart_data= [4,1,5,3,8,4,9,2,4,8,2,2],
        # chart_type= "area",
        delta_description="vs. año anterior" if mes_comparador == "Año anterior" else "vs. mes anterior"
        )
with mes_kpi_col2:
    st.metric(
        "Volumen mensual",
        f"{volume_mes_curr:,.0f} Und",
        delta= volume_mes_diff,
        # delta_arrow= "down",
        icon= "🚀",
        border= True,
        # chart_data= [4,1,5,3,8,4,9,2,4,8,2,2],
        # chart_type= "area",
        delta_description="vs. año anterior" if mes_comparador == "Año anterior" else "vs. mes anterior"
        )

# Cuadrícula 2x2 para las tarjetas de KPI
mes_kpi_col3, mes_kpi_col4 = st.columns(2)
with mes_kpi_col3:
    st.metric(
        "Vendedor Top",
        f"S/ {venta_top_mes:,.2f}",
        # delta= f"S/ {sales_mes_diff:,.0f}",
        # delta_arrow= "up" if sales_mes_diff > 0 else "down",
        # delta_color= "green" if sales_mes_diff > 0 else "red",
        icon= "🧑‍💼",
        border= True,
        # chart_data= [4,1,5,3,8,4,9,2,4,8,2,2],
        # chart_type= "area",
        delta_description=vendedor_top_mes
        )
with mes_kpi_col4:
    st.metric(
        "Producto Top",
        f"{volume_top_mes:,.0f} Und",
        # delta= volume_mes_diff,
        # delta_arrow= "down",
        icon= "🏆",
        border= True,
        # chart_data= [4,1,5,3,8,4,9,2,4,8,2,2],
        # chart_type= "area",
        delta_description=producto_top_mes
        )

# -------------------------------------------------------------
# SECCIÓN ADICIONAL: RANKINGS Y DETALLE
# -------------------------------------------------------------
with st.expander("📊 Ver Top Vendedores y Productos de la Unidad Seleccionada"):
    t_v1, t_v2 = st.columns(2)
    with t_v1:
        st.subheader("🏆 Top Vendedores")
        top_v = (
            df_anio_curr.groupby("VENDEDOR")["CANTIDAD"]
            .sum()
            .reset_index()
            .sort_values(by="CANTIDAD", ascending=False)
            .head(10)
        )
        st.dataframe(top_v.style.format({"CANTIDAD": '{:,.0f} und'}), use_container_width=True, hide_index=True)

    with t_v2:
        st.subheader("📦 Top Productos")
        col_prod = "PRODUCTO" if "PRODUCTO" in df_anio_curr.columns else "PRESENTACION"
        top_p = (
            df_anio_curr.groupby(col_prod)["CANTIDAD"]
            .sum()
            .reset_index()
            .sort_values(by="CANTIDAD", ascending=False)
            .head(10)
        )
        st.dataframe(top_p, use_container_width=True, hide_index=True)

    t2_v1, t2_v2 = st.columns(2)
    with t2_v1:
        st.subheader("🏆 Top Vendedores (S/)")
        top1_v = (
            df_anio_curr.groupby("VENDEDOR")["RV_TOTAL"]
            .sum()
            .reset_index()
            .sort_values(by="RV_TOTAL", ascending=False)
            .head(10)
        )
        st.dataframe(top1_v.style.format({"RV_TOTAL": 'S/ {:,.0f}'}), use_container_width=True, hide_index=True)

    with t2_v2:
        st.subheader("📦 Top Presentacion")
        # col_prod = "PRODUCTO" if "PRODUCTO" in df_anio_curr.columns else "PRESENTACION"
        top2_p = (
            df_anio_curr.groupby("PRESENTACION")["CANTIDAD"]
            .sum()
            .reset_index()
            .sort_values(by="CANTIDAD", ascending=False)
            .head(10)
        )
        st.dataframe(top2_p, width="stretch", hide_index=True)