import streamlit as st
from supabase import create_client
from datetime import datetime

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ======================================================
# 🔹 Obtener perfil de usuario
# ======================================================
def get_user_profile(user_id: str):
    data = (
        supabase.table("usuarios")
        .select("*")
        .eq("id", user_id)
        .execute()
    )
    return data.data[0] if data.data else None

# ======================================================
# 🔹 Obtener historial de visitas
# ======================================================
def get_user_visits(user_id: str):
    data = (
        supabase.table("visitas")
        .select("*")
        .eq("user_id", user_id)
        .order("fecha", desc=True)
        .execute()
    )
    return data.data

# ======================================================
# 🔹 Obtener clases
# ======================================================
def get_classes():
    return supabase.table("clases").select("*").execute().data

# ======================================================
# 🔹 Reservar clase (sin RPC, versión simplificada)
# ======================================================
def reserve_class_atomic(user_id: str, class_id: str):
    return supabase.table("reservas").insert({
        "user_id": user_id,
        "class_id": class_id,
        "fecha": datetime.now().isoformat()
    }).execute()

