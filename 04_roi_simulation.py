import pandas as pd
import joblib

# Load the data and the trained model from Phase 3
df = pd.read_csv('dubai_cashless_2026_data.csv')
model = joblib.load('rto_predictor_model.pkl')
cols = joblib.load('model_columns.pkl')

# 1. Prepare features for prediction
X = pd.get_dummies(df[['District', 'Payment_Method', 'Order_Value_AED', 'Distance_KM', 'Temperature_C', 'Is_Ramadan']], drop_first=True)
X = X.reindex(columns=cols, fill_value=0)

# 2. Identify "High Risk" orders
df['Risk_Score'] = model.predict_proba(X)[:, 1] # Probability of being an RTO
df['Predicted_High_Risk'] = (df['Risk_Score'] > 0.6).astype(int)

# 3. Simulate the "Nudge" Strategy
# We only nudge customers who chose COD and are flagged as High Risk
nudge_candidates = df[(df['Payment_Method'] == 'COD') & (df['Predicted_High_Risk'] == 1)]

# Financial Impact Calculations
conversion_rate = 0.70
savings_per_prevented_rto = 15.00
incentive_cost = 5.00

prevented_returns = len(nudge_candidates) * conversion_rate
gross_savings = prevented_returns * savings_per_prevented_rto
total_incentive_spend = prevented_returns * incentive_cost
net_logistics_profit = gross_savings - total_incentive_spend

# 4. Final Report
print(f"--- DUBAI 2026 CASHLESS ROI REPORT ---")
print(f"Total Transactions Analyzed: {len(df)}")
print(f"High-Risk COD Orders Flagged: {len(nudge_candidates)}")
print(f"Predicted Returns Prevented: {int(prevented_returns)}")
print(f"---------------------------------------")
print(f"Gross Logistics Savings:  AED {gross_savings:,.2f}")
print(f"Incentive Cost (Aani):   AED {total_incentive_spend:,.2f}")
print(f"NET ANNUAL SAVINGS:      AED {net_logistics_profit:,.2f}")