import psycopg2


class UserService:
    """
    A service for interacting with users
    """

    def __init__(self, conn):
        """
        Initializes the service with a psycopg2 connection object.

        Args:
            conn: A psycopg2 connection object to the database.
        """
        self.conn = conn

    def get_user_by_id(self, user_id: int) -> str:
        """
        Fetches a single user by its ID.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT name FROM artist WHERE artist_id = %s;", (user_id,))

                row = cur.fetchone()

                return row[0]

        except psycopg2.Error as e:
            print(f"Database error: {e}")
            self.conn.rollback()

        return ""

    def update_user(self, user_id: int, user_name: str):
        """
        Fetches a single user by its ID.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "UPDATE artist SET name = %s WHERE artist_id = %s;",
                    (
                        user_name,
                        user_id,
                    ),
                )

                self.conn.commit()

        except psycopg2.Error as e:
            print(f"Database error: {e}")
            self.conn.rollback()

        return ""
