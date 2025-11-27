from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd

app = Flask(__name__, template_folder="templates")
CORS(app)

# -----------------------------------------------
# LAZY-LOAD fuzzy system so Vercel won't crash
# -----------------------------------------------
fuzzy_system = None

def create_women_dei_stress_fuzzy_system():
    """Builds the fuzzy logic control system"""
    
    # Inputs
    work_hours = ctrl.Antecedent(np.arange(20, 81, 1), 'work_hours')
    dei_support = ctrl.Antecedent(np.arange(0, 11, 1), 'dei_support')
    remote_flexibility = ctrl.Antecedent(np.arange(0, 11, 1), 'remote_flexibility')
    mental_health_benefits = ctrl.Antecedent(np.arange(0, 11, 1), 'mental_health_benefits')
    manager_support = ctrl.Antecedent(np.arange(0, 11, 1), 'manager_support')
    discrimination_exp = ctrl.Antecedent(np.arange(0, 11, 1), 'discrimination_exp')
    
    # Outputs
    stress_level = ctrl.Consequent(np.arange(0, 101, 1), 'stress_level')
    burnout_risk = ctrl.Consequent(np.arange(0, 101, 1), 'burnout_risk')
    intervention_priority = ctrl.Consequent(np.arange(0, 101, 1), 'intervention_priority')

    # Membership functions
    work_hours['standard'] = fuzz.trimf(work_hours.universe, [20, 35, 45])
    work_hours['extended'] = fuzz.trimf(work_hours.universe, [40, 50, 60])
    work_hours['excessive'] = fuzz.trimf(work_hours.universe, [55, 70, 80])

    dei_support['poor'] = fuzz.trimf(dei_support.universe, [0, 0, 4])
    dei_support['moderate'] = fuzz.trimf(dei_support.universe, [3, 5, 7])
    dei_support['excellent'] = fuzz.trimf(dei_support.universe, [6, 10, 10])

    remote_flexibility['none'] = fuzz.trimf(remote_flexibility.universe, [0, 0, 3])
    remote_flexibility['partial'] = fuzz.trimf(remote_flexibility.universe, [2, 5, 8])
    remote_flexibility['full'] = fuzz.trimf(remote_flexibility.universe, [7, 10, 10])

    mental_health_benefits['inadequate'] = fuzz.trimf(mental_health_benefits.universe, [0, 0, 4])
    mental_health_benefits['adequate'] = fuzz.trimf(mental_health_benefits.universe, [3, 5, 7])
    mental_health_benefits['comprehensive'] = fuzz.trimf(mental_health_benefits.universe, [6, 10, 10])

    manager_support['unsupportive'] = fuzz.trimf(manager_support.universe, [0, 0, 4])
    manager_support['neutral'] = fuzz.trimf(manager_support.universe, [3, 5, 7])
    manager_support['supportive'] = fuzz.trimf(manager_support.universe, [6, 10, 10])

    discrimination_exp['minimal'] = fuzz.trimf(discrimination_exp.universe, [0, 0, 3])
    discrimination_exp['moderate'] = fuzz.trimf(discrimination_exp.universe, [2, 5, 8])
    discrimination_exp['severe'] = fuzz.trimf(discrimination_exp.universe, [7, 10, 10])

    stress_level['low'] = fuzz.trimf(stress_level.universe, [0, 0, 35])
    stress_level['moderate'] = fuzz.trimf(stress_level.universe, [25, 50, 75])
    stress_level['high'] = fuzz.trimf(stress_level.universe, [65, 100, 100])

    burnout_risk['low'] = fuzz.trimf(burnout_risk.universe, [0, 0, 35])
    burnout_risk['moderate'] = fuzz.trimf(burnout_risk.universe, [25, 50, 75])
    burnout_risk['high'] = fuzz.trimf(burnout_risk.universe, [65, 100, 100])

    intervention_priority['low'] = fuzz.trimf(intervention_priority.universe, [0, 0, 35])
    intervention_priority['medium'] = fuzz.trimf(intervention_priority.universe, [25, 50, 75])
    intervention_priority['urgent'] = fuzz.trimf(intervention_priority.universe, [65, 100, 100])

    # Rules (same rules as your original)
    rules = [
        ctrl.Rule(
            work_hours['standard'] & dei_support['excellent'] &
            manager_support['supportive'] & discrimination_exp['minimal'],
            (stress_level['low'], burnout_risk['low'], intervention_priority['low'])
        ),
        ctrl.Rule(
            discrimination_exp['severe'],
            (stress_level['high'], burnout_risk['high'], intervention_priority['urgent'])
        ),
        ctrl.Rule(
            discrimination_exp['moderate'] & manager_support['unsupportive'],
            (stress_level['high'], burnout_risk['moderate'], intervention_priority['urgent'])
        ),
        ctrl.Rule(
            work_hours['excessive'] & dei_support['poor'],
            (stress_level['high'], burnout_risk['high'], intervention_priority['urgent'])
        ),
    ]

    stress_ctrl = ctrl.ControlSystem(rules)
    return ctrl.ControlSystemSimulation(stress_ctrl)

# -------------------------------------------------------------
# ROUTES (API + frontend)
# -------------------------------------------------------------

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "Women DEI Fuzzy API Active"})

@app.route("/ui")
def ui_home():
    return render_template("index.html")

@app.route("/frontend")
def ui_frontend():
    return render_template("frontend.html")

@app.route("/analyze", methods=["POST"])
def analyze_stress():
    global fuzzy_system

    if fuzzy_system is None:
        fuzzy_system = create_women_dei_stress_fuzzy_system()

    data = request.json
    
    required = [
        "work_hours", "dei_support", "remote_flexibility",
        "mental_health_benefits", "manager_support", "discrimination_exp"
    ]

    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400
    
    try:
        for key in data:
            fuzzy_system.input[key] = float(data[key])

        fuzzy_system.compute()

        return jsonify({
            "stress_level": fuzzy_system.output["stress_level"],
            "burnout_risk": fuzzy_system.output["burnout_risk"],
            "intervention_priority": fuzzy_system.output["intervention_priority"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
