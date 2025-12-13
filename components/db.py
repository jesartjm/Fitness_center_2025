import streamlit as st
from supabase import create_client, Client

# ======================================================
# 🔐 SUPABASE CONFIG
# ======================================================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ======================================================
# 👤 PERFIL DE USUARIO
# ======================================================
def get_user_profile(user_id: str):
    res = (
        supabase
        .table("usuarios")
        .select("*")
        .eq("id", user_id)
        .execute()
    )
    return res.data[0] if res.data else None


# ======================================================
# 📊 HISTORIAL DE VISITAS
# ======================================================
def get_user_visits(user_id: str):
    res = (
        supabase
        .table("visitas")
        .select("*")
        .eq("user_id", user_id)
        .order("fecha", desc=True)
        .execute()
    )
    return res.data or []


# ======================================================
# 📅 CLASES DISPONIBLES
# ======================================================
def get_classes():
    res = supabase.table("clases").select("*").execute()
    return res.data or []


# ======================================================
# 🔐 RESERVA ATÓMICA (RPC SEGURO)
# ======================================================
def reserve_class_atomic(user_id: str, class_id: str):
    try:
        res = supabase.rpc(
            "reserve_class_atomic",
            {
                "p_user_id": user_id,
                "p_class_id": class_id,
            },
        ).execute()

        # El RPC retorna texto
        return res.data

    except Exception as e:
        # Nunca romper la app
        return "Error al procesar la reserva"


