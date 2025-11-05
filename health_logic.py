def calculate_bmi(height_cm, weight_kg):
    return round(weight_kg / ((height_cm/100) ** 2), 1)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    if 18.5 <= bmi <= 24.9:
        return "Normal weight"
    if 25 <= bmi <= 29.9:
        return "Overweight"
    return "Obese"

def health_score_and_classification(data, bmi):
    # BMI Score
    if 18.5 <= bmi <= 24.9:
        bmi_score = 100
    elif 17 <= bmi < 18.5 or 25 <= bmi <= 29.9:
        bmi_score = 70
    else:
        bmi_score = 40

    # Sleep Score
    if 7 <= data['sleep'] <= 9:
        sleep_score = 100
    elif 6 <= data['sleep'] < 7 or 9 < data['sleep'] <= 10:
        sleep_score = 70
    else:
        sleep_score = 40

    # Hydration
    if 2 <= data['water'] <= 3:
        water_score = 100
    elif 1 <= data['water'] < 2 or 3 < data['water'] <= 4:
        water_score = 70
    else:
        water_score = 40

    # Exercise
    if data['exercise'] >= 30:
        exercise_score = 100
    elif 15 <= data['exercise'] < 30:
        exercise_score = 70
    else:
        exercise_score = 40

    # Weighted Health Score
    score = round(
        0.3 * bmi_score +
        0.2 * sleep_score +
        0.2 * water_score +
        0.3 * exercise_score
    )

    # Classification
    if score >= 80:
        classification = "Healthy"
    elif score >= 60:
        classification = "Needs Improvement"
    else:
        classification = "At Risk"

    detail = {
        "BMI Score": bmi_score,
        "Sleep Score": sleep_score,
        "Water Score": water_score,
        "Exercise Score": exercise_score,
    }
    return score, classification, detail


def generate_personal_suggestion(data, bmi, classification):
    parts = []

    # BMI-based guidance
    if bmi < 18.5:
        parts.append("Increase nutrient-dense calories (whole grains, legumes, nuts, dairy) and add 2–3 strength sessions/week to build lean mass.")
    elif 18.5 <= bmi <= 24.9:
        parts.append("Maintain your weight with balanced meals (plate: 1/2 vegetables, 1/4 protein, 1/4 carbs) and regular activity.")
    elif 25 <= bmi <= 29.9:
        parts.append("Aim for a modest calorie deficit (200–400 kcal/day), prioritize protein and vegetables, and walk 30–45 minutes daily.")
    else:
        parts.append("Start with a gentle calorie deficit and daily walking; limit refined sugar and fried foods; consider supervised strength training.")

    # Sleep
    sleep = float(data.get('sleep', 0))
    if sleep < 7:
        parts.append("Sleep 7–9 hours: set a fixed bedtime, limit screens 1 hour before bed, and keep a dark, cool room.")
    elif sleep > 9:
        parts.append("Keep sleep within 7–9 hours; if you feel excessive fatigue, consider a checkup.")

    # Water
    water = float(data.get('water', 0))
    if water < 2:
        parts.append("Increase water toward 2–3 liters/day; sip regularly and front-load earlier in the day.")
    elif water > 4:
        parts.append("Avoid excessive water intake; spread intake across the day.")

    # Exercise
    exercise = float(data.get('exercise', 0))
    if exercise < 30:
        parts.append("Target ≥30 minutes moderate activity daily; add 2 strength sessions/week (full body).")
    elif exercise < 150:
        parts.append("Progress to 150–300 minutes/week moderate cardio plus 2–3 strength sessions.")
    else:
        parts.append("Great consistency—include 1 recovery day/week and mobility work 2–3×/week.")

    # Classification nudge
    if classification == "At Risk":
        parts.append("Schedule a primary care checkup for baseline labs (lipids, A1c, thyroid) and blood pressure.")

    return "\n".join(parts)