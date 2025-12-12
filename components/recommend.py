import random

def suggest_routine(user_profile, gym_load):
    objetivo = user_profile.get("goal", "general")
    visitas = user_profile.get("visits", 0)

    if objetivo == "perder grasa":
        focus = "Full body + HIIT"
    elif objetivo == "musculo":
        focus = "Hipertrofia + compuestos"
    else:
        focus = "Entrenamiento balanceado"

    zonas_libres = [z for z, o in gym_load.items() if o < 50]

    return {
        "titulo": f"Rutina recomendada para {objetivo}",
        "descripcion": f"Basado en tus {visitas} visitas y el estado actual del gimnasio.",
        "focus": focus,
        "zonas_sugeridas": zonas_libres or ["(todas ocupadas ahora)"]
    }

