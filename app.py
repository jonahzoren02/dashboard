import pandas as pd
import plotly.express as px
import streamlit as st

# Lista maestra para ordenar los meses de manera cronológica
ORDEN_MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Setiembre", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

# 1. Configuración de la página (Ancho completo y título)
st.set_page_config(page_title="Dashboard de Ventas", page_icon="📊", layout="wide")
st.title("📊 Tablero de Control de Ventas y Vendedores")


# 2. Función para cargar datos rápido (usa caché para no leer el Excel cada vez)
@st.cache_data
def cargar_datos():
    # Indicamos header=1 porque los encabezados reales están en la fila 2 del Excel
    df = pd.read_excel("ventas.xlsx", header=1)

    # Limpiamos espacios extra en los nombres de las columnas por si acaso
    df.columns = df.columns.str.strip()

    # Filtramos solo los registros donde hubo salida (ventas) mayor a 0
    df = df[df["SALIDA CANTIDAD"] > 0]

    # Convertimos la columna MES a tipo categórico con orden cronológico
    meses_presentes = [m for m in ORDEN_MESES if m in df["MES"].values]
    df["MES"] = pd.Categorical(df["MES"], categories=meses_presentes, ordered=True)

    return df


# Cargamos los datos con un mensaje de espera
with st.spinner("Cargando los 94,000 registros..."):
    df = cargar_datos()

# 3. Barra lateral de Filtros
st.sidebar.header("🔍 Filtros")

# Filtro de Año
anios = ["Todos"] + sorted(df["AÑO"].dropna().unique().tolist())
anio_sel = st.sidebar.selectbox("Selecciona el Año:", anios)

# Filtro de Mes (orden cronológico)
meses_en_datos = [m for m in ORDEN_MESES if m in df["MES"].unique()]
meses = ["Todos"] + meses_en_datos
mes_sel = st.sidebar.selectbox("Selecciona el Mes:", meses)

# Filtro de Vendedor
vendedores = ["Todos"] + sorted(
    df["VENDEDOR"].dropna().astype(str).unique().tolist()
)
vendedor_sel = st.sidebar.selectbox("Selecciona el Vendedor:", vendedores)

# Aplicamos los filtros al dataframe
df_filtrado = df.copy()
if anio_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["AÑO"] == anio_sel]
if mes_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["MES"] == mes_sel]
if vendedor_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["VENDEDOR"] == vendedor_sel]

# 4. Tarjetas de KPI Principales
st.markdown("### 📈 Indicadores Clave (KPI)")
col1, col2, col3, col4 = st.columns(4)

total_unidades = df_filtrado["SALIDA CANTIDAD"].sum()
total_operaciones = len(df_filtrado)
clientes_unicos = df_filtrado["PARTNER"].nunique()
productos_unicos = df_filtrado["PRODUCTO"].nunique()

col1.metric("Total Unidades Vendidas", f"{total_unidades:,.0f}")
col2.metric("Total Operaciones / Guías", f"{total_operaciones:,.0f}")
col3.metric("Clientes Atendidos", f"{clientes_unicos:,.0f}")
col4.metric("Productos Distintos", f"{productos_unicos:,.0f}")

st.markdown("---")

# 5. Gráficos Interactivos
col_izq, col_der = st.columns(2)

# Gráfico 1: Top 10 Mejores Vendedores
with col_izq:
    st.subheader("🏆 Top 10 Mejores Vendedores (Unidades)")
    top_vendedores = (
        df_filtrado.groupby("VENDEDOR")["SALIDA CANTIDAD"]
        .sum()
        .reset_index()
        .sort_values(by="SALIDA CANTIDAD", ascending=False)
        .head(10)
    )
    fig_vend = px.bar(
        top_vendedores,
        x="SALIDA CANTIDAD",
        y="VENDEDOR",
        orientation="h",
        text_auto=".2s",
        color="SALIDA CANTIDAD",
        color_continuous_scale="Blues",
    )
    fig_vend.update_layout(
        yaxis={"categoryorder": "total ascending"}, showlegend=False
    )
    st.plotly_chart(fig_vend, use_container_width=True)

# Gráfico 2: Top 10 Productos Más Vendidos
with col_der:
    st.subheader("📦 Top 10 Productos Más Vendidos")
    top_productos = (
        df_filtrado.groupby("PRODUCTO")["SALIDA CANTIDAD"]
        .sum()
        .reset_index()
        .sort_values(by="SALIDA CANTIDAD", ascending=False)
        .head(10)
    )
    fig_prod = px.bar(
        top_productos,
        x="SALIDA CANTIDAD",
        y="PRODUCTO",
        orientation="h",
        text_auto=".2s",
        color="SALIDA CANTIDAD",
        color_continuous_scale="Teal",
    )
    fig_prod.update_layout(
        yaxis={"categoryorder": "total ascending"}, showlegend=False
    )
    st.plotly_chart(fig_prod, use_container_width=True)

# Gráfico 3: Evolución de Ventas por Mes
st.subheader("📅 Evolución de Ventas por Mes")
ventas_mes = (
    df_filtrado.groupby(["AÑO", "MES"], observed=True)["SALIDA CANTIDAD"]
    .sum()
    .reset_index()
)
# Convertimos AÑO a texto para una leyenda limpia y ordenamos cronológicamente
ventas_mes["AÑO"] = ventas_mes["AÑO"].astype(str)
ventas_mes = ventas_mes.sort_values(by=["AÑO", "MES"])

fig_mes = px.line(
    ventas_mes,
    x="MES",
    y="SALIDA CANTIDAD",
    color="AÑO",
    markers=True,
    category_orders={"MES": ORDEN_MESES, "AÑO": sorted(ventas_mes["AÑO"].unique())},
)
fig_mes.update_xaxes(categoryorder="array", categoryarray=ORDEN_MESES)
st.plotly_chart(fig_mes, use_container_width=True)

# 6. Tabla de datos resumida
with st.expander("📋 Ver detalle de los datos filtrados"):
    st.dataframe(df_filtrado.head(100), use_container_width=True)
