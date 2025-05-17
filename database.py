import json
import os
from models import Policyholder, Claim

class Database:
    def __init__(self, data_dir="./data"):
        print("Using OUR Database class!")
        print("Running Database.__init__")
        print("Policyholders before init:", hasattr(self, 'policyholders'))
        self.policyholders = {}  # policyholders by ID
        self.claims = {}  # claims by ID
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        self.load_data()
    
    def add_policyholder(self, policyholder):
        self.policyholders[policyholder.id] = policyholder
        self.save_data()
    
    def update_policyholder(self, policyholder_id, updated_data):
        if policyholder_id in self.policyholders:
            policyholder = self.policyholders[policyholder_id]
            for key, value in updated_data.items():
                if hasattr(policyholder, key):
                    setattr(policyholder, key, value)    
            self.save_data()
            return True
        return False
    
    def delete_policyholder(self, policyholder_id):
        if policyholder_id in self.policyholders:
            # exisiting claims
            has_claims = any(claim.policyholder_id == policyholder_id for claim in self.claims.values())
            if not has_claims:
                del self.policyholders[policyholder_id]
                self.save_data()
                return True
            else:
                return False
        return False
    
    def add_claim(self, claim):
        if claim.policyholder_id in self.policyholders:
            self.claims[claim.id] = claim
            self.save_data()
            return True
        return False
    
    def update_claim_status(self, claim_id, new_status):
        if claim_id in self.claims:
            self.claims[claim_id].status = new_status
            self.save_data()
            return True
        return False
    
    def delete_claim(self, claim_id):
        if claim_id in self.claims:
            del self.claims[claim_id]
            self.save_data()
            return True
        return False
    
    def save_data(self):
        try:
            policyholder_data = {
                ph_id: ph.to_dict() for ph_id, ph in self.policyholders.items()
            }
            with open(os.path.join(self.data_dir, "policyholders.json"), "w") as f:
                json.dump(policyholder_data, f, indent=4)
            claim_data = {
                claim_id: claim.to_dict() for claim_id, claim in self.claims.items()
            }
            with open(os.path.join(self.data_dir, "claims.json"), "w") as f:
                json.dump(claim_data, f, indent=4)    
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def load_data(self):
        try:
            ph_file = os.path.join(self.data_dir, "policyholders.json")
            if os.path.exists(ph_file):
                with open(ph_file, "r") as f:
                    policyholder_data = json.load(f)
                    for ph_id, ph_dict in policyholder_data.items():
                        self.policyholders[ph_id] = Policyholder.from_dict(ph_dict)
            claims_file = os.path.join(self.data_dir, "claims.json")
            if os.path.exists(claims_file):
                with open(claims_file, "r") as f:
                    claim_data = json.load(f)
                    for claim_id, claim_dict in claim_data.items():
                        self.claims[claim_id] = Claim.from_dict(claim_dict)                
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
            
    def get_claims_for_policyholder(self, policyholder_id):
        return [claim for claim in self.claims.values() if claim.policyholder_id == policyholder_id]