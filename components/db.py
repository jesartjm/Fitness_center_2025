import streamlit as st
from supabase import create_client, Client
from datetime import datetime

print("URL:", SUPABASE_URL)
print("KEY:", SUPABASE_KEY[:8], "... cargada")

# ======================================================
# 🔐 LEER SECRETS DESDE STREAMLIT
# ======================================================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Crear cliente
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ======================================================
# 🔹 Obtener perfil de usuario
# ======================================================
def get_user_profile(user_id: str):
    data = (
        supabase.table("usuarios")
        .select("*")
        .eq("id", user_id)
        .single()
        .execute()
    )
    return data.data

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
# 🔹 Obtener clases disponibles
# ======================================================
def get_classes():
    return supabase.table("clases").select("*").execute().data

# ======================================================
# 🔹 Reservar clase (Transaction / RPC)
#


