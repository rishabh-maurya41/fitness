# Knowledge Transfer (KT) Documentation
## Health Score & Personalized Health Suggestion System

---

## install all dependencies from requirements.txt
pip install <dependency name>

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Project Structure](#project-structure)
4. [Code Flow & Execution](#code-flow--execution)
5. [Component Details](#component-details)
6. [Data Flow](#data-flow)
7. [API Integration](#api-integration)
8. [Machine Learning Model](#machine-learning-model)
9. [Configuration & Setup](#configuration--setup)
10. [Dependencies](#dependencies)

---

## Project Overview

### Purpose
This is a Flask-based web application that provides personalized health assessment and recommendations. It combines:
- **Rule-based health scoring** (BMI, sleep, hydration, exercise)
- **Machine Learning predictions** (KNN classifier trained on health dataset)

### Key Features
- Calculate personalized health score (0-100)
- Classify health status: Healthy / Needs Improvement / At Risk
- Provide AI-generated health recommendations
- Display component-wise health scores
- Responsive web interface

---

## System Architecture

```
┌─────────────────┐
│   User Browser  │
└────────┬────────┘
         │
         │ HTTP Requests
         ▼
┌─────────────────┐
│   Flask App     │  ◄─── app.py (Main Application)
│   (app.py)      │
└────────┬────────┘
         │
         ├──────────────────┬
         │                  │               
         ▼                  ▼                  
┌──────────────┐  ┌──────────────┐  
│ health_logic │  │   ml_model   │  
│    (BMI,     │  │   (KNN)      │  
│   Scoring)   │  │              │  
└──────────────┘  └──────────────┘  
         │                  │                 
         │                  │                 
         ▼                  ▼                  
┌──────────────┐  ┌──────────────┐  
│   Rule-based │  │   Training   │  
│   Algorithms │  │   Dataset    │  
└──────────────┘  └──────────────┘  
```

---

## Project Structure

```
fitness/
│
├── app.py                          # Main Flask application (Entry point)
├── health_logic.py                 # Health scoring & classification logic
├── ml_model.py                     # Machine Learning model (KNN classifier)
├── health_training_dataset.csv     # Training data for ML model
├── requirements.txt                # Python dependencies
├── README.md                       # Basic project README
│
├── templates/                      # Jinja2 HTML templates
│   ├── home.html                  # Landing page
│   ├── form.html                  # Input form + Results display
│   └── result.html                # Alternative results page (not used)
│
└── static/                         # Static assets
    ├── style.css                  # CSS styling
    └── health-hero.jpg            # Images/assets
```

---

## Code Flow & Execution

### 1. Application Startup
```
User runs: python app.py
    │
    ├─> Flask app initializes (app = Flask(__name__))
    │
    └─> Server starts on http://localhost:5000 (debug mode)
```

### 2. User Journey Flow

#### Step 1: Landing Page (`/`)
```
User visits: http://localhost:5000/
    │
    ├─> Route: @app.route("/")
    │   └─> Function: home()
    │       └─> Renders: templates/home.html
    │
    └─> User clicks "Get Started" → Redirects to /input
```

#### Step 2: Input Form (`/input` - GET)
```
User visits: http://localhost:5000/input
    │
    ├─> Route: @app.route("/input", methods=["GET", "POST"])
    │   └─> Function: input_form()
    │       └─> Method: GET (first visit)
    │           └─> Renders: templates/form.html (empty form, no result)
```

#### Step 3: Form Submission (`/input` - POST)
```
User submits form → POST to /input
    │
    ├─> Extract form data:
    │   ├─ age, gender, height, weight
    │   ├─ sleep, water, exercise
    │
    ├─> [STEP 3.1] Calculate BMI
    │   └─> health_logic.calculate_bmi(height, weight)
    │       └─> Formula: weight / (height/100)²
    │
    ├─> [STEP 3.2] Calculate Health Score
    │   └─> health_logic.health_score_and_classification(data, bmi)
    │       ├─> Calculate component scores (BMI, Sleep, Water, Exercise)
    │       ├─> Weighted average: 0.3*BMI + 0.2*Sleep + 0.2*Water + 0.3*Exercise
    │       └─> Classify: Healthy (≥80) / Needs Improvement (≥60) / At Risk (<60)
    │
    ├─> [STEP 3.3] Get ML Model Prediction
    │   └─> ml_model.get_model()
    │       ├─> Load/initialize model (singleton pattern)
    │       ├─> Train if first call (fit_from_csv)
    │       └─> model.predict_suggestion(data)
    │           └─> KNN prediction based on similar cases in dataset
    │
    ├─> [STEP 3.4] Generate Personalized Suggestions
    │   └─> health_logic.generate_personal_suggestion(data, bmi, classification)
    │       └─> Rule-based suggestions for BMI, sleep, water, exercise
    │
    └─> Compile results and render template with results
        └─> templates/form.html (with result dictionary)
```

### 3. Detailed Component Execution

#### Component 1: BMI Calculation
```python
# health_logic.py
calculate_bmi(height_cm, weight_kg)
    │
    └─> Return: round(weight_kg / ((height_cm/100) ** 2), 1)
```

#### Component 2: Health Scoring
```python
# health_logic.py
health_score_and_classification(data, bmi)
    │
    ├─> Calculate BMI Score:
    │   ├─ 18.5 ≤ BMI ≤ 24.9 → 100
    │   ├─ 17 ≤ BMI < 18.5 OR 25 ≤ BMI ≤ 29.9 → 70
    │   └─ Otherwise → 40
    │
    ├─> Calculate Sleep Score:
    │   ├─ 7 ≤ sleep ≤ 9 hours → 100
    │   ├─ 6 ≤ sleep < 7 OR 9 < sleep ≤ 10 → 70
    │   └─ Otherwise → 40
    │
    ├─> Calculate Water Score:
    │   ├─ 2 ≤ water ≤ 3 liters → 100
    │   ├─ 1 ≤ water < 2 OR 3 < water ≤ 4 → 70
    │   └─ Otherwise → 40
    │
    ├─> Calculate Exercise Score:
    │   ├─ exercise ≥ 30 minutes → 100
    │   ├─ 15 ≤ exercise < 30 → 70
    │   └─ Otherwise → 40
    │
    ├─> Calculate Weighted Health Score:
    │   └─ 0.3*BMI + 0.2*Sleep + 0.2*Water + 0.3*Exercise
    │
    └─> Classification:
        ├─ Score ≥ 80 → "Healthy"
        ├─ Score ≥ 60 → "Needs Improvement"
        └─ Score < 60 → "At Risk"
```

#### Component 3: ML Model Prediction
```python
# ml_model.py
get_model()
    │
    ├─> Check if _model exists (singleton)
    │   ├─ If exists → Return existing model
    │   └─ If not → Initialize new model
    │
    ├─> HealthSuggestionModel()
    │   ├─ Initialize pipeline: StandardScaler + KNeighborsClassifier(n_neighbors=3)
    │   └─ Feature columns: [age, gender_num, height_cm, weight_kg, bmi, 
    │                        sleep_hours, water_liters, exercise_minutes]
    │
    ├─> model.fit_from_csv("health_training_dataset.csv")
    │   ├─ Load CSV file
    │   ├─ Convert gender to numeric (Male=0, Female=1, Other=2)
    │   ├─ Extract features (X) and target (health_suggestion)
    │   ├─ Standardize features
    │   └─ Train KNN classifier
    │
    └─> model.predict_suggestion(data)
        ├─ Convert input data to feature vector
        ├─ Scale features using StandardScaler
        ├─ Find 3 nearest neighbors
        └─ Return most common suggestion from neighbors
```

#### Component 4: Gemini API Integration


#### Component 5: Personalized Suggestions
```python
# health_logic.py
generate_personal_suggestion(data, bmi, classification)
    │
    ├─> BMI-based suggestions:
    │   ├─ BMI < 18.5 → Underweight advice
    │   ├─ 18.5 ≤ BMI ≤ 24.9 → Maintain weight advice
    │   ├─ 25 ≤ BMI ≤ 29.9 → Weight loss advice
    │   └─ BMI > 29.9 → Obesity management advice
    │
    ├─> Sleep suggestions:
    │   ├─ sleep < 7 → Improve sleep hygiene
    │   └─ sleep > 9 → Optimize sleep duration
    │
    ├─> Water suggestions:
    │   ├─ water < 2L → Increase hydration
    │   └─ water > 4L → Moderate intake
    │
    ├─> Exercise suggestions:
    │   ├─ exercise < 30 min → Increase activity
    │   ├─ 30 ≤ exercise < 150 → Progress gradually
    │   └─ exercise ≥ 150 → Add recovery days
    │
    └─> Classification-based:
        └─ If "At Risk" → Add checkup recommendation
```

---

## Data Flow

### Input Data Structure
```python
{
    "age": int,           # User's age
    "gender": str,        # "Male", "Female", or "Other"
    "height": float,      # Height in centimeters
    "weight": float,      # Weight in kilograms
    "sleep": float,       # Sleep duration in hours
    "water": float,       # Water intake in liters
    "exercise": int       # Exercise duration in minutes
}
```

### Processing Pipeline
```
1. User Input (Form Data)
   │
   ├─> Extract: age, gender, height, weight, sleep, water, exercise
   │
2. Calculate BMI
   │
   ├─> Input: height, weight
   └─> Output: bmi (float)
   │
3. Health Scoring
   │
   ├─> Input: data + bmi
   ├─> Calculate: BMI Score, Sleep Score, Water Score, Exercise Score
   ├─> Weighted Average → Health Score
   └─> Output: score, classification, detail
   │
4. ML Model Prediction
   │
   ├─> Input: data (with bmi added)
   ├─> Feature Extraction: [age, gender_num, height, weight, bmi, sleep, water, exercise]
   ├─> Scaling: StandardScaler
   ├─> Prediction: KNN (3 neighbors)
   └─> Output: suggestion (string)
   │
5. Personalized Suggestions
   │
   ├─> Input: data, bmi, classification
   ├─> Rule-based logic
   └─> Output: personalized (string)
   │
6. Result Compilation
   │
   └─> {
        "score": int,
        "bmi": float,
        "classification": str,
        "detail": dict,
        "gemini": str,      # Actually ML model prediction
        "personal": str
    }
```

### Output Data Structure
```python
{
    "score": int,                    # Overall health score (0-100)
    "bmi": float,                    # Calculated BMI
    "classification": str,           # "Healthy" / "Needs Improvement" / "At Risk"
    "detail": {                      # Component scores
        "BMI Score": int,
        "Sleep Score": int,
        "Water Score": int,
        "Exercise Score": int
    },
    "gemini": str,                   # ML model prediction (mislabeled as "gemini")
    "personal": str                  # Rule-based personalized suggestions
}
```

---

## Component Details

### 1. app.py (Main Application)

**Purpose:** Flask web application entry point

**Key Functions:**
- `home()`: Renders landing page
- `input_form()`: Handles form display (GET) and processing (POST)

**Routes:**
- `GET /`: Home page
- `GET /input`: Display input form
- `POST /input`: Process form submission and return results

**Dependencies:**
- Flask (web framework)
- health_logic (scoring logic)
- ml_model (ML predictions)

---

### 2. health_logic.py (Health Scoring Logic)

**Purpose:** Rule-based health assessment calculations

**Functions:**

#### `calculate_bmi(height_cm, weight_kg)`
- **Input:** Height (cm), Weight (kg)
- **Output:** BMI (float, rounded to 1 decimal)
- **Formula:** `weight / (height/100)²`

#### `health_score_and_classification(data, bmi)`
- **Input:** User data dict, BMI value
- **Output:** Tuple (score, classification, detail)
- **Logic:**
  - Component scoring (0-100 scale)
  - Weighted average calculation
  - Health classification

#### `generate_personal_suggestion(data, bmi, classification)`
- **Input:** User data, BMI, classification
- **Output:** Multi-line string with personalized advice
- **Logic:** Rule-based suggestions for each health metric

---

### 3. ml_model.py (Machine Learning Model)

**Purpose:** KNN-based health suggestion prediction

**Class: `HealthSuggestionModel`**

**Methods:**
- `__init__()`: Initialize model with feature columns
- `fit_from_csv(csv_path)`: Train model from CSV dataset
- `predict_suggestion(data)`: Predict health suggestion for new data

**Features Used:**
- age, gender_num, height_cm, weight_kg, bmi, sleep_hours, water_liters, exercise_minutes

**Model Pipeline:**
1. StandardScaler (feature normalization)
2. KNeighborsClassifier (n_neighbors=3)

**Singleton Pattern:**
- `get_model()`: Ensures model is loaded/trained only once


---

## Machine Learning Model

### Model Type
- **Algorithm:** K-Nearest Neighbors (KNN)
- **Neighbors:** 3 (k=3)
- **Preprocessing:** StandardScaler (feature standardization)

### Training Data
- **Source:** `health_training_dataset.csv`
- **Features:** 8 numerical features
- **Target:** `health_suggestion` (string/categorical)

### Feature Engineering
- **Gender Encoding:** Male=0, Female=1, Other=2
- **Feature Scaling:** StandardScaler (mean=0, std=1)

### Prediction Process
1. Load user input data
2. Convert gender to numeric
3. Extract feature vector
4. Standardize features
5. Find 3 nearest neighbors in training data
6. Return most common suggestion from neighbors

### Model Performance
- **Training:** On-demand (first call to `get_model()`)
- **Caching:** Singleton pattern (model loaded once)
- **Inference:** Fast (<100ms typically)

---

## Configuration & Setup

### Environment Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Required Packages:**
   - flask
   - requests
   - numpy
   - pandas
   - scikit-learn
   - google-genai (for Gemini API)

3. **Run Application:**
   ```bash
   python app.py
   ```

4. **Access Application:**
   - URL: `http://localhost:5000`
   - Debug mode: Enabled (development only)

### Configuration Files

#### requirements.txt
```
flask
requests
numpy
pandas
scikit-learn
```

**Missing:** `google-genai` (should be added if using Gemini API)

#### Environment Variables (Recommended)
```bash
export GEMINI_API_KEY="your-api-key-here"  # For production
export FLASK_ENV="production"              # For production
```

### Data Files

#### health_training_dataset.csv
- **Purpose:** Training data for ML model
- **Required Columns:**
  - age, gender, height_cm, weight_kg, bmi
  - sleep_hours, water_liters, exercise_minutes
  - health_suggestion (target variable)

---

## Dependencies

### Python Packages

| Package | Version | Purpose |
|---------|---------|---------|
| flask | Latest | Web framework |
| numpy | Latest | Numerical operations |
| pandas | Latest | Data manipulation |
| scikit-learn | Latest | ML model (KNN, StandardScaler) |
| requests | Latest | HTTP requests (if needed) |
| google-genai | Latest | Gemini API client |

### System Requirements
- **Python:** 3.7+
- **OS:** Windows, Linux, macOS
- **Memory:** Minimal (model loads dataset into memory)
- **Storage:** ~50MB (including dataset)

---

## Key Design Patterns

### 1. Singleton Pattern (ML Model)
- `get_model()` ensures model is loaded only once
- Reduces memory usage and training time

### 2. Separation of Concerns
- **app.py:** Routing and request handling
- **health_logic.py:** Business logic
- **ml_model.py:** ML operations

### 3. Template Rendering
- Jinja2 templates for HTML rendering
- Conditional rendering based on results

---

## Security Considerations

### Current Issues
1. **API Key Exposure:** Gemini API key is hardcoded
2. **Debug Mode:** Enabled in production (should be disabled)
3. **Input Validation:** Limited validation on form inputs

### Recommendations
1. Use environment variables for API keys
2. Add input validation and sanitization
3. Disable debug mode in production
4. Add rate limiting for API calls
5. Implement error handling for API failures

---

## Future Enhancements

### Potential Improvements
1. **Activate Gemini API:** Replace ML prediction with Gemini
2. **Database Integration:** Store user history
3. **User Authentication:** Multi-user support
4. **Enhanced UI:** Better styling and UX
5. **API Endpoints:** RESTful API for mobile apps
6. **Model Retraining:** Periodic model updates
7. **Analytics Dashboard:** Track health trends
8. **Export Reports:** PDF/CSV export functionality

---

## Troubleshooting

### Common Issues

1. **Model Not Loading:**
   - Check `health_training_dataset.csv` exists
   - Verify CSV has required columns

2. **Gemini API Errors:**
   - Verify API key is valid
   - Check internet connection
   - Review API quota limits

3. **Flask Server Errors:**
   - Check port 5000 is available
   - Verify all dependencies installed

4. **Import Errors:**
   - Run `pip install -r requirements.txt`
   - Check Python version compatibility

---

## Contact & Support

For questions or issues:
1. Review this documentation
2. Check code comments in source files
3. Verify configuration and dependencies

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Maintained By:** Development Team

