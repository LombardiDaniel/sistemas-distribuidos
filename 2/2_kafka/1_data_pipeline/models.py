import json
from datetime import datetime
from enum import Enum


class TelemetryEvent:
    """telemetry messages in kafka"""

    def __init__(
        self, user_id: str = "", action: str = "", timestamp: datetime = datetime.now()
    ):
        self.user_id = user_id
        self.action = action
        self.timestamp = timestamp

    def dump(self) -> bytes:
        """dumps to json"""
        return json.dumps(
            {
                "userId": self.user_id,
                "action": self.action,
                "timestamp": self.timestamp.strftime("%d/%m/%Y, %H:%M:%S"),
            }
        ).encode()

    def load(self, data: bytes | str):
        """loads from the data"""
        d = json.loads(data)
        self.user_id = d["userId"]
        self.action = d["action"]
        self.timestamp = datetime.strptime(d["timestamp"], "%d/%m/%Y, %H:%M:%S")


class ActionTypes(Enum):
    ENTERED = 1
    EXITED = 2
    PURCHASED = 3
    VIEWED = 4
    CLICKED = 5
    ADDED_TO_CART = 6
    REMOVED_FROM_CART = 7
    WISHLISTED = 8
    SHARED = 9
    COMMENTED = 10
    LIKED = 11
    RATED = 12
    SUBSCRIBED = 13
    UNSUBSCRIBED = 14
    LOGGED_IN = 15
    LOGGED_OUT = 16
    SIGNED_UP = 17
    UPDATED_PROFILE = 18
    DELETED_ACCOUNT = 19
    SEARCHED = 20
    FILTERED = 21
    SORTED = 22
    DOWNLOADED = 23
    UPLOADED = 24
    STARTED_TRIAL = 25
    CANCELED_SUBSCRIPTION = 26
    REFUNDED = 27
    RECEIVED_MESSAGE = 28
    SENT_MESSAGE = 29
    JOINED_GROUP = 30
    LEFT_GROUP = 31
    BOOKMARKED = 32
    COMPLETED_TUTORIAL = 33
    FAILED_PAYMENT = 34
    ATTEMPTED_LOGIN = 35
    FORGOT_PASSWORD = 36
    ACCEPTED_TERMS = 37
    REJECTED_TERMS = 38
