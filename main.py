import streamlit as st
import plotly.graph_objects as go
from components.db import (
    get_user_profile,
    get_user_visits,
    get_classes,
    reserve_class_atomic,
)

# ================================
# CONFIG GENERAL
# ================================
st.set_page_config(
    page_title="Fitness Center App",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ================================
# THEME + CSS
# ================================
st.markdown(
    """
    <style>
    body { background-color: #0e0e0e; color: white; }

    h1, h2, h3, h4, h5 { color: #ffe04c; }

    .card {
        background: #151515;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 18px;
        border: 1px solid #222;
        transition: 0.25s ease;
    }

    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 0 20px rgba(255,224,76,0.25);
    }

    .kpi {
        font-size: 28px;
        font-weight: 700;
        color: #ffe04c;
    }

    .small { color: #aaa; font-size: 13px; }

    [data-testid="stSidebar"] {
        background: #111;
        border-right: 1px solid #222;
        animation: slideIn 0.4s ease;
    }

    @keyframes slideIn {
        from { transform: translateX(-200px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ================================
# USUARIO SIMULADO
# ================================
USER_ID = "00000000-0000-0000-0000-000000000001"

perfil = get_user_profile(USER_ID)

if not perfil:
    st.error("Usuario no encontrado en Supabase")
    st.stop()

visitas = get_user_visits(USER_ID)
clases = get_classes()

# ================================
# COMPONENTES
# ================================

def card(html):
    st.markdown(f"<div class='card'>{html}</div>", unsafe_allow_html=True)


def mini_gauge(value):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#ffe04c"},
                "bgcolor": "#222",
                "borderwidth": 0,
            },
        )
    )
    fig.update_layout(
        height=180,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="#0e0e0e",
        font_color="white",
    )
    st.plotly_chart(fig, use_container_width=True)

# ================================
# HEADER
# ================================
st.markdown("<h1>🏋️ Fitness Center – Smart Gym</h1>", unsafe_allow_html=True)

# ================================
# MENU
# ================================
section = st.sidebar.radio(
    "Menú",
    [
        "Perfil",
        "Ocupación",
        "Clases",
        "Recomendaciones",
    ],
)

# ================================
# PERFIL
# ================================
if section == "Perfil":
    st.subheader("👤 Perfil del Usuario")

    c1, c2, c3 = st.columns(3)
    with c1:
        card(f"<div class='kpi'>{perfil.get('nombre','-')}</div><div class='small'>Nombre</div>")
    with c2:
        card(f"<div class='kpi'>{perfil.get('membresia','No asignada')}</div><div class='small'>Membresía</div>")
    with c3:
        card(f"<div class='kpi'>{len(visitas)}</div><div class='small'>Visitas acumuladas</div>")

# ================================
# OCUPACIÓN
# ================================
elif section == "Ocupación":
    st.subheader("📊 Ocupación del Gimnasio")

    zonas = {
        "Pesas": 65,
        "Cardio": 40,
        "Funcional": 25,
    }

    cols = st.columns(3)
    for i, (zona, val) in enumerate(zonas.items()):
        with cols[i]:
            card(f"<div class='kpi'>{zona}</div><div class='small'>Ocupación</div>")
            mini_gauge(val)

# ================================
# CLASES
# ================================
elif section == "Clases":
    st.subheader("📅 Reservar clases")

    for c in clases:
        percent = int((c["capacidad_actual"] / c["capacidad_max"]) * 100)

        card(
            f"""
            <div class='kpi'>{c['nombre']}</div>
            <div class='small'>Horario: {c['horario']}</div>
            <div class='small'>Ocupación: {c['capacidad_actual']} / {c['capacidad_max']}</div>
            """
        )

        mini_gauge(percent)

        if percent < 100:
            if st.button(f"Reservar {c['nombre']}", key=c["id"]):
                msg = reserve_class_atomic(USER_ID, c["id"])
                st.success(msg)
                st.rerun()
        else:
            st.error("Clase llena")

# ================================
# RECOMENDACIONES IA
# ================================
elif section == "Recomendaciones":
    st.subheader("🤖 Entrenamiento sugerido")

    objetivo = perfil.get("objetivo", "general")
    frecuencia = st.slider("Sesiones por semana", 1, 6, 3)

    if st.button("Generar rutina"):
        if objetivo == "fuerza":
            rutina = "Push / Pull / Legs con sobrecarga progresiva"
        elif objetivo == "resistencia":
            rutina = "Cardio intervalos + funcional"
        else:
            rutina = "Full body balanceado"

        card(
            f"""
            <div class='kpi'>Rutina recomendada</div>
            <div>{rutina}</div>
            <div class='small'>Basado en objetivo, visitas y ocupación</div>
            """
        )






