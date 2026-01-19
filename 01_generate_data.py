import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_dubai_2026_dataset(rows=50000):
    np.random.seed(2026)
    
    # 1. Setup Anchors
    districts = {
        'Dubai Marina': {'rto_base': 0.05, 'cod_pref': 0.15},
        'JVC': {'rto_base': 0.12, 'cod_pref': 0.35},
        'International City': {'rto_base': 0.18, 'cod_pref': 0.55},
        'Dubai Hills': {'rto_base': 0.04, 'cod_pref': 0.10},
        'Business Bay': {'rto_base': 0.07, 'cod_pref': 0.20},
        'Al Barsha': {'rto_base': 0.09, 'cod_pref': 0.30}
    }
    
    payment_methods = ['COD', 'ApplePay', 'Credit_Card', 'Tabby_BNPL', 'Aani_Instant']
    
    data = []
    start_date = datetime(2026, 1, 1)

    for i in range(rows):
        # Time & Date
        date = start_date + timedelta(days=random.randint(0, 150), hours=random.randint(0, 23))
        is_ramadan = 1 if (datetime(2026, 2, 18) <= date <= datetime(2026, 3, 20)) else 0
        
        # Location & Payment
        district_name = random.choice(list(districts.keys()))
        district_stats = districts[district_name]
        
        # Bias payment method based on district
        if random.random() < district_stats['cod_pref']:
            method = 'COD'
        else:
            method = random.choice(['ApplePay', 'Credit_Card', 'Tabby_BNPL', 'Aani_Instant'])
            
        # 2. Logic for RTO (Return to Origin)
        # Base RTO + Payment Penalty + Temperature Penalty
        rto_prob = district_stats['rto_base']
        if method == 'COD': rto_prob += 0.15 # Massive penalty for Cash
        if method == 'Aani_Instant': rto_prob -= 0.02 # Instant payments are "Sticky"
        
        temp = random.randint(22, 48)
        if temp > 40: rto_prob += 0.05 # Heat leads to failed deliveries
        
        rto_flag = 1 if random.random() < rto_prob else 0
        
        # Financials
        order_val = np.random.exponential(300) + 50
        # Delivery cost = Base (10 AED) + Distance (KM * 0.5) + Return Penalty
        dist_km = random.randint(5, 35)
        delivery_cost = 10 + (dist_km * 0.5)
        if rto_flag == 1: delivery_cost += 15 # Add return processing cost
        
        data.append([
            f"TXN_{i:06d}", date, district_name, method, 
            round(order_val, 2), rto_flag, dist_km, temp, is_ramadan, round(delivery_cost, 2)
        ])

    columns = ['Transaction_ID', 'Timestamp', 'District', 'Payment_Method', 
               'Order_Value_AED', 'RTO_Flag', 'Distance_KM', 'Temperature_C', 'Is_Ramadan', 'Delivery_Cost_AED']
    
    return pd.DataFrame(data, columns=columns)

# Generate and save
df_dubai = generate_dubai_2026_dataset()
df_dubai.to_csv('dubai_cashless_2026_data.csv', index=False)
print("Phase 1 Complete: 50,000 rows of Dubai 2026 data generated!")