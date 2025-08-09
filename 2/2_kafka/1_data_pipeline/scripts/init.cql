CREATE KEYSPACE telemetry WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

CREATE TABLE telemetry.user_telemetry (
    user_id text,
    action text,
    event_time timestamp,
    PRIMARY KEY (user_id, event_time)
);