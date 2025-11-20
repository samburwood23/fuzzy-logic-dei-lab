# women_dei_stress_fuzzy.py
from flask import Flask, request, jsonify
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd

app = Flask(__name__)
CORS(app)
@app.route("/ui")
def ui_home():
    return render_template("index.html")

@app.route("/frontend")
def ui_frontend():
    return render_template("frontend.html")
    
def create_women_dei_stress_fuzzy_system():
    """
    Fuzzy Logic System for Women's Workplace Stress & DEI Analysis
    Based on Mental Health in Tech Survey
    
    Key Inputs:
    1. Work Hours per Week (20-80 hours)
    2. Company DEI Support Level (0-10 scale)
    3. Remote Work Flexibility (0-10 scale)
    4. Mental Health Benefits Access (0-10 scale)
    5. Manager Support Quality (0-10 scale)
    6. Gender Discrimination Experience (0-10 scale)
    
    Outputs:
    1. Overall Stress Level (0-100)
    2. Burnout Risk (0-100)
    3. Intervention Priority (0-100)
    """
    
    # Define input variables (antecedents)
    work_hours = ctrl.Antecedent(np.arange(20, 81, 1), 'work_hours')
    dei_support = ctrl.Antecedent(np.arange(0, 11, 1), 'dei_support')
    remote_flexibility = ctrl.Antecedent(np.arange(0, 11, 1), 'remote_flexibility')
    mental_health_benefits = ctrl.Antecedent(np.arange(0, 11, 1), 'mental_health_benefits')
    manager_support = ctrl.Antecedent(np.arange(0, 11, 1), 'manager_support')
    discrimination_exp = ctrl.Antecedent(np.arange(0, 11, 1), 'discrimination_exp')
    
    # Define output variables (consequents)
    stress_level = ctrl.Consequent(np.arange(0, 101, 1), 'stress_level')
    burnout_risk = ctrl.Consequent(np.arange(0, 101, 1), 'burnout_risk')
    intervention_priority = ctrl.Consequent(np.arange(0, 101, 1), 'intervention_priority')
    
    # Membership functions for Work Hours
    work_hours['standard'] = fuzz.trimf(work_hours.universe, [20, 35, 45])
    work_hours['extended'] = fuzz.trimf(work_hours.universe, [40, 50, 60])
    work_hours['excessive'] = fuzz.trimf(work_hours.universe, [55, 70, 80])
    
    # Membership functions for DEI Support
    dei_support['poor'] = fuzz.trimf(dei_support.universe, [0, 0, 4])
    dei_support['moderate'] = fuzz.trimf(dei_support.universe, [3, 5, 7])
    dei_support['excellent'] = fuzz.trimf(dei_support.universe, [6, 10, 10])
    
    # Membership functions for Remote Flexibility
    remote_flexibility['none'] = fuzz.trimf(remote_flexibility.universe, [0, 0, 3])
    remote_flexibility['partial'] = fuzz.trimf(remote_flexibility.universe, [2, 5, 8])
    remote_flexibility['full'] = fuzz.trimf(remote_flexibility.universe, [7, 10, 10])
    
    # Membership functions for Mental Health Benefits
    mental_health_benefits['inadequate'] = fuzz.trimf(mental_health_benefits.universe, [0, 0, 4])
    mental_health_benefits['adequate'] = fuzz.trimf(mental_health_benefits.universe, [3, 5, 7])
    mental_health_benefits['comprehensive'] = fuzz.trimf(mental_health_benefits.universe, [6, 10, 10])
    
    # Membership functions for Manager Support
    manager_support['unsupportive'] = fuzz.trimf(manager_support.universe, [0, 0, 4])
    manager_support['neutral'] = fuzz.trimf(manager_support.universe, [3, 5, 7])
    manager_support['supportive'] = fuzz.trimf(manager_support.universe, [6, 10, 10])
    
    # Membership functions for Discrimination Experience
    discrimination_exp['minimal'] = fuzz.trimf(discrimination_exp.universe, [0, 0, 3])
    discrimination_exp['moderate'] = fuzz.trimf(discrimination_exp.universe, [2, 5, 8])
    discrimination_exp['severe'] = fuzz.trimf(discrimination_exp.universe, [7, 10, 10])
    
    # Membership functions for Stress Level Output
    stress_level['low'] = fuzz.trimf(stress_level.universe, [0, 0, 35])
    stress_level['moderate'] = fuzz.trimf(stress_level.universe, [25, 50, 75])
    stress_level['high'] = fuzz.trimf(stress_level.universe, [65, 100, 100])
    
    # Membership functions for Burnout Risk Output
    burnout_risk['low'] = fuzz.trimf(burnout_risk.universe, [0, 0, 35])
    burnout_risk['moderate'] = fuzz.trimf(burnout_risk.universe, [25, 50, 75])
    burnout_risk['high'] = fuzz.trimf(burnout_risk.universe, [65, 100, 100])
    
    # Membership functions for Intervention Priority Output
    intervention_priority['low'] = fuzz.trimf(intervention_priority.universe, [0, 0, 35])
    intervention_priority['medium'] = fuzz.trimf(intervention_priority.universe, [25, 50, 75])
    intervention_priority['urgent'] = fuzz.trimf(intervention_priority.universe, [65, 100, 100])
    
    # Define comprehensive fuzzy rules
    rules = []
    
    # RULE SET 1: Ideal Conditions (Low Stress)
    rules.append(ctrl.Rule(
        work_hours['standard'] & dei_support['excellent'] & 
        manager_support['supportive'] & discrimination_exp['minimal'],
        (stress_level['low'], burnout_risk['low'], intervention_priority['low'])
    ))
    
    # RULE SET 2: Discrimination Impact (High Stress regardless of other factors)
    rules.append(ctrl.Rule(
        discrimination_exp['severe'],
        (stress_level['high'], burnout_risk['high'], intervention_priority['urgent'])
    ))
    
    rules.append(ctrl.Rule(
        discrimination_exp['moderate'] & manager_support['unsupportive'],
        (stress_level['high'], burnout_risk['moderate'], intervention_priority['urgent'])
    ))
    
    # RULE SET 3: Overwork Conditions
    rules.append(ctrl.Rule(
        work_hours['excessive'] & dei_support['poor'],
        (stress_level['high'], burnout_risk['high'], intervention_priority['urgent'])
    ))
    
    rules.append(ctrl.Rule(
        work_hours['excessive'] & remote_flexibility['none'],
        (stress_level['high'], burnout_risk['moderate'], intervention_priority['medium'])
    ))
    
    rules.append(ctrl.Rule(
        work_hours['extended'] & mental_health_benefits['inadequate'],
        (stress_level['moderate'], burnout_risk['moderate'], intervention_priority['medium'])
    ))
    
    # RULE SET 4: Poor Organizational Support
    rules.append(ctrl.Rule(
        dei_support['poor'] & mental_health_benefits['inadequate'] & 
        manager_support['unsupportive'],
        (stress_level['high'], burnout_risk['high'], intervention_priority['urgent'])
    ))
    
    rules.append(ctrl.Rule(
        manager_support['unsupportive'] & discrimination_exp['moderate'],
        (stress_level['high'], burnout_risk['moderate'], intervention_priority['urgent'])
    ))
    
    # RULE SET 5: Protective Factors
    rules.append(ctrl.Rule(
        remote_flexibility['full'] & manager_support['supportive'] & 
        work_hours['standard'],
        (stress_level['low'], burnout_risk['low'], intervention_priority['low'])
    ))
    
    rules.append(ctrl.Rule(
        mental_health_benefits['comprehensive'] & dei_support['excellent'],
        (stress_level['low'], burnout_risk['low'], intervention_priority['low'])
    ))
    
    # RULE SET 6: Mixed Conditions
    rules.append(ctrl.Rule(
        work_hours['extended'] & dei_support['moderate'] & 
        manager_support['neutral'],
        (stress_level['moderate'], burnout_risk['moderate'], intervention_priority['medium'])
    ))
    
    rules.append(ctrl.Rule(
        discrimination_exp['minimal'] & work_hours['standard'] & 
        dei_support['moderate'],
        (stress_level['low'], burnout_risk['low'], intervention_priority['low'])
    ))
    
    # RULE SET 7: Work-Life Balance Impact
    rules.append(ctrl.Rule(
        work_hours['excessive'] & remote_flexibility['full'] & 
        manager_support['supportive'],
        (stress_level['moderate'], burnout_risk['moderate'], intervention_priority['medium'])
    ))
    
    rules.append(ctrl.Rule(
        work_hours['standard'] & remote_flexibility['none'] & 
        discrimination_exp['moderate'],
        (stress_level['moderate'], burnout_risk['moderate'], intervention_priority['medium'])
    ))
    
    # RULE SET 8: Critical Support Gaps
    rules.append(ctrl.Rule(
        mental_health_benefits['inadequate'] & discrimination_exp['moderate'] & 
        manager_support['unsupportive'],
        (stress_level['high'], burnout_risk['high'], intervention_priority['urgent'])
    ))
    
    rules.append(ctrl.Rule(
        dei_support['poor'] & work_hours['excessive'] & 
        remote_flexibility['none'],
        (stress_level['high'], burnout_risk['high'], intervention_priority['urgent'])
    ))
    
    # RULE SET 9: Moderate Risk Scenarios
    rules.append(ctrl.Rule(
        work_hours['extended'] & dei_support['moderate'] & 
        remote_flexibility['partial'],
        (stress_level['moderate'], burnout_risk['moderate'], intervention_priority['medium'])
    ))
    
    rules.append(ctrl.Rule(
        manager_support['neutral'] & mental_health_benefits['adequate'] & 
        discrimination_exp['minimal'],
        (stress_level['moderate'], burnout_risk['low'], intervention_priority['low'])
    ))
    
    # RULE SET 10: Additional nuanced rules
    rules.append(ctrl.Rule(
        work_hours['standard'] & dei_support['poor'] & 
        discrimination_exp['moderate'],
        (stress_level['moderate'], burnout_risk['moderate'], intervention_priority['medium'])
    ))
    
    rules.append(ctrl.Rule(
        remote_flexibility['partial'] & manager_support['supportive'] & 
        work_hours['extended'],
        (stress_level['moderate'], burnout_risk['low'], intervention_priority['low'])
    ))
    
    # Create control system
    stress_ctrl = ctrl.ControlSystem(rules)
    return ctrl.ControlSystemSimulation(stress_ctrl)

# Create the fuzzy system once at startup
fuzzy_system = create_women_dei_stress_fuzzy_system()

@app.route('/')
def home():
    return jsonify({
        'message': 'Women\'s Workplace Stress & DEI Analysis API',
        'description': 'Fuzzy Logic System for Mental Health in Tech Survey',
        'dataset': 'Mental Health in Tech Survey (2014)',
        'focus': 'Women in technology workplaces',
        'inputs': {
            'work_hours': '20-80 hours per week',
            'dei_support': '0-10 (company DEI initiatives quality)',
            'remote_flexibility': '0-10 (work from home options)',
            'mental_health_benefits': '0-10 (mental health coverage quality)',
            'manager_support': '0-10 (manager understanding & support)',
            'discrimination_exp': '0-10 (experienced gender discrimination)'
        },
        'outputs': {
            'stress_level': '0-100 (overall stress)',
            'burnout_risk': '0-100 (burnout probability)',
            'intervention_priority': '0-100 (urgency of intervention)'
        }
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'system': 'Women DEI Stress Analysis'})

@app.route('/analyze', methods=['POST'])
def analyze_stress():
    try:
        data = request.json
        
        # Validate input
        required_fields = ['work_hours', 'dei_support', 'remote_flexibility', 
                          'mental_health_benefits', 'manager_support', 'discrimination_exp']
        
        if not data or not all(field in data for field in required_fields):
            return jsonify({
                'error': f'Missing required fields: {", ".join(required_fields)}'
            }), 400
        
        # Extract and validate inputs
        work_hours = float(data['work_hours'])
        dei_support = float(data['dei_support'])
        remote_flexibility = float(data['remote_flexibility'])
        mental_health_benefits = float(data['mental_health_benefits'])
        manager_support = float(data['manager_support'])
        discrimination_exp = float(data['discrimination_exp'])
        
        # Validate ranges
        if not (20 <= work_hours <= 80):
            return jsonify({'error': 'Work hours must be between 20 and 80'}), 400
        if not (0 <= dei_support <= 10):
            return jsonify({'error': 'DEI support must be between 0 and 10'}), 400
        if not (0 <= remote_flexibility <= 10):
            return jsonify({'error': 'Remote flexibility must be between 0 and 10'}), 400
        if not (0 <= mental_health_benefits <= 10):
            return jsonify({'error': 'Mental health benefits must be between 0 and 10'}), 400
        if not (0 <= manager_support <= 10):
            return jsonify({'error': 'Manager support must be between 0 and 10'}), 400
        if not (0 <= discrimination_exp <= 10):
            return jsonify({'error': 'Discrimination experience must be between 0 and 10'}), 400
        
        # Set inputs
        fuzzy_system.input['work_hours'] = work_hours
        fuzzy_system.input['dei_support'] = dei_support
        fuzzy_system.input['remote_flexibility'] = remote_flexibility
        fuzzy_system.input['mental_health_benefits'] = mental_health_benefits
        fuzzy_system.input['manager_support'] = manager_support
        fuzzy_system.input['discrimination_exp'] = discrimination_exp
        
        # Compute results
        fuzzy_system.compute()
        
        stress_score = float(fuzzy_system.output['stress_level'])
        burnout_score = float(fuzzy_system.output['burnout_risk'])
        intervention_score = float(fuzzy_system.output['intervention_priority'])
        
        # Determine risk levels
        def get_risk_level(score):
            if score < 35:
                return 'Low'
            elif score < 65:
                return 'Moderate'
            else:
                return 'High'
        
        stress_risk = get_risk_level(stress_score)
        burnout_level = get_risk_level(burnout_score)
        intervention_urgency = 'Low Priority' if intervention_score < 35 else \
                              'Medium Priority' if intervention_score < 65 else 'Urgent'
        
        # Generate recommendations
        recommendations = generate_recommendations(
            stress_risk, burnout_level, discrimination_exp, 
            dei_support, manager_support, work_hours
        )
        
        # Calculate DEI health score
        dei_health_score = calculate_dei_health(
            dei_support, discrimination_exp, manager_support, 
            mental_health_benefits, remote_flexibility
        )
        
        return jsonify({
            'analysis': {
                'stress_level': {
                    'score': round(stress_score, 1),
                    'risk': stress_risk,
                    'description': get_stress_description(stress_risk)
                },
                'burnout_risk': {
                    'score': round(burnout_score, 1),
                    'level': burnout_level,
                    'description': get_burnout_description(burnout_level)
                },
                'intervention_priority': {
                    'score': round(intervention_score, 1),
                    'urgency': intervention_urgency,
                    'description': get_intervention_description(intervention_urgency)
                }
            },
            'dei_metrics': {
                'overall_dei_health': round(dei_health_score, 1),
                'discrimination_impact': 'Severe' if discrimination_exp >= 7 else \
                                        'Moderate' if discrimination_exp >= 4 else 'Minimal',
                'support_adequacy': 'Strong' if dei_support >= 7 else \
                                   'Adequate' if dei_support >= 4 else 'Weak'
            },
            'workplace_factors': {
                'work_hours_assessment': 'Excessive' if work_hours >= 55 else \
                                        'Extended' if work_hours >= 45 else 'Standard',
                'flexibility_rating': 'High' if remote_flexibility >= 7 else \
                                     'Moderate' if remote_flexibility >= 4 else 'Low',
                'benefits_adequacy': 'Comprehensive' if mental_health_benefits >= 7 else \
                                    'Adequate' if mental_health_benefits >= 4 else 'Inadequate'
            },
            'recommendations': recommendations,
            'inputs': {
                'work_hours': work_hours,
                'dei_support': dei_support,
                'remote_flexibility': remote_flexibility,
                'mental_health_benefits': mental_health_benefits,
                'manager_support': manager_support,
                'discrimination_exp': discrimination_exp
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_recommendations(stress_risk, burnout_level, discrimination, 
                            dei_support, manager_support, work_hours):
    """Generate personalized recommendations based on analysis"""
    recommendations = []
    
    if discrimination >= 7:
        recommendations.append({
            'category': 'Urgent: Discrimination',
            'action': 'Document incidents and report to HR/legal immediately',
            'impact': 'Critical'
        })
        recommendations.append({
            'category': 'Support',
            'action': 'Seek external support through employee assistance programs or legal counsel',
            'impact': 'High'
        })
    
    if stress_risk == 'High' or burnout_level == 'High':
        recommendations.append({
            'category': 'Immediate Wellbeing',
            'action': 'Take immediate time off if possible; consult mental health professional',
            'impact': 'Critical'
        })
    
    if work_hours >= 55:
        recommendations.append({
            'category': 'Work-Life Balance',
            'action': 'Negotiate workload reduction with manager; set firm boundaries',
            'impact': 'High'
        })
    
    if dei_support < 4:
        recommendations.append({
            'category': 'Organizational Change',
            'action': 'Advocate for formal DEI initiatives; join or create employee resource groups',
            'impact': 'Medium'
        })
    
    if manager_support < 4:
        recommendations.append({
            'category': 'Management',
            'action': 'Request 1:1 meetings to discuss support needs; escalate to skip-level if needed',
            'impact': 'High'
        })
    
    if len(recommendations) == 0:
        recommendations.append({
            'category': 'Maintenance',
            'action': 'Continue current practices; monitor stress levels regularly',
            'impact': 'Low'
        })
    
    return recommendations

def calculate_dei_health(dei_support, discrimination, manager_support, 
                        benefits, flexibility):
    """Calculate overall DEI health score"""
    # Invert discrimination (higher discrimination = lower DEI health)
    discrimination_inverted = 10 - discrimination
    
    # Weighted average
    dei_health = (dei_support * 0.3 + discrimination_inverted * 0.3 + 
                  manager_support * 0.2 + benefits * 0.1 + flexibility * 0.1) * 10
    
    return dei_health

def get_stress_description(risk):
    descriptions = {
        'Low': 'Stress levels are manageable and within healthy ranges.',
        'Moderate': 'Stress is present but manageable with appropriate interventions.',
        'High': 'Stress levels are concerning and require immediate attention.'
    }
    return descriptions[risk]

def get_burnout_description(level):
    descriptions = {
        'Low': 'Low risk of burnout; current coping strategies appear effective.',
        'Moderate': 'Warning signs of burnout present; preventive measures recommended.',
        'High': 'High burnout risk; immediate intervention strongly recommended.'
    }
    return descriptions[level]

def get_intervention_description(urgency):
    descriptions = {
        'Low Priority': 'Maintain current support systems and monitor periodically.',
        'Medium Priority': 'Implement stress reduction strategies and increase support.',
        'Urgent': 'Immediate intervention required; prioritize employee wellbeing.'
    }
    return descriptions[urgency]

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Women's Workplace Stress & DEI Analysis System")
    print("Based on Mental Health in Tech Survey")
    print("="*60)
    print("\nFocus Areas:")
    print("  • Gender discrimination and bias")
    print("  • DEI initiatives effectiveness")
    print("  • Work-life balance for women in tech")
    print("  • Mental health support accessibility")
    print("  • Management support quality")
    print("\nAPI will be available at http://localhost:5000")
    print("="*60 + "\n")
    app.run(debug=True, port=5000)
