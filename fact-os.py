import streamlit as st
import plotly.express as px
import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Mi Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Reporte de area contable - Año 2025")

# Conexión a la base de datos
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)

# Ejecutar la query
query = """
SELECT o.os_nombre AS obra_social, COUNT(p.prestacion_id) AS cantidad_prestaciones
FROM v_prestaciones p JOIN v_os o 
ON p.prestacion_os = o.os_id
WHERE prestacion_estado_descrip = "ACTIVA" COLLATE utf8mb4_0900_ai_ci
GROUP BY obra_social
"""
df = pd.read_sql(query, conn)

# Asegurar orden correcto
df = df.sort_values('cantidad_prestaciones', ascending=False)

# Gráfico
fig = px.bar(
    df,
    x='obra_social',
    y='cantidad_prestaciones',
    title='Cantidad de prestaciones por obra social',
    labels={'obra_social': 'Obra Social', 'cantidad_prestaciones': 'Cantidad'},
)

# Ajustar layout para que se use todo el ancho
fig.update_layout(
    xaxis_title=None,
    yaxis_title=None,
    title_x=0.5,  # Centra el título
    margin=dict(l=150, r=0, t=40, b=20),
    width=1200,
    height=500
)

# Mostrar en Streamlit
st.plotly_chart(fig, use_container_width=False)

query2 = """
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
GROUP BY obra_social
HAVING 
    promedio_dias IS NOT NULL
"""

df2 = pd.read_sql(query2, conn)

conn.close()

df2 = df2.sort_values(by='promedio_dias', ascending=True)

# st.subheader("Promedio de días de pago")

fig2 = px.bar(
    df2,
    x="obra_social",
    y="promedio_dias",
    title="Promedio de días de pago",
    labels={"obra_social": "Obra Social", "promedio_dias": "Días promedio"}
)
fig2.update_layout(
    xaxis_title=None,
    yaxis_title=None,
    title_x=0.5,  # Centra el título
    margin=dict(l=150, r=0, t=40, b=20),
    width=1200,
    height=500
)


st.plotly_chart(fig2, use_container_width=False)
