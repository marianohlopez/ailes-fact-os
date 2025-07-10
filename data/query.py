import pandas as pd
from utils.utils import get_color

#--- Tarjeta de promedio total de dif. de días

def q_prom_card(year_condition, conn):
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

  return df_prom_card['promedio_total'][0]

#--- Gráfico de días para autorizar por os

def q_days_aut(year_condition, conn):
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

  df_days_aut = pd.concat([
      df_days_aut,
      pd.DataFrame([{
          "obra_social": "OSDE",
          "promedio_dias": 60
      }])
  ], ignore_index=True)

  df_days_aut["color"] = df_days_aut["promedio_dias"].apply(get_color)

  return df_days_aut.sort_values(by='promedio_dias', ascending=True)

# Cant. de prestaciones por OS

def q_prest_os(conn):

  q_prest_os = """
  SELECT o.os_nombre AS obra_social, COUNT(p.prestacion_id) AS cantidad_prestaciones
  FROM v_prestaciones p JOIN v_os o 
  ON p.prestacion_os = o.os_id
  WHERE prestacion_estado_descrip = "ACTIVA" COLLATE utf8mb4_0900_ai_ci
  GROUP BY obra_social
  """
  df_prest_os = pd.read_sql(q_prest_os, conn)

  # Asegurar orden correcto
  df_prest_os = df_prest_os.sort_values('cantidad_prestaciones', ascending=False)

  return df_prest_os