import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import uuid
import matplotlib.pyplot as plt
import seaborn as sns
from models import Policyholder, Claim
from database import Database

db = Database()
print("DB instance:", db)

def load_sample_data():
    if len(db.policyholders) == 0 and len(db.claims) == 0:
        # Sample policyholders
        policyholders = [
            Policyholder("John Abhram", 35, "Health", 500000),
            Policyholder("Jane Smith", 42, "Vehicle", 300000),
            Policyholder("Varun Dhawan", 50, "Life", 1000000),
            Policyholder("Lisa Ray", 28, "Health", 400000),
        ]     
        for policyholder in policyholders:
            db.add_policyholder(policyholder)        
        # Sample claims
        claims = [
            Claim(policyholders[0].id, 50000, "Medical Treatment", "Approved", (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")),
            Claim(policyholders[0].id, 30000, "Surgery", "Pending", (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d")),
            Claim(policyholders[1].id, 80000, "Car Accident", "Approved", (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")),
            Claim(policyholders[2].id, 100000, "Critical Illness", "Rejected", (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")),
        ]        
        for claim in claims:
            db.add_claim(claim)

# Page configuration
st.set_page_config(
    page_title="ABC Insurance - Claim Management System",
    page_icon="📋",
    layout="wide",
)

# Title and sidebar navigation
st.title("ABC Insurance - Claim Management System")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Policyholder Management", "Claim Management", "Risk Analysis", "Reports"])

load_sample_data()

# Policyholder Management Page
if page == "Policyholder Management":
    st.header("Policyholder Management")   
    # Create tabs 
    tab1, tab2, tab3 = st.tabs(["Add Policyholder", "View Policyholders", "Edit Policyholder"])
    
    with tab1:
        st.subheader("Add New Policyholder")        
        with st.form("add_policyholder_form"):
            name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
            policy_type = st.selectbox("Policy Type", ["Health", "Vehicle", "Life"])
            sum_insured = st.number_input("Sum Insured", min_value=100000, max_value=10000000, value=500000, step=100000)            
            submit_button = st.form_submit_button("Register Policyholder")            
            if submit_button:
                if not name:
                    st.error("Name cannot be empty")
                else:
                    new_policyholder = Policyholder(name, age, policy_type, sum_insured)
                    db.add_policyholder(new_policyholder)
                    st.success(f"Policyholder {name} registered successfully with ID: {new_policyholder.id}")
    
    with tab2:
        st.subheader("View All Policyholders")        
        if not db.policyholders:
            st.info("No policyholders registered yet.")
        else:
            # Convert policyholders
            policyholder_data = []
            for p in db.policyholders.values():
                policyholder_data.append({
                    "ID": p.id,
                    "Name": p.name,
                    "Age": p.age,
                    "Policy Type": p.policy_type,
                    "Sum Insured": f"${p.sum_insured:,}"
                })            
            df = pd.DataFrame(policyholder_data)
            st.dataframe(df, use_container_width=True)
    
    with tab3:
        st.subheader("Edit Policyholder")        
        if not db.policyholders:
            st.info("No policyholders registered yet.")
        else:
            policyholder_id = st.selectbox("Select Policyholder to Edit", 
                                          options=list(db.policyholders.keys()),
                                          format_func=lambda x: f"{db.policyholders[x].name} (ID: {x})")            
            if policyholder_id:
                policyholder = db.policyholders[policyholder_id]                
                with st.form("edit_policyholder_form"):
                    name = st.text_input("Full Name", value=policyholder.name)
                    age = st.number_input("Age", min_value=18, max_value=100, value=policyholder.age)
                    policy_type = st.selectbox("Policy Type", ["Health", "Vehicle", "Life"], index=["Health", "Vehicle", "Life"].index(policyholder.policy_type))
                    sum_insured = st.number_input("Sum Insured", min_value=100000, max_value=10000000, value=policyholder.sum_insured, step=100000)                    
                    submit_button = st.form_submit_button("Update Policyholder")
                    if submit_button:
                        if not name:
                            st.error("Name cannot be empty")
                        else:
                            policyholder.name = name
                            policyholder.age = age
                            policyholder.policy_type = policy_type
                            policyholder.sum_insured = sum_insured
                            db.save_data()
                            st.success(f"Policyholder {name} updated successfully")

# Claim Management Page
elif page == "Claim Management":
    st.header("Claim Management")    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Add Claim", "View Claims", "Update Claim Status"])    
    with tab1:
        st.subheader("Add New Claim")        
        if not db.policyholders:
            st.warning("No policyholders registered yet. Please add policyholders first.")
        else:
            with st.form("add_claim_form"):
                policyholder_id = st.selectbox("Select Policyholder", 
                                              options=list(db.policyholders.keys()),
                                              format_func=lambda x: f"{db.policyholders[x].name} (ID: {x})")                
                claim_amount = st.number_input("Claim Amount", min_value=1000, max_value=10000000, value=50000)
                reason = st.text_input("Reason for Claim")
                claim_status = st.selectbox("Claim Status", ["Pending", "Approved", "Rejected"], index=0)
                claim_date = st.date_input("Date of Claim", max_value=datetime.now())                
                submit_button = st.form_submit_button("Add Claim")                
                if submit_button:
                    if not reason:
                        st.error("Reason cannot be empty")
                    else:
                        policyholder = db.policyholders[policyholder_id]
                        if claim_amount > policyholder.sum_insured:
                            st.error(f"Claim amount exceeds the sum insured (${policyholder.sum_insured:,})")
                        else:
                            new_claim = Claim(
                                policyholder_id, 
                                claim_amount, 
                                reason, 
                                claim_status, 
                                claim_date.strftime("%Y-%m-%d")
                            )
                            db.add_claim(new_claim)
                            st.success(f"Claim added successfully with ID: {new_claim.id}")
    
    with tab2:
        st.subheader("View All Claims")        
        if not db.claims:
            st.info("No claims registered yet.")
        else:
            claim_data = []
            for c in db.claims.values():
                policyholder = db.policyholders.get(c.policyholder_id, None)
                policyholder_name = policyholder.name if policyholder else "Unknown"                
                claim_data.append({
                    "Claim ID": c.id,
                    "Policyholder": policyholder_name,
                    "Amount": f"${c.amount:,}",
                    "Reason": c.reason,
                    "Status": c.status,
                    "Date": c.date
                })            
            df = pd.DataFrame(claim_data)
            st.dataframe(df, use_container_width=True)
    
    with tab3:
        st.subheader("Update Claim Status")        
        if not db.claims:
            st.info("No claims registered yet.")
        else:
            claim_id = st.selectbox("Select Claim to Update", 
                                  options=list(db.claims.keys()),
                                  format_func=lambda x: f"Claim {x} - {db.claims[x].reason} (${db.claims[x].amount:,})")           
            if claim_id:
                claim = db.claims[claim_id]
                policyholder = db.policyholders.get(claim.policyholder_id, None)
                policyholder_name = policyholder.name if policyholder else "Unknown"                
                st.write(f"Policyholder: {policyholder_name}")
                st.write(f"Claim Amount: ${claim.amount:,}")
                st.write(f"Reason: {claim.reason}")
                st.write(f"Current Status: {claim.status}")                
                new_status = st.selectbox("New Status", ["Pending", "Approved", "Rejected"], index=["Pending", "Approved", "Rejected"].index(claim.status))                
                if st.button("Update Status"):
                    claim.status = new_status
                    db.save_data()
                    st.success(f"Claim status updated to {new_status}")

# Risk Analysis Page
elif page == "Risk Analysis":
    st.header("Risk Analysis")
    if not db.claims or not db.policyholders:
        st.warning("Insufficient data for risk analysis. Please add more policyholders and claims.")
    else:
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["Claim Frequency", "High Risk Policyholders", "Claims by Policy Type"])        
        with tab1:
            st.subheader("Claim Frequency per Policyholder")
            claim_frequency = {}
            for ph_id in db.policyholders:
                policyholder_name = db.policyholders[ph_id].name
                count = sum(1 for c in db.claims.values() if c.policyholder_id == ph_id)
                claim_frequency[policyholder_name] = count
            df_freq = pd.DataFrame(list(claim_frequency.items()), columns=['Policyholder', 'Number of Claims'])
            df_freq = df_freq.sort_values('Number of Claims', ascending=False)
            st.dataframe(df_freq, use_container_width=True)
            
            # Create bar chart
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x='Policyholder', y='Number of Claims', data=df_freq, ax=ax)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
        
        with tab2:
            st.subheader("High Risk Policyholders")
            high_risk_data = []
            one_year_ago = datetime.now() - timedelta(days=365)
            
            for ph_id, policyholder in db.policyholders.items():
                claims_last_year = sum(1 for c in db.claims.values() 
                                     if c.policyholder_id == ph_id and 
                                     datetime.strptime(c.date, "%Y-%m-%d") > one_year_ago)
                total_claim_amount = sum(c.amount for c in db.claims.values() 
                                       if c.policyholder_id == ph_id)
                claim_ratio = (total_claim_amount / policyholder.sum_insured) * 100 if policyholder.sum_insured > 0 else 0
                risk_factors = []
                if claims_last_year > 3:
                    risk_factors.append("Frequent Claims")
                if claim_ratio > 80:
                    risk_factors.append("High Claim Ratio")
                if risk_factors:
                    high_risk_data.append({
                        "Policyholder": policyholder.name,
                        "Policy Type": policyholder.policy_type,
                        "Claims (Last Year)": claims_last_year,
                        "Total Claim Amount": f"${total_claim_amount:,}",
                        "Sum Insured": f"${policyholder.sum_insured:,}",
                        "Claim Ratio": f"{claim_ratio:.2f}%",
                        "Risk Factors": ", ".join(risk_factors)
                    })
            if high_risk_data:
                df_risk = pd.DataFrame(high_risk_data)
                st.dataframe(df_risk, use_container_width=True)
            else:
                st.info("No high-risk policyholders identified.")
        
        with tab3:
            st.subheader("Claims by Policy Type")
            policy_claims = {}
            for claim in db.claims.values():
                ph = db.policyholders.get(claim.policyholder_id)
                if ph:
                    if ph.policy_type not in policy_claims:
                        policy_claims[ph.policy_type] = {
                            "count": 0,
                            "total_amount": 0,
                            "approved": 0,
                            "pending": 0,
                            "rejected": 0
                        }
                    policy_claims[ph.policy_type]["count"] += 1
                    policy_claims[ph.policy_type]["total_amount"] += claim.amount
                    if claim.status == "Approved":
                        policy_claims[ph.policy_type]["approved"] += 1
                    elif claim.status == "Pending":
                        policy_claims[ph.policy_type]["pending"] += 1
                    elif claim.status == "Rejected":
                        policy_claims[ph.policy_type]["rejected"] += 1
            policy_claims_data = []
            for policy_type, data in policy_claims.items():
                policy_claims_data.append({
                    "Policy Type": policy_type,
                    "Total Claims": data["count"],
                    "Total Amount": f"${data['total_amount']:,}",
                    "Approved Claims": data["approved"],
                    "Pending Claims": data["pending"],
                    "Rejected Claims": data["rejected"],
                    "Average Claim": f"${data['total_amount'] / data['count']:,.2f}" if data["count"] > 0 else "$0"
                })
            df_policy = pd.DataFrame(policy_claims_data)
            st.dataframe(df_policy, use_container_width=True)
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            labels = [data["Policy Type"] for data in policy_claims_data]
            values = [data["Total Claims"] for data in policy_claims_data]
            ax1.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
            ax1.set_title('Claims Count by Policy Type')
            amount_values = [policy_claims[pt]["total_amount"] for pt in policy_claims]
            ax2.pie(amount_values, labels=labels, autopct='%1.1f%%', startangle=90)
            ax2.set_title('Claims Amount by Policy Type')
            plt.tight_layout()
            st.pyplot(fig)
elif page == "Reports":
    st.header("Reports Module")
    if not db.claims or not db.policyholders:
        st.warning("Insufficient data for reports. Please add more policyholders and claims.")
    else:
        tab1, tab2, tab3, tab4 = st.tabs([
            "Claims per Month", 
            "Average Claim by Policy Type", 
            "Highest Claims", 
            "Pending Claims"
        ])
        with tab1:
            st.subheader("Total Claims per Month")
            claims_by_month = {}
            for claim in db.claims.values():
                claim_date = datetime.strptime(claim.date, "%Y-%m-%d")
                month_key = claim_date.strftime("%Y-%m")
                month_name = claim_date.strftime("%B %Y")  
                if month_key not in claims_by_month:
                    claims_by_month[month_key] = {
                        "month_name": month_name,
                        "count": 0,
                        "total_amount": 0
                    }
                claims_by_month[month_key]["count"] += 1
                claims_by_month[month_key]["total_amount"] += claim.amount
            monthly_data = []
            for month_key, data in sorted(claims_by_month.items()):
                monthly_data.append({
                    "Month": data["month_name"],
                    "Number of Claims": data["count"],
                    "Total Amount": f"${data['total_amount']:,}",
                    "Average Claim": f"${data['total_amount'] / data['count']:,.2f}"
                })
            df_monthly = pd.DataFrame(monthly_data)
            st.dataframe(df_monthly, use_container_width=True)
            fig, ax = plt.subplots(figsize=(10, 6))
            months = [data["Month"] for data in monthly_data]
            counts = [data["Number of Claims"] for data in monthly_data]    
            sns.barplot(x=months, y=counts, ax=ax)
            plt.xticks(rotation=45, ha='right')
            plt.ylabel("Number of Claims")
            plt.title("Claims per Month")
            plt.tight_layout()
            st.pyplot(fig)
        with tab2:
            st.subheader("Average Claim Amount by Policy Type")
            avg_claim_by_policy = {}
            for claim in db.claims.values():
                ph = db.policyholders.get(claim.policyholder_id)
                if ph:
                    if ph.policy_type not in avg_claim_by_policy:
                        avg_claim_by_policy[ph.policy_type] = {
                            "total_amount": 0,
                            "count": 0
                        }
                    avg_claim_by_policy[ph.policy_type]["total_amount"] += claim.amount
                    avg_claim_by_policy[ph.policy_type]["count"] += 1
            avg_data = []
            for policy_type, data in avg_claim_by_policy.items():
                average = data["total_amount"] / data["count"] if data["count"] > 0 else 0
                avg_data.append({
                    "Policy Type": policy_type,
                    "Average Claim Amount": average,
                    "Average Claim": f"${average:,.2f}",
                    "Total Claims": data["count"],
                    "Total Amount": f"${data['total_amount']:,}"
                })    
            df_avg = pd.DataFrame(avg_data).sort_values("Average Claim Amount", ascending=False)
            display_df = df_avg.drop(columns=["Average Claim Amount"])
            st.dataframe(display_df, use_container_width=True)
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x="Policy Type", y="Average Claim Amount", data=df_avg, ax=ax)
            plt.ylabel("Average Claim Amount ($)")
            plt.title("Average Claim Amount by Policy Type")
            plt.tight_layout()
            st.pyplot(fig)
        
        with tab3:
            st.subheader("Highest Claims Filed")
            highest_claims = []
            for claim in db.claims.values():
                ph = db.policyholders.get(claim.policyholder_id)
                if ph:
                    highest_claims.append({
                        "Claim ID": claim.id,
                        "Policyholder": ph.name,
                        "Policy Type": ph.policy_type,
                        "Amount": claim.amount,
                        "Formatted Amount": f"${claim.amount:,}",
                        "Reason": claim.reason,
                        "Status": claim.status,
                        "Date": claim.date
                    })
            df_highest = pd.DataFrame(highest_claims).sort_values("Amount", ascending=False).head(10)
            display_df = df_highest.drop(columns=["Amount"])
            st.dataframe(display_df, use_container_width=True)
        
        with tab4:
            st.subheader("Policyholders with Pending Claims")
            pending_claims = []
            for claim in db.claims.values():
                if claim.status == "Pending":
                    ph = db.policyholders.get(claim.policyholder_id)
                    if ph:
                        pending_claims.append({
                            "Claim ID": claim.id,
                            "Policyholder": ph.name,
                            "Policy Type": ph.policy_type,
                            "Amount": f"${claim.amount:,}",
                            "Reason": claim.reason,
                            "Date": claim.date,
                            "Days Pending": (datetime.now() - datetime.strptime(claim.date, "%Y-%m-%d")).days
                        })
            if pending_claims:
                df_pending = pd.DataFrame(pending_claims).sort_values("Days Pending", ascending=False)
                st.dataframe(df_pending, use_container_width=True)
            else:
                st.info("No pending claims found.")
db.save_data()
