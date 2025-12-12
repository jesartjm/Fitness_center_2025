import random

def suggest_routine(goal, visits_last_30, fav_hours, occupancy):
    score = {}

    if goal == "ganar_músculo":
        score["Fuerza"] = 90
        score["Hipertrofia"] = 85
        score["Cardio"] = 30

    if goal == "perder_grasa":
        score["Cardio HIIT"] = 90
        score["Fuerza"] = 70
        score["Resistencia"] = 80

    if goal == "mantener":
        score["Full Body"] = 75
        score["Movilidad"] = 60
        score["Cardio ligero"] = 60

    # Penalizar zonas muy llenas
    if occupancy > 70:
        for k in score:
            score[k] -= 10

    # Sugerencias finales
    routine = sorted(score.items(), key=lambda x: x[1], reverse=True)[:2]

    return {
        "top1": routine[0][0],
        "top2": routine[1][0],
        "detalles": [
            "Calentamiento 5 min",
            "Ejercicios principales 20–30 min",
            "Accesorios 10 min",
            "Estiramientos 5 min",
        ],
    }


