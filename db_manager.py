class DBManager:
    def __init__(self, *args, **kwargs):
        self.risks = []
        self.next_id = 1

    def get_all_risks(self):
        return self.risks

    def get_risk_by_id(self, risk_id):
        for risk in self.risks:
            if risk['id'] == risk_id:
                return risk
        return None

    def create_risk(self, risk_data):
        risk_data['id'] = self.next_id
        self.next_id += 1
        self.risks.append(risk_data)
        return risk_data['id']

    def update_risk(self, risk_id, updated_data):
        for i, risk in enumerate(self.risks):
            if risk['id'] == risk_id:
                self.risks[i].update(updated_data)
                return True
        return False

    def delete_risk(self, risk_id):
        for i, risk in enumerate(self.risks):
            if risk['id'] == risk_id:
                del self.risks[i]
                return True
        return False
