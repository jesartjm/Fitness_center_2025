import streamlit as st
from supabase import create_client
from datetime import datetime

# =========================
# CONEXIÓN SUPABASE
# =========================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================
# USUARIO
# =========================
def get_user_profile(user_id: str):
    res = (
        supabase.table("usuarios")
        .select("*")
        .eq("id", user_id)
        .execute()
    )
    return res.data[0] if res.data else None


def get_user_visits(user_id: str):
    res = (
        supabase.table("visitas")
        .select("*")
        .eq("user_id", user_id)
        .order("fecha", desc=True)
        .execute()
    )
    return res.data


# =========================
# CLASES
# =========================
def get_classes():
    res = supabase.table("clases").select("*").execute()
    return res.data


def get_reserved_classes(user_id: str):
    """
    Devuelve clases reservadas por el usuario
    JOIN reservas → clases
    """
    res = (
        supabase.table("reservas")
        .select("id, fecha, clases(id, nombre, horario)")
        .eq("user_id", user_id)
        .execute()
    )
    return res.data


# =========================
# RESERVAR CLASE (REAL)
# =========================
def reserve_class_atomic(user_id: str, class_id: str):
    """
    Reserva simple:
    - Inserta reserva
    - Incrementa capacidad_actual
    """

    # 1. Obtener clase
    clase = (
        supabase.table("clases")
        .select("*")
        .eq("id", class_id)
        .execute()
        .data[0]
    )

    if clase["capacidad_actual"] >= clase["capacidad_max"]:
        raise Exception("Clase llena")

    # 2. Insertar reserva
    supabase.table("reservas").insert({
        "user_id": user_id,
        "clase_id": class_id,
        "fecha": datetime.now().isoformat(),
    }).execute()

    # 3. Actualizar capacidad
    supabase.table("clases").update({
        "capacidad_actual": clase["capacidad_actual"] + 1
    }).eq("id", class_id).execute()

    return "Reserva exitosa"



