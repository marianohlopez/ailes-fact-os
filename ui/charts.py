import streamlit as st
import plotly.express as px
from data.query import q_days_aut
from data.query import q_prest_os
from utils.utils import get_color



def chart_days_aut(year_condition, year):

  df_days_aut = q_days_aut(year_condition)

  fig_days_aut = px.bar(
      df_days_aut,
      x="obra_social",
      y="promedio_dias",
      color="color",
      color_discrete_map={
          "verde": "green",
          "amarillo": "gold",
          "rojo": "red"
      },
      title=f"Promedio de días de pago por obra social ({year})",
      labels={"obra_social": "Obra Social", "promedio_dias": "Días promedio"},
      text='promedio_dias'
  )

  fig_days_aut.update_layout(
      title_x=0.5,
      height=600,
      showlegend=False
  )

  st.plotly_chart(fig_days_aut, use_container_width=False)

#--- Cant. de prestaciones por OS

def chart_cant_prest(year_condition):

  df_prest_os = q_prest_os()
  df_days_aut = q_days_aut(year_condition)

  df_prest_os = df_prest_os.merge(
      df_days_aut[['obra_social', 'color']],
      on='obra_social',
      how='left'
  )

  # Rellenar colores faltantes con gris
  df_prest_os['color'] = df_prest_os['color'].fillna('gris')

  color_discrete_map = {
      "verde": "green",
      "amarillo": "gold",
      "rojo": "red",
      "gris": "gray"
  }

  # Gráfico
  fig_prest_os = px.bar(
      df_prest_os,
      x='obra_social',
      y='cantidad_prestaciones',
      color='color',
      color_discrete_map=color_discrete_map,
      title='Cantidad de prestaciones activas por obra social del año 2025',
      labels={'obra_social': 'Obra Social', 'cantidad_prestaciones': 'Cantidad'},
      text='cantidad_prestaciones',
      category_orders={"obra_social": df_prest_os["obra_social"].tolist()}
  )

  # Ajustar layout para que se use todo el ancho
  fig_prest_os.update_layout(
      title_x=0.5,
      height=600,
      showlegend=False
  )

  # Mostrar en Streamlit
  st.plotly_chart(fig_prest_os, use_container_width=False)