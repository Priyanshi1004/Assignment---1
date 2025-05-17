# Assignment---1
Web-app

Bonus task 1- app.py


Bonus task 3- risk_analyzer.py


Bonus task 4- Dockerfile.dockerfile


## ***Setup Instructions***

1. Clone the repository:
```   
   git clone https://github.com/Priyanshi1004/Assignment---1.git
   cd Assignment---1
```
2. Create and activate a virtual environment:
```   
   python -m venv venv# On Windows
```
3. Install required Python packages:
```
   pip install -r requirements.txt
```
4. Run the Streamlit Web Application:
  ```   
   streamlit run main.py
  ``` 
5. Open your browser at http://localhost:8501 to access the UI.

6. Run the REST API Server:
  ```   
  python app.py
  ```
The API will be accessible at http://localhost:5000.

## ***Usage Guide:*** 
Streamlit UI: Use the interface to register policyholders, file claims, perform risk analysis, and view reports
1. Health Check: 
Check if the API is running:
GET /health
  ```
  curl http://localhost:5000/health
  ```
Response:
{
  "status": "ok",
  "message": "API is up and running"
}

2. Analyze Risk:
POST /api/analyze
  ```
  curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "risk_factors": {
      "technical_complexity": 7,
      "resource_availability": 5,
      "timeline_constraints": 6,
      "budget_constraints": 4,
      "stakeholder_involvement": 3,
      "regulatory_compliance": 6
    }
  }'
  ```

3. Full Risk Assessment: 
POST /api/risks
  ```
  curl -X POST http://localhost:5000/api/risks \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Insurance App Revamp",
    "risk_factors": {
      "technical_complexity": 8,
      "resource_availability": 6,
      "timeline_constraints": 5,
      "budget_constraints": 3,
      "stakeholder_involvement": 4,
      "regulatory_compliance": 7
    }
  }'
  ```

4. List All Risk Assessments
GET /api/risks
  ```
  curl http://localhost:5000/api/risks
  ```
6. Get Risk Assessment by ID
GET /api/risks/<id>
Example:
  ```
  curl http://localhost:5000/api/risks/1
  ```

8. Update Risk Assessment
PUT /api/risks/<id>
  ```
  curl -X PUT http://localhost:5000/api/risks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Updated Project Name",
    "risk_factors": {
      "technical_complexity": 9
    }
  }'
  ```

9. Delete Risk Assessment
DELETE /api/risks/<id>
  ```
  curl -X DELETE http://localhost:5000/api/risks/1
  ```
## ***API Documentation***

You can explore and test the API using the Postman collection published here:

🔗 [ABC Insurance API Documentation on Postman](https://documenter.getpostman.com/view/45034017/2sB2qWHPj9)
