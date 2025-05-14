import streamlit as st
import plotly.express as px
import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

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

# Conexión a la base de datos
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)

# Filtro de Año
year = st.selectbox("Seleccione el año", ["Todos", "2024", "2025"])

# Condición de año en la consulta
year_condition = ""
if year != "Todos":
    year_condition = f"AND YEAR(c.cbteFch) = {year}"

# Tarjeta de promedio total de dif. de días

q_prom_card = f""" 
    SELECT 
        ROUND(AVG(DATEDIFF(c.cobro_fec, c.cbteFch)), 2) AS promedio_total
    FROM 
        v_comprobantes c JOIN v_os o
    ON c.os_id = o.os_id
    WHERE 
        c.cbteFch IS NOT NULL
        AND c.cobro_fec IS NOT NULL
        AND o.os_nombre NOT IN ('OSDE')
        {year_condition};
"""

df_prom_card = pd.read_sql(q_prom_card, conn)

prom_total = df_prom_card['promedio_total'][0]


# Mostrar en tarjeta

st.markdown(f"""
    <div class="card-container">
        <div class="card">
            <div class="card-title">Promedio total de días de pago ({year})</div>
            <div class="card-value">{prom_total}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<div class='space'></div>", unsafe_allow_html=True)

# Gráfico de días para autorizar por os

q_days_aut = f"""
SELECT 
    o.os_nombre AS obra_social,
    ROUND(AVG(DATEDIFF(c.cobro_fec, c.cbteFch)), 2) AS promedio_dias
FROM 
    v_comprobantes c JOIN v_os o
ON c.os_id = o.os_id
WHERE 
    c.cbteFch IS NOT NULL
    AND c.cobro_fec IS NOT NULL
    AND o.os_nombre NOT IN ('OSDE')
    {year_condition}
GROUP BY obra_social
HAVING 
    promedio_dias IS NOT NULL
"""

df_days_aut = pd.read_sql(q_days_aut, conn)

df_days_aut = df_days_aut.sort_values(by='promedio_dias', ascending=True)

fig_days_aut = px.bar(
    df_days_aut,
    x="obra_social",
    y="promedio_dias",
    title=f"Promedio de días de pago por obra social ({year})",
    labels={"obra_social": "Obra Social", "promedio_dias": "Días promedio"},
    text='promedio_dias'
)

fig_days_aut.update_layout(
    title_x=0.5,
    height=600
)


st.plotly_chart(fig_days_aut, use_container_width=False)

st.markdown("<div class='space'></div>", unsafe_allow_html=True)


# Cant. de prestaciones por OS

q_prest_os = """
SELECT o.os_nombre AS obra_social, COUNT(p.prestacion_id) AS cantidad_prestaciones
FROM v_prestaciones p JOIN v_os o 
ON p.prestacion_os = o.os_id
WHERE prestacion_estado_descrip = "ACTIVA" COLLATE utf8mb4_0900_ai_ci
GROUP BY obra_social
"""
df_prest_os = pd.read_sql(q_prest_os, conn)

conn.close()

# Asegurar orden correcto
df_prest_os = df_prest_os.sort_values('cantidad_prestaciones', ascending=False)

# Gráfico
fig_prest_os = px.bar(
    df_prest_os,
    x='obra_social',
    y='cantidad_prestaciones',
    title='Cantidad de prestaciones por obra social',
    labels={'obra_social': 'Obra Social', 'cantidad_prestaciones': 'Cantidad'},
    text='cantidad_prestaciones'
)

# Ajustar layout para que se use todo el ancho
fig_prest_os.update_layout(
    title_x=0.5,
    height=600
)

# Mostrar en Streamlit
st.plotly_chart(fig_prest_os, use_container_width=False)




