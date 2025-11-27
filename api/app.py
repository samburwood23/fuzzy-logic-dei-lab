from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
app = Flask(__name__, 
            static_folder='../public',
            template_folder='../public')
CORS(app)
# Add this route at the top:
@app.route('/')
def home():
    return send_from_directory('../public', 'index.html')

# Define fuzzy variables
work_hours = ctrl.Antecedent(np.arange(20, 81, 1), 'work_hours')
dei_support = ctrl.Antecedent(np.arange(0, 11, 1), 'dei_support')
remote_flexibility = ctrl.Antecedent(np.arange(0, 11, 1), 'remote_flexibility')
mental_health_benefits = ctrl.Antecedent(np.arange(0, 11, 1), 'mental_health_benefits')
manager_support = ctrl.Antecedent(np.arange(0, 11, 1), 'manager_support')
discrimination_exp = ctrl.Antecedent(np.arange(0, 11, 1), 'discrimination_exp')

stress_level = ctrl.Consequent(np.arange(0, 11, 1), 'stress_level')
burnout_risk = ctrl.Consequent(np.arange(0, 11, 1), 'burnout_risk')
intervention_priority = ctrl.Consequent(np.arange(0, 11, 1), 'intervention_priority')

# Define membership functions
work_hours['low'] = fuzz.trimf(work_hours.universe, [20, 20, 40])
work_hours['moderate'] = fuzz.trimf(work_hours.universe, [30, 45, 60])
work_hours['high'] = fuzz.trimf(work_hours.universe, [50, 80, 80])

dei_support['poor'] = fuzz.trimf(dei_support.universe, [0, 0, 5])
dei_support['moderate'] = fuzz.trimf(dei_support.universe, [3, 5, 7])
dei_support['excellent'] = fuzz.trimf(dei_support.universe, [6, 10, 10])

remote_flexibility['low'] = fuzz.trimf(remote_flexibility.universe, [0, 0, 5])
remote_flexibility['moderate'] = fuzz.trimf(remote_flexibility.universe, [3, 5, 7])
remote_flexibility['high'] = fuzz.trimf(remote_flexibility.universe, [6, 10, 10])

mental_health_benefits['poor'] = fuzz.trimf(mental_health_benefits.universe, [0, 0, 5])
mental_health_benefits['moderate'] = fuzz.trimf(mental_health_benefits.universe, [3, 5, 7])
mental_health_benefits['excellent'] = fuzz.trimf(mental_health_benefits.universe, [6, 10, 10])

manager_support['poor'] = fuzz.trimf(manager_support.universe, [0, 0, 5])
manager_support['moderate'] = fuzz.trimf(manager_support.universe, [3, 5, 7])
manager_support['excellent'] = fuzz.trimf(manager_support.universe, [6, 10, 10])

discrimination_exp['none'] = fuzz.trimf(discrimination_exp.universe, [0, 0, 3])
discrimination_exp['some'] = fuzz.trimf(discrimination_exp.universe, [2, 5, 8])
discrimination_exp['severe'] = fuzz.trimf(discrimination_exp.universe, [7, 10, 10])

stress_level['low'] = fuzz.trimf(stress_level.universe, [0, 0, 4])
stress_level['moderate'] = fuzz.trimf(stress_level.universe, [3, 5, 7])
stress_level['high'] = fuzz.trimf(stress_level.universe, [6, 10, 10])

burnout_risk['low'] = fuzz.trimf(burnout_risk.universe, [0, 0, 4])
burnout_risk['moderate'] = fuzz.trimf(burnout_risk.universe, [3, 5, 7])
burnout_risk['high'] = fuzz.trimf(burnout_risk.universe, [6, 10, 10])

intervention_priority['low'] = fuzz.trimf(intervention_priority.universe, [0, 0, 4])
intervention_priority['medium'] = fuzz.trimf(intervention_priority.universe, [3, 5, 7])
intervention_priority['urgent'] = fuzz.trimf(intervention_priority.universe, [6, 10, 10])

# Define fuzzy rules (add all your rules from backend.py)
rule1 = ctrl.Rule(work_hours['high'] & dei_support['poor'], 
                  (stress_level['high'], burnout_risk['high'], intervention_priority['urgent']))
rule2 = ctrl.Rule(dei_support['excellent'] & manager_support['excellent'], 
                  (stress_level['low'], burnout_risk['low'], intervention_priority['low']))
rule3 = ctrl.Rule(discrimination_exp['severe'], 
                  (stress_level['high'], intervention_priority['urgent']))
rule4 = ctrl.Rule(work_hours['high'] & remote_flexibility['low'], 
                  (stress_level['high'], burnout_risk['moderate']))
rule5 = ctrl.Rule(mental_health_benefits['poor'] & discrimination_exp['some'], 
                  intervention_priority['medium'])
rule6 = ctrl.Rule(work_hours['moderate'] & dei_support['moderate'], 
                  (stress_level['moderate'], burnout_risk['moderate']))
rule7 = ctrl.Rule(remote_flexibility['high'] & mental_health_benefits['excellent'], 
                  stress_level['low'])
rule8 = ctrl.Rule(manager_support['poor'] & work_hours['high'], 
                  burnout_risk['high'])
rule9 = ctrl.Rule(dei_support['poor'] & discrimination_exp['severe'], 
                  (stress_level['high'], intervention_priority['urgent']))
rule10 = ctrl.Rule(mental_health_benefits['excellent'] & manager_support['excellent'] & 
                   dei_support['excellent'], stress_level['low'])

# Create control system
stress_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, 
                                   rule6, rule7, rule8, rule9, rule10])
stress_sim = ctrl.ControlSystemSimulation(stress_ctrl)

def get_recommendation(stress, burnout, priority):
    """Generate personalized recommendations based on results"""
    recommendations = []
    
    if priority > 7:
        recommendations.append("🚨 Critical: Immediate professional support recommended")
        recommendations.append("Contact your HR department or EAP program immediately")
    elif priority > 5:
        recommendations.append("⚠️ Medium Priority: Schedule time with manager or HR")
        recommendations.append("Consider requesting workload adjustment")
    else:
        recommendations.append("✅ Low Priority: Continue current coping strategies")
        recommendations.append("Maintain regular check-ins with manager")
    
    if stress > 7:
        recommendations.append("High stress detected - prioritize self-care activities")
    
    if burnout > 7:
        recommendations.append("Burnout risk is high - consider taking time off if possible")
    
    if dei_support < 4:
        recommendations.append("Advocate for improved DEI initiatives in your workplace")
    
    return recommendations

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Backend is running"})

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        
        # Input validation
        required_fields = ['work_hours', 'dei_support', 'remote_flexibility', 
                          'mental_health_benefits', 'manager_support', 'discrimination_exp']
        
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Set inputs
        stress_sim.input['work_hours'] = data['work_hours']
        stress_sim.input['dei_support'] = data['dei_support']
        stress_sim.input['remote_flexibility'] = data['remote_flexibility']
        stress_sim.input['mental_health_benefits'] = data['mental_health_benefits']
        stress_sim.input['manager_support'] = data['manager_support']
        stress_sim.input['discrimination_exp'] = data['discrimination_exp']
        
        # Compute results
        stress_sim.compute()
        
        stress = stress_sim.output['stress_level']
        burnout = stress_sim.output['burnout_risk']
        priority = stress_sim.output['intervention_priority']
        
        recommendations = get_recommendation(stress, burnout, priority)
        
        return jsonify({
            "stress_level": round(stress, 2),
            "burnout_risk": round(burnout, 2),
            "intervention_priority": round(priority, 2),
            "recommendations": recommendations
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# This is required for Vercel
if __name__ == '__main__':
    app.run()
        
