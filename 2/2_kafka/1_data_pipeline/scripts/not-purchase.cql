SELECT count(DISTINCT user_id) FROM user_telemetry
WHERE action = 'ADDED_TO_CART'
AND user_id NOT IN (
    SELECT DISTINCT user_id FROM user_telemetry
    WHERE action = 'PURCHASED'
);