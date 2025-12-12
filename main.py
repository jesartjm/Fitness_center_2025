import streamlit as st
import math
from math import pi
import pandas as pd
import plotly.graph_objects as go

# --- SIDEBAR NAV ---
section = st.sidebar.radio(
"Menú",
["Ocupación en Tiempo Real", "Dashboard Avanzado", "Guía Técnica", "Clases", "Recomendaciones"],
)


# --- SECTIONS ---
if section == "Ocupación en Tiempo Real":
st.header("📊 Ocupación en Tiempo Real")
data = get_fake_occupancy()
cols = st.columns(2)
i = 0
for zona, percent in data.items():
with cols[i % 2]:
micro_card(zona, f"Ocupación actual: {percent}%", "📍")
gauge_chart(percent, title=zona)
i += 1


elif section == "Dashboard Avanzado":
st.header("📈 Dashboard Avanzado – KPIs del Gimnasio")


col1, col2, col3 = st.columns(3)
with col1:
micro_card("Asistencia Hoy", "542 miembros", "👥")
with col2:
micro_card("Promedio Ocupación", "58%", "📊")
with col3:
micro_card("Clases Activas", "12 clases en curso", "🔥")


st.subheader("Radar Chart – Perfil del Gimnasio")
labels = ["Fuerza", "Cardio", "Movilidad", "Funcional", "HIIT"]
values = [78, 63, 55, 82, 90]
radar_chart(labels, values)


elif section == "Guía Técnica":
st.header("🦾 Guía Técnica Inteligente")
movimiento = st.selectbox("Ejercicio", ["Sentadilla", "Peso muerto", "Press banca", "Remo"])
if st.button("Mostrar sugerencia técnica"):
micro_card("Sugerencia técnica", f"Posible error en {movimiento}. Ajusta postura.", "⚠️")


elif section == "Clases":
st.header("📅 Reservas de Clases")
clases = [
{"nombre": "HIIT", "hora": "18:00", "capacidad": 20, "ocupados": 17},
{"nombre": "Yoga", "hora": "19:00", "capacidad": 25, "ocupados": 25},
{"nombre": "Spinning", "hora": "20:00", "capacidad": 15, "ocupados": 12},
]


for c in clases:
percent = int((c["ocupados"] / c["capacidad"]) * 100)
micro_card(f"{c['nombre']} – {c['hora']}", "Disponibilidad:", "📌")
gauge_chart(percent, title=c["nombre"])
if percent < 100:
st.button(f"Reservar {c['nombre']}")
else:
st.error("Clase llena")
st.button(f"Lista de espera — {c['nombre']}")


elif section == "Recomendaciones":
st.header("🤖 Recomendaciones Personalizadas")
objetivo = st.selectbox("Objetivo", ["Perder grasa", "Ganar músculo", "Mejorar resistencia"])
frecuencia = st.slider("Entrenos por semana", 1, 7, 3)


if st.button("Generar recomendaciones"):
micro_card("Horario óptimo", "14:00–17:00 – Menor ocupación", "⏱️")
if objetivo == "Ganar músculo":
micro_card("Rutina ideal", "Push/Pull/Legs con sobrecarga progresiva", "💪")
elif objetivo == "Perder grasa":
micro_card("Rutina ideal", "Circuitos + cardio estable", "🔥")
else:
micro_card("Rutina ideal", "Funcional + intervalos", "🏃")
