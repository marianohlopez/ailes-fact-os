import streamlit as st
import plotly.express as px
import pandas as pd
from data.connection import get_connection
from logic.filters import year_filter
from data.query import q_prom_card
from ui.cards import card_total_average
from ui.charts import chart_days_aut
from ui.charts import chart_cant_prest

st.set_page_config(
    page_title="Dashboard-Contable",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS
css = open("styles.css").read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.title("Reporte de area contable - Año 2025")

st.markdown("<div class='space'></div>", unsafe_allow_html=True)

# crear conexión
conn = get_connection()

#--- Filtro de Año

year = st.selectbox("Seleccione el año", ["Todos", "2024", "2025"])

# Condición de año para la consulta
year_condition = year_filter(year)

#--- Tarjeta de promedio total de dif. de días

prom_total = q_prom_card(year_condition, conn)

# Mostrar en tarjeta
card_total_average(year, prom_total)

#--- Leyenda de colores

st.markdown("""
<div style='padding: 10px; border: 1px solid #ccc; border-radius: 10px; background-color: #f9f9f9'>
  <strong>Leyenda de colores:</strong><br>
  <span style='font-weight:bold'>🟩 Verde:</span> Menos de 30 días de pago<br>
  <span style='font-weight:bold'>🟨 Amarillo:</span> Entre 30 y 60 días de pago<br>
  <span style='font-weight:bold'>🟥 Rojo:</span> Más de 60 días de pago
</div>
""", unsafe_allow_html=True)

# Espacio
st.markdown("<div class='space'></div>", unsafe_allow_html=True)

#--- Gráfico de días para autorizar por os

chart_days_aut(year_condition, year, conn)

st.markdown("<div class='space'></div>", unsafe_allow_html=True)

#--- Cant. de prestaciones por OS

chart_cant_prest(year_condition, conn)

#-----------------------------------------------------------------

# Simulamos datos
data = {
    "mes": pd.date_range("2023-01-01", periods=12, freq="M"),
    "OSDE": [100, 120, 130, 110, 90, 150, 160, 170, 155, 180, 190, 200],
    "IOMA": [80, 85, 90, 100, 95, 110, 115, 120, 125, 130, 140, 150]
}
df = pd.DataFrame(data)
df = df.melt(id_vars="mes", var_name="Obra Social", value_name="Cantidad")

# Gráfico de línea
fig = px.line(df, x="mes", y="Cantidad", color="Obra Social", markers=True,
              title="Cantidad de prestaciones por mes")
fig.update_layout(xaxis_title="Mes", yaxis_title="Cantidad")

# Mostrar en Streamlit
# st.plotly_chart(fig)

conn.close()
