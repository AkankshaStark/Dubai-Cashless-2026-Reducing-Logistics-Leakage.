SELECT 
    District,
    COUNT(*) as Total_Orders,
    ROUND(AVG(RTO_Flag) * 100, 2) as RTO_Rate_Percentage,
    ROUND(SUM(CASE WHEN RTO_Flag = 1 THEN Delivery_Cost_AED ELSE 0 END), 2) as Total_Loss_AED
FROM transactions
WHERE Payment_Method = 'COD'
GROUP BY District
ORDER BY Total_Loss_AED DESC;

SELECT 
    Payment_Method,
    COUNT(*) as Volume,
    ROUND(AVG(Order_Value_AED), 2) as Avg_Order_Value,
    ROUND(AVG(RTO_Flag) * 100, 2) as Return_Rate,
    ROUND(AVG(Delivery_Cost_AED), 2) as Avg_Logistics_Cost
FROM transactions
GROUP BY Payment_Method;