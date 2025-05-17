from flask import Flask, request, jsonify
import os
import json
from db_manager import DBManager
from risk_analyzer import RiskAnalyzer

app = Flask(__name__)
@app.route('/')
def home():
    return "<h2>Risk Analysis API</h2><p>Visit <code>/health</code> to check API status or use Postman to test endpoints like <code>/api/analyze</code>.</p>"
db_manager = DBManager()
risk_analyzer = RiskAnalyzer()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "risk-analysis-api"})

@app.route('/api/risks', methods=['GET'])
def get_all_risks():
    try:
        risks = db_manager.get_all_risks()
        return jsonify({"status": "success", "data": risks})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/risks/<int:risk_id>', methods=['GET'])
def get_risk(risk_id):
    try:
        risk = db_manager.get_risk_by_id(risk_id)
        if risk:
            return jsonify({"status": "success", "data": risk})
        else:
            return jsonify({"status": "error", "message": "Risk not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/risks', methods=['POST'])
def create_risk():
    try:
        data = request.get_json()
        required_fields = ['project_name', 'risk_factors']
        for field in required_fields:
            if field not in data:
                return jsonify({"status": "error", "message": f"Missing required field: {field}"}), 400
        risk_score = risk_analyzer.analyze_risk(data['risk_factors'])
        data['risk_score'] = risk_score
        risk_id = db_manager.create_risk(data)        
        return jsonify({"status": "success", "message": "Risk assessment created", "risk_id": risk_id}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/risks/<int:risk_id>', methods=['PUT'])
def update_risk(risk_id):
    try:
        data = request.get_json()
        existing_risk = db_manager.get_risk_by_id(risk_id)
        if not existing_risk:
            return jsonify({"status": "error", "message": "Risk not found"}), 404
        if 'risk_factors' in data:
            risk_score = risk_analyzer.analyze_risk(data['risk_factors'])
            data['risk_score'] = risk_score
        success = db_manager.update_risk(risk_id, data)
        if success:
            return jsonify({"status": "success", "message": "Risk assessment updated"})
        else:
            return jsonify({"status": "error", "message": "Failed to update risk assessment"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/risks/<int:risk_id>', methods=['DELETE'])
def delete_risk(risk_id):
    try:
        existing_risk = db_manager.get_risk_by_id(risk_id)
        if not existing_risk:
            return jsonify({"status": "error", "message": "Risk not found"}), 404
        success = db_manager.delete_risk(risk_id)        
        if success:
            return jsonify({"status": "success", "message": "Risk assessment deleted"})
        else:
            return jsonify({"status": "error", "message": "Failed to delete risk assessment"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_risk():
    try:
        data = request.get_json()
        if 'risk_factors' not in data:
            return jsonify({"status": "error", "message": "Missing risk_factors"}), 400
        risk_score = risk_analyzer.analyze_risk(data['risk_factors'])
        return jsonify({
            "status": "success", 
            "data": {
                "risk_score": risk_score,
                "risk_level": risk_analyzer.get_risk_level(risk_score)
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('DEBUG', 'False').lower() == 'true')