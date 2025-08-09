WITH UserEvents AS (
  -- Get all 'PURCHASED' events
  SELECT user_id, event_time AS purchase_time
  FROM user_telemetry
  WHERE action = 'PURCHASED'
),
PrePurchaseEvents AS (
  -- Get the event that occurred immediately before the purchase for each user
  SELECT
    t1.user_id,
    t1.action AS pre_purchase_action
  FROM user_telemetry t1
  JOIN UserEvents t2 ON t1.user_id = t2.user_id
  WHERE
    t1.event_time < t2.purchase_time
    AND t1.event_time >= t2.purchase_time - INTERVAL 5 MINUTE -- Events within 5 minutes
)
-- Count the occurrences of each pre-purchase action
SELECT
  pre_purchase_action,
  count(pre_purchase_action) AS action_count
FROM PrePurchaseEvents
GROUP BY pre_purchase_action
ORDER BY action_count DESC
LIMIT 1;