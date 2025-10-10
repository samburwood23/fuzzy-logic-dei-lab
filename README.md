# Women's Workplace Stress & DEI Analysis System

A fuzzy logic-based machine learning system for analyzing workplace stress and diversity, equity, and inclusion (DEI) impacts on women in technology. Based on the Mental Health in Tech Survey (2014), this system provides personalized mental health assessments and actionable recommendations.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎯 Overview

This project implements a comprehensive fuzzy logic system that evaluates multiple workplace factors to assess:
- **Overall stress levels** in women working in tech
- **Burnout risk** based on work conditions
- **Intervention priority** for mental health support
- **DEI health metrics** and organizational support quality

The system uses 6 input variables and 3 output metrics, with 20+ fuzzy rules to provide nuanced, personalized assessments.

## ✨ Key Features

- **Real-time Analysis**: Interactive web interface for immediate stress assessment
- **Multi-Factor Evaluation**: Considers work hours, DEI support, remote flexibility, mental health benefits, manager support, and discrimination experiences
- **Personalized Recommendations**: Generates targeted action items based on individual circumstances
- **DEI-Focused**: Specifically addresses challenges faced by women in technology workplaces
- **Visual Dashboard**: Clean, modern UI with progress bars and color-coded risk indicators
- **REST API**: Flask backend for integration with other systems

## 📊 Based on Real Data

This system is informed by the **Mental Health in Tech Survey (2014)**, focusing on:
- Gender discrimination and bias in tech workplaces
- DEI initiatives effectiveness
- Work-life balance for women in tech
- Mental health support accessibility
- Management support quality

## 🏗️ System Architecture

### Input Variables (0-10 scale, except work hours)
1. **Work Hours per Week** (20-80 hours)
2. **Company DEI Support Level** (quality of diversity initiatives)
3. **Remote Work Flexibility** (work-from-home options)
4. **Mental Health Benefits** (coverage quality)
5. **Manager Support Quality** (understanding and support)
6. **Gender Discrimination Experience** (severity of experienced discrimination)

### Output Metrics (0-100 scale)
1. **Stress Level** - Low / Moderate / High
2. **Burnout Risk** - Low / Moderate / High  
3. **Intervention Priority** - Low / Medium / Urgent

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/samburwood23/ML_TEST_REPO.git
cd ML_TEST_REPO
```

2. Install required Python packages:
```bash
pip install flask flask-cors numpy scikit-fuzzy pandas
```

### Running the Application

1. Start the Flask backend server:
```bash
cd src/code
python backend.py
```

The server will start on `http://localhost:5000`

2. Open the frontend in your browser:
```bash
# Simply open frontend.html in your browser
# Or use a local server:
python -m http.server 8000
# Then navigate to http://localhost:8000/frontend.html
```

3. The web interface will automatically check the backend connection status

## 💻 Usage

### Web Interface

1. Adjust the sliders for each workplace factor:
   - **Work Hours**: Your typical weekly work hours
   - **DEI Support**: Quality of company diversity initiatives (0=none, 10=excellent)
   - **Remote Flexibility**: Work-from-home options (0=none, 10=full remote)
   - **Mental Health Benefits**: Quality of mental health coverage (0=inadequate, 10=comprehensive)
   - **Manager Support**: Manager understanding and support (0=unsupportive, 10=very supportive)
   - **Discrimination Experience**: Gender discrimination severity (0=minimal, 10=severe)

2. Click "Analyze Workplace Stress & DEI Impact"

3. Review your results:
   - **Stress metrics** with color-coded risk levels
   - **DEI health indicators**
   - **Workplace environment assessment**
   - **Personalized recommendations** with priority levels

### API Usage

**Health Check:**
```bash
curl http://localhost:5000/health
```

**Analyze Stress:**
```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "work_hours": 50,
    "dei_support": 6,
    "remote_flexibility": 7,
    "mental_health_benefits": 5,
    "manager_support": 8,
    "discrimination_exp": 3
  }'
```

**Response Format:**
```json
{
  "analysis": {
    "stress_level": {"score": 45.2, "risk": "Moderate"},
    "burnout_risk": {"score": 38.7, "level": "Moderate"},
    "intervention_priority": {"score": 42.1, "urgency": "Medium Priority"}
  },
  "dei_metrics": {
    "overall_dei_health": 72.5,
    "discrimination_impact": "Minimal",
    "support_adequacy": "Adequate"
  },
  "recommendations": [...]
}
```

## 🧠 Fuzzy Logic System

The system implements **20+ fuzzy rules** covering scenarios such as:

- **Ideal conditions**: Standard hours + excellent DEI + supportive management = Low stress
- **Discrimination impact**: Severe discrimination → High stress/urgent intervention
- **Overwork conditions**: Excessive hours + poor DEI → High burnout risk
- **Poor organizational support**: Multiple support gaps → Urgent intervention
- **Protective factors**: Remote flexibility + manager support → Reduced stress
- **Mixed conditions**: Nuanced assessments for complex situations

### Membership Functions

Each input and output variable uses triangular membership functions (trimf) to represent fuzzy categories, allowing the system to handle uncertainty and partial truth values.

## 📁 Project Structure

```
ML_TEST_REPO/
├── src/
│   └── code/
│       ├── backend.py          # Flask API with fuzzy logic system
│       └── frontend.html        # Interactive web interface
├── README.md                    # This file
└── requirements.txt            # Python dependencies
```

## 🔧 Dependencies

- **Flask** - Web framework for REST API
- **Flask-CORS** - Cross-origin resource sharing
- **NumPy** - Numerical computing
- **scikit-fuzzy** - Fuzzy logic implementation
- **Pandas** - Data manipulation (for future dataset analysis)

Install all dependencies:
```bash
pip install -r requirements.txt
```

## 🎨 Features Deep Dive

### Visual Design
- Modern gradient backgrounds with purple theme
- Responsive design for mobile and desktop
- Real-time connection status indicator
- Animated progress bars with color-coded risk levels
- Smooth transitions and hover effects

### Smart Recommendations
The system generates context-aware recommendations with priority levels:
- **Critical**: Immediate discrimination or high burnout situations
- **High**: Work-life balance issues, poor management support
- **Medium**: DEI improvement opportunities
- **Low**: Maintenance of healthy practices

### DEI Health Metrics
Calculates overall organizational DEI health considering:
- Company DEI initiatives (30% weight)
- Discrimination experiences (30% weight)
- Manager support (20% weight)
- Mental health benefits (10% weight)
- Remote flexibility (10% weight)

## 🔬 Use Cases

- **Individual Assessment**: Women in tech can evaluate their workplace stress
- **Organizational Analysis**: HR teams can identify systemic issues
- **Research**: Study patterns in workplace stress and DEI effectiveness
- **Policy Development**: Data-driven insights for workplace improvements
- **Intervention Planning**: Prioritize mental health support resources

## 🛣️ Future Enhancements

- [ ] Data visualization dashboard for trends over time
- [ ] Integration with actual Mental Health in Tech Survey dataset
- [ ] Machine learning model comparison (vs traditional ML approaches)
- [ ] Multi-user anonymous data aggregation
- [ ] Export reports as PDF
- [ ] Additional input variables (company size, industry sector, etc.)
- [ ] Mobile app version

## 📚 Technical Details

**Fuzzy Logic Engine**: scikit-fuzzy (skfuzzy)
- Uses Mamdani-style inference
- Centroid defuzzification method
- Triangular membership functions for all variables

**Backend**: Flask REST API
- CORS-enabled for local development
- JSON request/response format
- Comprehensive input validation
- Detailed error handling

**Frontend**: Vanilla JavaScript
- No frameworks required
- Real-time connection monitoring
- Responsive slider controls
- Dynamic result rendering

## 🤝 Contributing

Contributions are welcome! This project could benefit from:
- Additional fuzzy rules based on research
- Integration with real survey data
- Improved visualization options
- Accessibility enhancements
- Internationalization

## 📖 References

- Mental Health in Tech Survey (2014)
- Fuzzy Logic principles and implementation
- DEI best practices in technology workplaces
- Workplace stress and burnout research

## 📧 Contact

For questions, suggestions, or collaboration opportunities, please open an issue on GitHub.



## 🙏 Acknowledgments

- Mental Health in Tech Survey contributors
- scikit-fuzzy development team
- Women in tech communities advocating for workplace equality

---

**Note**: This system provides assessment and recommendations but is not a substitute for professional mental health care. If you're experiencing severe stress or mental health concerns, please consult with a qualified healthcare provider.
