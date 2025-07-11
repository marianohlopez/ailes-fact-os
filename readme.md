# 📊 Dashboard Contable – Año 2025

Este proyecto es un **dashboard interactivo en Streamlit** que analiza los tiempos de cobro y las prestaciones activas de cada Obra Social (OS) durante el año 2025. Permite a contaduría identificar rápidamente demoras de pago, volúmenes de prestaciones y tendencias mensuales.

## Deployment: https://ailes-contable.streamlit.app/

---

## 🚀 Funcionalidades principales

| Bloque                                          | Descripción                                                                                                                    |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **Tarjeta KPI**                                 | Promedio de días transcurridos entre la fecha del comprobante (`cbteFch`) y la fecha de cobro (`cobro_fec`), filtrable por año |
| **Leyenda de colores**                          | Indicador visual de desempeño de pago                                                                                          |
| 🟩 < 30 días ➜ excelente                        |                                                                                                                                |
| 🟨 30 – 60 días ➜ aceptable                     |                                                                                                                                |
| 🟥 > 60 días ➜ crítico                          |                                                                                                                                |
| **Gráfico de barras – Promedio de pago por OS** | Tiempo medio (días) de cobro para cada Obra Social, coloreado según la leyenda                                                 |
| **Gráfico de barras – Volumen de prestaciones** | Cantidad de prestaciones ACTIVA por OS en 2025                                                                                 |
| **Selector de Año**                             | Permite comparar métricas entre 2024, 2025 o todos los años                                                                    |

---

## 🛠️ Stack tecnológico

- **Python 3.10+**
- **Streamlit 1.x**
- **Plotly Express**
- **MySQL 8**
- **pandas**
- **python‑dotenv**

---

## 📸 Capturas de pantalla

<img width="1286" height="537" alt="image" src="https://github.com/user-attachments/assets/58532c8f-62cb-4234-9381-bf6f4016f873" />

<img width="1276" height="387" alt="image" src="https://github.com/user-attachments/assets/25a5bf69-96cc-4965-8da5-0709f1a9ddb4" />
