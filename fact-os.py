import streamlit as st
import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

# Cargar el archivo .env
load_dotenv()

# Título de la app
st.title("Pendientes por Obra Social - Año 2025")

# Conexión a la base de datos usando variables de entorno (definidas en los secrets)
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)

cursor = conn.cursor()

# Query SQL (la misma que pasaste)
query = """
SELECT 
    c.NroComprobante, 
    c.cbteFch, 
    c.factura_cobro_descrip, 
    o.os_nombre, 
    p.alumno_nombre, 
    p.alumno_apellido
FROM v_comprobantes c 
JOIN v_os o ON c.os_id = o.os_id 
JOIN v_prestaciones p ON c.prestacion_id = p.prestacion_id
WHERE YEAR(cbteFch) = 2025 
AND factura_cobro_descrip = 'PENDIENTE' COLLATE utf8mb4_0900_ai_ci
"""

cursor.execute(query)
registros = cursor.fetchall()

# Cierre de cursor y conexión
cursor.close()
conn.close()

# Convertir a DataFrame
df = pd.DataFrame(registros, columns=[
                  "NroComprobante", "Fecha", "Estado", "Obra Social", "Nombre", "Apellido"])

# Agrupar por obra social y contar alumnos únicos
df["Alumno"] = df["Nombre"] + " " + df["Apellido"]
conteo = df.groupby("Obra Social")["Alumno"].nunique().reset_index()
conteo = conteo.sort_values(by="Alumno", ascending=False)

# Mostrar tabla y gráfico
st.subheader("Cantidad de alumnos con prestaciones pendientes por obra social")
st.bar_chart(conteo.set_index("Obra Social"))

st.dataframe(df)
