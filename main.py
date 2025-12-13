import streamlit as st
import plotly.graph_objects as go
from components.db import (
    get_user_profile,
    get_user_visits,
    get_classes,
    reserve_class_atomic,
    get_reserved_classes,
)

# =====================================
# CONFIG
# =====================================
st.set_page_config(
    page_title="Smart Gym",
    page_icon="🏋️",
    layout="wide",
)

# =====================================
# CSS / THEME
# =====================================
st.markdown("""
<style>
body { background-color: #0e0e0e; color: white; }
h1,h2,h3 { color: #ffe04c; }

.card {
    background: #151515;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 18px;
    border: 1px solid #222;
}

.kpi {
    font-size: 26px;
    font-weight: 700;
    color: #ffe04c;
}

.small {
    font-size: 13px;
    color: #aaa;
}

[data-testid="stSidebar"] {
    background: #111;
    border-right: 1px solid #222;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# USUARIO SIMULADO
# =====================================
USER_ID = "00000000-0000-0000-0000-000000000001"

perfil = get_user_profile(USER_ID)
if not perfil:
    st.error("Usuario no encontrado")
    st.stop()

visitas = get_user_visits(USER_ID)
clases = get_classes()
reservadas = get_reserved_classes(USER_ID)

# =====================================
# HELPERS
# =====================================
def card(html):
    st.markdown(f"<div class='card'>{html}</div>", unsafe_allow_html=True)

def mini_gauge(value, key):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#ffe04c"},
            "bgcolor": "#222",
        }
    ))
    fig.update_layout(
        height=160,
        margin=dict(l=10,r=10,t=10,b=10),
        paper_bgcolor="#0e0e0e",
        font_color="white",
    )
    st.plotly_chart(fig, use_container_width=True, key=key)

def generar_rutina(objetivo, nivel, dias):
    rutinas = {
        "Ganar músculo": {
            "Principiante": [
                ["Press pecho", "Sentadilla", "Plancha"],
                ["Remo con barra", "Peso muerto", "Crunch"],
            ],
            "Intermedio": [
                ["Press banca", "Sentadilla", "Dominadas"],
                ["Peso muerto", "Press militar", "Core"],
            ],
            "Avanzado": [
                ["Press banca", "Sentadilla frontal", "Dominadas lastradas"],
                ["Peso muerto", "Push press", "Ab wheel"],
            ],
        },
        "Perder grasa": {
            "Principiante": [
                ["Caminata inclinada", "Sentadilla", "Plancha"],
                ["Bici estática", "Zancadas", "Crunch"],
            ],
            "Intermedio": [
                ["HIIT", "Burpees", "Mountain climbers"],
                ["Cuerda", "Kettlebell swing", "Core"],
            ],
            "Avanzado": [
                ["HIIT avanzado", "Saltos pliométricos", "Core"],
                ["Sprints", "Circuito funcional", "Abdominales"],
            ],
        },
        "general": {
            "Principiante": [
                ["Press máquina", "Sentadilla goblet", "Plancha"],
                ["Remo polea", "Peso muerto ligero", "Crunch"],
            ],
            "Intermedio": [
                ["Press banca", "Sentadilla", "Dominadas"],
                ["Peso muerto", "Press hombro", "Core"],
            ],
            "Avanzado": [
                ["Full body pesado", "Sentadilla", "Dominadas"],
                ["Fuerza + cardio", "Circuito funcional", "Core"],
            ],
        },
    }

    # Fallbacks seguros
    objetivo = objetivo if objetivo in rutinas else "general"
    nivel = nivel if nivel in rutinas[objetivo] else "Principiante"

    bloques = rutinas[objetivo][nivel]
    rutina_final = {}

    for i, dia in enumerate(dias):
        rutina_final[dia] = bloques[i % len(bloques)]

    return rutina_final
# =====================================
# HEADER
# =====================================
st.markdown("<h1>🏋️ Smart Fitness Center</h1>", unsafe_allow_html=True)

# =====================================
# MENU
# =====================================
section = st.sidebar.radio(
    "Menú",
    ["Perfil", "Ocupación", "Clases", "Entrenamiento IA"]
)

# =====================================
# PERFIL
# =====================================
if section == "Perfil":
    st.subheader("👤 Perfil")

    c1, c2, c3 = st.columns(3)
    with c1:
        card(f"<div class='kpi'>{perfil['nombre']}</div><div class='small'>Nombre</div>")
    with c2:
        card(f"<div class='kpi'>{perfil['membresia']}</div><div class='small'>Membresía</div>")
    with c3:
        card(f"<div class='kpi'>{len(visitas)}</div><div class='small'>Visitas</div>")

    st.subheader("📅 Clases reservadas")
    if reservadas:
        for r in reservadas:
            card(
                f"<div class='kpi'>{r['clases']['nombre']}</div>"
                f"<div class='small'>{r['clases']['horario']}</div>"
            )
    else:
        st.info("No tienes clases reservadas")

# =====================================
# OCUPACIÓN
# =====================================
elif section == "Ocupación":
    st.subheader("📊 Ocupación actual")

    zonas = {
        "Pesas": 60,
        "Cardio": 35,
        "Funcional": 20,
    }

    cols = st.columns(3)
    for i, (zona, val) in enumerate(zonas.items()):
        with cols[i]:
            card(f"<div class='kpi'>{zona}</div><div class='small'>Ocupación</div>")
            mini_gauge(val, key=f"zona_{zona}")

# =====================================
# CLASES
# =====================================
elif section == "Clases":
    st.subheader("📅 Reservar clases")

    for c in clases:
        percent = int((c["capacidad_actual"] / c["capacidad_max"]) * 100)

        card(
            f"<div class='kpi'>{c['nombre']}</div>"
            f"<div class='small'>Horario: {c['horario']}</div>"
            f"<div class='small'>Cupo: {c['capacidad_actual']} / {c['capacidad_max']}</div>"
        )

        mini_gauge(percent, key=f"class_{c['id']}")

        if percent < 100:
            if st.button(f"Reservar {c['nombre']}", key=f"btn_{c['id']}"):
                try:
                    reserve_class_atomic(USER_ID, c["id"])
                    st.success("Reserva confirmada")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))
        else:
            st.error("Clase llena")

# =====================================
# ENTRENAMIENTO IA
# =====================================
elif section == "Entrenamiento IA":
    st.subheader("🤖 Rutina personalizada")

    objetivo = perfil.get("objetivo", "general")

    nivel = st.selectbox("Nivel", ["Principiante", "Intermedio", "Avanzado"])
    tiempo = st.selectbox("Tiempo por sesión (min)", [30, 45, 60])
    dias = st.multiselect(
        "Días disponibles",
        ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    )

    if st.button("Generar rutina"):
        if not dias:
            st.warning("Selecciona al menos un día para entrenar")
        else:
            rutina = generar_rutina(objetivo, nivel, dias)

            for dia, ejercicios in rutina.items():
                html = f"""
                <div class='kpi'>{dia}</div>
                <ul>
                    {''.join([f"<li>{e}</li>" for e in ejercicios])}
                </ul>
                """
                card(html)
