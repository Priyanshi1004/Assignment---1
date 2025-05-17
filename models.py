import uuid
from datetime import datetime

class Policyholder:
    def __init__(self, name, age, policy_type, sum_insured):
        self.id = str(uuid.uuid4())[:8]  
        self.name = name
        self.age = age
        self.policy_type = policy_type
        self.sum_insured = sum_insured
        self.registration_date = datetime.now().strftime("%Y-%m-%d")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "policy_type": self.policy_type,
            "sum_insured": self.sum_insured,
            "registration_date": self.registration_date
        }
    
    @classmethod
    def from_dict(cls, data):
        policyholder = cls(
            data["name"],
            data["age"],
            data["policy_type"],
            data["sum_insured"]
        )
        policyholder.id = data["id"]
        policyholder.registration_date = data["registration_date"]
        return policyholder


class Claim:
    def __init__(self, policyholder_id, amount, reason, status, date=None):
        self.id = str(uuid.uuid4())[:8]  # Generate a short unique ID
        self.policyholder_id = policyholder_id
        self.amount = amount
        self.reason = reason
        self.status = status
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")
    
    def to_dict(self):
        return {
            "id": self.id,
            "policyholder_id": self.policyholder_id,
            "amount": self.amount,
            "reason": self.reason,
            "status": self.status,
            "date": self.date
        }
    
    @classmethod
    def from_dict(cls, data):
        claim = cls(
            data["policyholder_id"],
            data["amount"],
            data["reason"],
            data["status"],
            data["date"]
        )
        claim.id = data["id"]
        return claim