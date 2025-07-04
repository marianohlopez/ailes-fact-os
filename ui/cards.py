import streamlit as st

def card_total_average(year, prom_total):

  st.markdown(f"""
      <div class="card-container">
          <div class="card">
              <div class="card-title">Promedio total de días de pago ({year})</div>
              <div class="card-value">{prom_total}</div>
          </div>
      </div>
  """, unsafe_allow_html=True)