import supabase
from datetime import datetime
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

sb = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def get_user_profile(user_id):
    res = sb.table("users").select("*").eq("id", user_id).execute()
    if res.data:
        return res.data[0]
    return None

def get_visit_stats(user_id):
    res = sb.table("visits").select("id").eq("user_id", user_id).execute()
    return len(res.data)

def get_classes():
    return sb.table("classes").select("*").execute().data

def reserve_class_atomic(user_id, class_id):
    res = sb.rpc(
        "reserve_class_atomic",
        {"p_user_id": user_id, "p_class_id": class_id}
    ).execute()
    return res.data

