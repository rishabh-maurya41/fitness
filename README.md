# Health Score & Personalized Health Suggestion System

## Features
- Input user health data
- Get a Health Score (0–100)
- Classification: Healthy / Needs Improvement / At Risk
- Personalized recommendations powered by Gemini LLM (Google AI)
- Dataset-backed score logic
- Responsive, modern UI

## Running Locally

```bash
pip install -r requirements.txt
python app.py
# Visit http://localhost:5000 in your browser
```

## Configure Gemini API Key

Replace the key in `gemini_api.py` with your own for production.

## Datasets

Use the following (see documentation for refinement):
- https://www.kaggle.com/datasets/andradaolteanu/lifestyle-and-wellbeing-data
- https://www.kaggle.com/datasets/laxmihemanth/healthy-vs-unhealthy-habits

## Security
Never expose the Gemini API key publicly in production environments.
