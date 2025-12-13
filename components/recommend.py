import random
def suggest_routine(goal, visits_count, preferred_time, occupancy):
    routine = []

    if goal == "fuerza":
        routine.append("🏋️ Rutina de fuerza (pesas libres)")
    elif goal == "cardio":
        routine.append("🏃 Cardio HIIT 30 min")
    else:
        routine.append("🤸 Entrenamiento funcional")

    if visits_count < 5:
        routine.append("📌 Intensidad baja – adaptación")
    elif visits_count < 15:
        routine.append("📈 Intensidad media")
    else:
        routine.append("🔥 Intensidad alta")

    if occupancy > 80:
        routine.append("⏰ Recomendado entrenar en horas valle")
    else:
        routine.append("✅ Buen momento para entrenar")

    routine.append(f"🕒 Horario ideal: {preferred_time}")

    return routine


