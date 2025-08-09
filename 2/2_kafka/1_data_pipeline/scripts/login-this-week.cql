SELECT count(DISTINCT user_id) FROM user_telemetry
WHERE action = 'LOGGED_IN'
AND event_time >= now() - INTERVAL 7 DAY;