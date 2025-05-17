class RiskAnalyzer:
    RISK_LEVELS = {
        'low': (0, 30),
        'medium': (30, 70),
        'high': (70, 100)
    }

    WEIGHT_FACTORS = {
        'technical_complexity': 0.25,
        'resource_availability': 0.20,
        'timeline_constraints': 0.15,
        'budget_constraints': 0.15,
        'stakeholder_involvement': 0.10,
        'regulatory_compliance': 0.15
    }
    
    def analyze_risk(self, risk_factors):
        if not risk_factors:
            raise ValueError("Risk factors cannot be empty")
        self._validate_risk_factors(risk_factors)
        weighted_score = 0
        for factor, weight in self.WEIGHT_FACTORS.items():
            if factor in risk_factors:
                weighted_score += (risk_factors[factor] / 10) * 100 * weight
        return round(weighted_score, 2)
    
    def get_risk_level(self, risk_score):
        if risk_score < self.RISK_LEVELS['low'][1]:
            return 'low'
        elif risk_score < self.RISK_LEVELS['medium'][1]:
            return 'medium'
        else:
            return 'high'
    
    def get_mitigation_recommendations(self, risk_factors, risk_score):
        recommendations = []
        risk_level = self.get_risk_level(risk_score)
        if risk_level == 'high':
            recommendations.append("Consider project restructuring or phased approach")
        elif risk_level == 'medium':
            recommendations.append("Implement detailed risk management plan")
        for factor, score in risk_factors.items():
            if score >= 7:  # High individual risk factor
                if factor == 'technical_complexity':
                    recommendations.append("Consider technical proof of concept before full implementation")
                elif factor == 'resource_availability':
                    recommendations.append("Secure additional resources or adjust project scope")
                elif factor == 'timeline_constraints':
                    recommendations.append("Re-evaluate timeline and consider extensions or phased delivery")
                elif factor == 'budget_constraints':
                    recommendations.append("Review budget allocation or seek additional funding sources")
                elif factor == 'stakeholder_involvement':
                    recommendations.append("Implement stakeholder engagement plan with regular touchpoints")
                elif factor == 'regulatory_compliance':
                    recommendations.append("Conduct compliance review with legal/regulatory experts")        
        return recommendations
    
    def _validate_risk_factors(self, risk_factors):
        missing_factors = set(self.WEIGHT_FACTORS.keys()) - set(risk_factors.keys())
        if missing_factors:
            raise ValueError(f"Missing required risk factors: {', '.join(missing_factors)}")
        invalid_values = {k: v for k, v in risk_factors.items() 
                         if not isinstance(v, (int, float)) or v < 1 or v > 10}        
        if invalid_values:
            raise ValueError(f"Invalid risk factor values: {invalid_values}. Values must be between 1 and 10")