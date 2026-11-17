-- Supplier scorecard: on-time rate, quality, average lead time and cost variance.
SELECT supplier_id, COUNT(*) AS orders,
 ROUND(100.0*AVG(CASE WHEN actual_days<=promised_days THEN 1.0 ELSE 0.0 END),2) AS on_time_pct,
 ROUND(100.0*AVG(quality_issue),2) AS defect_pct,
 ROUND(AVG(actual_days),1) AS mean_lead_days,
 ROUND(100.0*(SUM(actual_cost_eur)/SUM(quoted_cost_eur)-1),2) AS variance_pct
FROM orders GROUP BY supplier_id ORDER BY on_time_pct;

-- Monthly operational trends
SELECT SUBSTR(order_date,1,7) AS month, COUNT(*) AS orders,
 ROUND(100.0*AVG(CASE WHEN actual_days<=promised_days THEN 1.0 ELSE 0.0 END),2) AS on_time_pct,
 ROUND(SUM(actual_cost_eur)-SUM(quoted_cost_eur),2) AS cost_variance_eur
FROM orders GROUP BY SUBSTR(order_date,1,7) ORDER BY month;

-- Drilldown of late orders (origin, supplier and product)
SELECT origin,supplier_id,product,COUNT(*) AS orders,
 SUM(CASE WHEN actual_days>promised_days THEN 1 ELSE 0 END) AS late_orders
FROM orders GROUP BY origin,supplier_id,product ORDER BY late_orders DESC;

-- Cost exposure by delivery status
SELECT CASE WHEN actual_days>promised_days THEN 'Late' ELSE 'On time' END AS delivery_status,
 COUNT(*) AS orders,
 ROUND(SUM(actual_cost_eur)-SUM(quoted_cost_eur),2) AS cost_variance_eur
FROM orders GROUP BY delivery_status;
