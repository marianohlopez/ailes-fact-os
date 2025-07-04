import streamlit as st

# Filtro de Año

def year_filter(year):

  # Condición de año en la consulta
  year_condition = ""
  if year != "Todos":
      year_condition = f"AND YEAR(c.cbteFch) = {year}"

  return year_condition