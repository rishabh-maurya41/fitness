from flask import Flask, render_template, request
from health_logic import calculate_bmi, health_score_and_classification, generate_personal_suggestion
from ml_model import get_model

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("form.html")

@app.route("/input", methods=["GET", "POST"])
def input_form():
    result = None
    if request.method == "POST":
        data = {
            "age": int(request.form["age"]),
            "gender": request.form["gender"],
            "height": float(request.form["height"]),
            "weight": float(request.form["weight"]),
            "sleep": float(request.form["sleep"]),
            "water": float(request.form["water"]),
            "exercise": int(request.form["exercise"]),
        }
        bmi = calculate_bmi(data["height"], data["weight"])
        data["bmi"] = bmi
        score, classification, detail = health_score_and_classification(data, bmi)
        # Use the trained model to suggest based on dataset
        model = get_model()
        suggestion = model.predict_suggestion(data)
        personal = generate_personal_suggestion(data, bmi, classification)
        result = {
            "score": score,
            "bmi": bmi,
            "classification": classification,
            "detail": detail,
            "gemini": suggestion,
            "personal": personal
        }
    return render_template("form.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
