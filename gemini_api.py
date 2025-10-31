from google import genai
import os

# Store your key securely (recommended use: export GEMINI_API_KEY=xxxx)
API_KEY = "AIzaSyAuPGUxjWz378gQAL-fbmATpcRWPQjfRCE"

client = genai.Client(api_key=API_KEY)

def get_gemini_recommendation(age, gender, bmi, sleep, water, exercise):
    prompt = (
        f"Given:\n"
        f"- Age: {age}\n"
        f"- Gender: {gender}\n"
        f"- BMI: {bmi}\n"
        f"- Sleep: {sleep} hours/day\n"
        f"- Water Intake: {water} liters/day\n"
        f"- Exercise: {exercise} minutes/day\n\n"
        "Provide:\n"
        "1) Current Health Condition Summary\n"
        "2) Potential Risks\n"
        "3) Simple & practical daily improvements.\n"
    )

    result = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return result.text  # Clean text response


# Test
# print(get_gemini_recommendation(25, "Male", 24.3, 6, 1.5, 20))
