import psycopg2
from models import InvoiceModel


class InvoiceService:
    """
    A service for interacting with invoice data in a PostgreSQL database.
    """

    def __init__(self, conn):
        """
        Initializes the service with a psycopg2 connection object.

        Args:
            conn: A psycopg2 connection object to the database.
        """
        self.conn = conn

    def get_invoices(self) -> list[InvoiceModel]:
        """
        Fetches all invoices from the database.

        Returns:
            list[InvoiceModel]: A list of InvoiceModel objects.
        """
        invoices = []
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT * FROM invoice;")

                rows = cur.fetchall()

                for row in rows:
                    invoices.append(self._create_invoice_from_row(row))

        except psycopg2.Error as e:
            print(f"Database error: {e}")
            self.conn.rollback()

        return invoices

    def get_invoice_by_id(self, invoice_id: int) -> InvoiceModel | None:
        """
        Fetches a single invoice by its ID.

        Args:
            invoice_id (int): The ID of the invoice to retrieve.

        Returns:
            InvoiceModel or None: An InvoiceModel object if found, otherwise None.
        """
        invoice: InvoiceModel | None = None
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM invoice WHERE invoice_id = %s;", (invoice_id,)
                )

                row = cur.fetchone()

                if row:
                    invoice = self._create_invoice_from_row(row)
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            self.conn.rollback()

        return invoice

    def _create_invoice_from_row(self, row):
        """
        A helper method to create an InvoiceModel from a database row.

        Args:
            row (tuple): A single row from a psycopg2 query result.

        Returns:
            InvoiceModel: An instance of the InvoiceModel.
        """

        return InvoiceModel(
            invoice_id=row[0],
            customer_id=row[1],
            invoice_date=row[2],
            billing_address=row[3],
            billing_city=row[4],
            billing_state=row[5],
            billing_country=row[6],
            billing_postal_code=row[7],
            total=row[8],
        )

    def join_all(self) -> str:
        """executes a large join on the db"""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                    SELECT
                        c.first_name,
                        c.last_name,
                        c.email,
                        i.invoice_id,
                        i.invoice_date,
                        il.unit_price,
                        il.quantity,
                        t.name AS track_name,
                        a.title AS album_title,
                        ar.name AS artist_name,
                        g.name AS genre_name
                    FROM
                        customer c
                    JOIN
                        invoice i ON c.customer_id = i.customer_id
                    JOIN
                        invoice_line il ON i.invoice_id = il.invoice_id
                    JOIN
                        track t ON il.track_id = t.track_id
                    JOIN
                        album a ON t.album_id = a.album_id
                    JOIN
                        artist ar ON a.artist_id = ar.artist_id
                    JOIN
                        genre g ON t.genre_id = g.genre_id
                    ORDER BY
                        i.invoice_date DESC, c.last_name, c.first_name;
                """
            )
            rows = cur.fetchall()

            ret: list[str] = [
                "First Name | Last Name | Email | Invoice ID | Invoice Date | Unit Price | Quantity | Track Name | Album Title | Artist Name | Genre Name"
            ]
            for row in rows:
                ret.append(
                    f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} | {row[7]} | {row[8]} | {row[9]} | {row[10]}"
                )
            return "\n\n".join(ret)

    def insert_mock(self, count: int):
        """creates mock invoices"""
        for _ in range(count):
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                        -- This query inserts three new invoices starting from the next available invoice_id.
                        WITH
                        max_invoice AS (
                            SELECT
                            COALESCE(MAX(invoice_id), 0) AS max_id
                            FROM
                            invoice
                        )
                        INSERT INTO
                        invoice (
                            invoice_id,
                            customer_id,
                            invoice_date,
                            billing_address,
                            billing_city,
                            billing_state,
                            billing_country,
                            billing_postal_code,
                            total
                        )
                        SELECT
                        max_invoice.max_id + ROW_NUMBER() OVER (),
                        c.customer_id,
                        NOW(),
                        '123 Mock St.',
                        'Mockville',
                        'MS',
                        'USA',
                        '12345',
                        (random() * 100 + 5.0)::numeric(10, 2)
                        FROM
                        max_invoice,
                        -- Subquery to select existing customer IDs to use for the new invoices
                        (
                            SELECT
                            customer_id
                            FROM
                            customer
                            ORDER BY
                            RANDOM()
                            LIMIT
                            1
                        ) AS c;
                    """
                )

                self.conn.commit()
