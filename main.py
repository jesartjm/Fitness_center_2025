import streamlit as st
import plotly.graph_objects as go
from components.db import (
    get_user_profile,
    get_user_visits,
    get_classes,
    reserve_class_atomic,
)
from components.recommend import suggest_routine

st.set_page_config(
    page_title="Fitness Center",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ======================
# 🎨 ESTILOS
# ======================
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #0e0e0e;
    color: white;
}

.sidebar .sidebar-content {
    background-color: #111;
}

.card {
    background-color: #151515;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 18px;
    border: 1px solid #222;
}

.kpi {
    font-size: 32px;
    font-weight: bold;
    color: #ffe04c;
}

.small {
    color: #aaa;
}

button {
    background-color: #ffe04c !important;
    color: black !important;
    border-radius: 8px !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

def mini_gauge(percent, label):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=percent,
        title={"text": label, "font": {"color": "white"}},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#ffe04c"},
            "bgcolor": "#1a1a1a",
            "borderwidth": 0,
        },
        number={"font": {"color": "white"}}
    ))

    fig.update_layout(
        height=180,
        margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor="#0e0e0e",
        font_color="white",
    )
    st.plotly_chart(fig, use_container_width=True)

st.sidebar.title("🏋️ Fitness Center")
menu = st.sidebar.radio(
    "Menú",
    ["🏠 Dashboard", "📊 Ocupación", "📅 Clases", "👤 Perfil"]
)

USER_ID = "00000000-0000-0000-0000-000000000001"
perfil = get_user_profile(USER_ID)
visitas = get_user_visits(USER_ID)

if menu == "🏠 Dashboard":
    st.title("🏠 Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card"><div class="kpi">'
                    f'{len(visitas)}</div><div class="small">Visitas</div></div>',
                    unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card"><div class="kpi">'
                    f'{perfil["membresia"]}</div><div class="small">Membresía</div></div>',
                    unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card"><div class="kpi">'
                    f'{perfil["objetivo"]}</div><div class="small">Objetivo</div></div>',
                    unsafe_allow_html=True)

    st.subheader("🤖 Entrenamiento sugerido")
    routine = suggest_routine(
        goal=perfil["objetivo"],
        visits_count=len(visitas),
        preferred_time="Tarde",
        occupancy=65,
    )

    for r in routine:
        st.markdown(f"- {r}")

elif menu == "📊 Ocupación":
    st.title("📊 Ocupación actual")

    zonas = {
        "Cardio": 72,
        "Pesas": 85,
        "Funcional": 40,
    }

    cols = st.columns(3)
    for col, (zona, percent) in zip(cols, zonas.items()):
        with col:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            mini_gauge(percent, zona)
            st.markdown('</div>', unsafe_allow_html=True)

elif menu == "📅 Clases":
    st.title("📅 Clases disponibles")

    clases = get_classes()

    for c in clases:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader(c["nombre"])
        st.write(f"🕒 {c['horario']}")
        st.write(f"👥 {c['capacidad_actual']} / {c['capacidad_max']}")

        if st.button(f"Reservar {c['nombre']}", key=c["id"]):
            result = reserve_class_atomic(USER_ID, c["id"])
            st.success(result)

        st.markdown('</div>', unsafe_allow_html=True)

elif menu == "👤 Perfil":
    st.title("👤 Mi perfil")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(f"**Nombre:** {perfil['nombre']}")
    st.write(f"**Email:** {perfil['email']}")
    st.write(f"**Membresía:** {perfil['membresia']}")
    st.write(f"**Objetivo:** {perfil['objetivo']}")
    st.write(f"**Visitas acumuladas:** {len(visitas)}")
    st.markdown('</div>', unsafe_allow_html=True)





