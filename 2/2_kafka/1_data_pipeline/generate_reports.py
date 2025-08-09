from collections import defaultdict
from datetime import datetime, timedelta

import models
from cassandra.cluster import Cluster

CASSANDRA_CLUSTER = Cluster(["127.0.0.1"], port=9042)
CASSANDRA_SESSION = CASSANDRA_CLUSTER.connect("telemetry")


def run_analytics_queries_with_python():
    """
    Fetches data from Cassandra and performs analytics in Python.
    """
    print("Fetching all telemetry data from Cassandra...")
    # This query will read all rows, which is not scalable for a large dataset.
    rows = CASSANDRA_SESSION.execute(
        "SELECT user_id, action, event_time FROM user_telemetry"
    )
    print("Data fetch complete. Starting analysis...")

    # A list to store all events
    events = []
    for row in rows:
        events.append(
            {
                "user_id": row.user_id,
                "action": row.action,
                "event_time": row.event_time,
            }
        )

    # --- Query 1: How many unique users logged in this week? ---
    print("\n" + "=" * 50)
    print("1. Unique users logged in this week")
    one_week_ago = datetime.now() - timedelta(days=7)

    logged_in_users_this_week = set()
    for event in events:
        if event["action"] == "LOGGED_IN" and event["event_time"] >= one_week_ago:
            logged_in_users_this_week.add(event["user_id"])

    print(f"Result: {len(logged_in_users_this_week)} unique users logged in this week.")

    # --- Query 2: What's the most common action performed by users before a purchase? ---
    print("\n" + "=" * 50)
    print("2. Most common action before a purchase")

    pre_purchase_actions = defaultdict(int)
    # Sort events by user and time to easily find sequences
    events.sort(key=lambda x: (x["user_id"], x["event_time"]))

    for i, event in enumerate(events):
        if event["action"] == models.ActionTypes.PURCHASED.name and i > 0:
            previous_event = events[i - 1]
            # Check if the previous event is from the same user and within a reasonable timeframe (e.g., 5 minutes)
            if (
                previous_event["user_id"] == event["user_id"]
                and (event["event_time"] - previous_event["event_time"]).total_seconds()
                <= 300
            ):
                pre_purchase_actions[previous_event["action"]] += 1

    if pre_purchase_actions:
        most_common_action = max(pre_purchase_actions, key=pre_purchase_actions.get)
        count = pre_purchase_actions[most_common_action]
        print(
            f"Result: The most common action before a purchase is '{most_common_action}' with {count} occurrences."
        )
    else:
        print("Result: No pre-purchase actions found.")

    # --- Query 3: How many users added an item to their cart but didn't purchase it? ---
    print("\n" + "=" * 50)
    print("3. Users who added to cart but didn't purchase")

    added_to_cart_users = set()
    purchased_users = set()

    for event in events:
        if event["action"] == models.ActionTypes.ADDED_TO_CART.name:
            added_to_cart_users.add(event["user_id"])
        elif event["action"] == models.ActionTypes.PURCHASED.name:
            purchased_users.add(event["user_id"])

    # Use set difference to find users who added to cart but didn't purchase
    non_purchasing_users = added_to_cart_users - purchased_users

    print(
        f"Result: {len(non_purchasing_users)} users added an item to their cart but didn't purchase."
    )


if __name__ == "__main__":
    run_analytics_queries_with_python()
    CASSANDRA_CLUSTER.shutdown()
