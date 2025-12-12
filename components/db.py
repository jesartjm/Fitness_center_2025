import os
from supabase import create_client, Client
from datetime import datetime

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------
# 🔹 Obtener perfil de usuario
# -------------------------
def get_user_profile(user_id: str):
    data = (
        supabase.table("usuarios")
        .select("*")
        .eq("id", user_id)
        .single()
        .execute()
    )
    return data.data

# -------------------------
# 🔹 Obtener historial de visitas
# -------------------------
def get_user_visits(user_id: str):
    data = (
        supabase.table("visitas")
        .select("*")
        .eq("user_id", user_id)
        .order("fecha", desc=True)
        .execute()
    )
    return data.data

# -------------------------
# 🔹 Obtener clases
# -------------------------
def get_classes():
    return supabase.table("clases").select("*").execute().data

# -------------------------
# 🔹 Reservar una clase (llama el RPC)
# -------------------------
def reserve_class_atomic(user_id: str, class_id: str):
    result = supabase.rpc(
        "reserve_class_atomic",
        {
            "p_user_id": user_id,
            "p_class_id": class_id,
        },
    ).execute()

    return result.data

