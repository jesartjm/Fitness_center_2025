import streamlit as st
import math
from math import pi
import pandas as pd
import plotly.graph_objects as go

# --- STREAMLIT THEME CONFIG ---
st.set_page_config(
    page_title="Fitness Center App",
    layout="wide",
    page_icon="🏋️",
    initial_sidebar_state="expanded",
)

# --- BUILT-IN THEME (Dark + Yellow Highlights) ---
st.markdown(
    """
    <style>
    :root {
        --primary-color: #ffe04c;
        --background-color: #0e0e0e;
        --card-bg: #1b1b1b;
        --text-color: #e6e6e6;
    }
    body {background-color: var(--background-color); color: var(--text-color);}

    /* --- MICROINTERACCIONES --- */
    .micro-card {
        background: linear-gradient(145deg, #1b1b1b, #0f0f0f);
        padding: 22px;
        border-radius: 20px;
        border: 1px solid #242424;
        transition: all 0.25s ease;
        box-shadow: 0px 0px 15px rgba(255, 224, 76, 0.06);
    }
    .micro-card:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0px 0px 25px rgba(255, 224, 76, 0.25);
    }

    /* Botones animados */
    .stButton>button {
        background-color: var(--primary-color);
        color: black;
        font-weight: 600;
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        border: none;
        transition: 0.2s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 12px rgba(255, 224, 76, 0.75);
    }

    /* Sidebar Slide-In */
    [data-testid="stSidebar"] {
        background-color: #111;
        border-right: 1px solid #333;
        animation: slideIn 0.5s ease-out;
    }
    @keyframes slideIn {
        from {opacity: 0; transform: translateX(-200px);}    
        to {opacity: 1; transform: translateX(0);} 
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- SAMPLE DATA ---
def get_fake_occupancy():
    return {"Zona de Pesas": 67, "Cardio": 42, "Funcional": 29, "Estudios": 18}

# --- COMPONENTS ---
def micro_card(title, body, icon="🔥"):
    st.markdown(f"""
    <div class='micro-card'>
        <div style='font-size:40px;color:#ffe04c'>{icon}</div>
        <h3>{title}</h3>
        <p>{body}</p>
    </div>
    """, unsafe_allow_html=True)


def radar_chart(labels, values):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values, theta=labels, fill="toself"))
    fig.update_layout(
        polar=dict(bgcolor="#0e0e0e", radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        paper_bgcolor="#0e0e0e",
        font_color="#ffe04c",
    )
    st.plotly_chart(fig, use_container_width=True)


def gauge_chart(value, title="KPI"):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6, 1.0))
    ax.barh([0], [100], color="#333333", height=0.28)
    ax.barh([0], [value], color="#ffe04c", height=0.28)
    ax.text(value, 0, f" {value}%", va="center", ha="left", fontsize=14, color="white", fontweight="bold")
    ax.text(0, 0.55, title, va="center", ha="left", fontsize=14, color="white", fontweight="bold")
    ax.set_xlim(0, 100)
    ax.set_yticks([])
    ax.set_xticks([])
    fig.patch.set_facecolor('#0e0e0e')
    ax.set_facecolor('#0e0e0e')
    plt.box(False)
    st.pyplot(fig)(fig, use_container_width=True)

# --- UI HEADER ---
st.markdown("<h1 style='color:#ffe04c;'>🏋️ Fitness Center – Smart Training</h1>", unsafe_allow_html=True)

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


