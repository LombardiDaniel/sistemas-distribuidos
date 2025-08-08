from datetime import datetime


class InvoiceModel:
    """
    A model to represent an invoice.
    """

    def __init__(
        self,
        invoice_id: int,
        customer_id: int,
        invoice_date: datetime,
        total: float,
        billing_address: str | None = None,
        billing_city: str | None = None,
        billing_state: str | None = None,
        billing_country: str | None = None,
        billing_postal_code: str | None = None,
    ):
        """
        Initializes a new InvoiceModel instance.

        Args:
            invoice_id (int): A unique identifier for the invoice.
            customer_id (int): The ID of the customer.
            invoice_date (datetime): The date and time of the invoice.
            total (float): The total amount of the invoice.
            billing_address (str, optional): The billing address. Defaults to None.
            billing_city (str, optional): The billing city. Defaults to None.
            billing_state (str, optional): The billing state. Defaults to None.
            billing_country (str, optional): The billing country. Defaults to None.
            billing_postal_code (str, optional): The billing postal code. Defaults to None.
        """
        self.invoice_id = invoice_id
        self.customer_id = customer_id
        self.invoice_date = invoice_date
        self.billing_address = billing_address
        self.billing_city = billing_city
        self.billing_state = billing_state
        self.billing_country = billing_country
        self.billing_postal_code = billing_postal_code
        self.total = total

    def to_dict(self) -> dict:
        """
        Converts the invoice model into a dictionary.
        The datetime object is converted to an ISO format string for serialization.
        """
        return {
            "invoice_id": self.invoice_id,
            "customer_id": self.customer_id,
            "invoice_date": self.invoice_date.isoformat(),
            "billing_address": self.billing_address,
            "billing_city": self.billing_city,
            "billing_state": self.billing_state,
            "billing_country": self.billing_country,
            "billing_postal_code": self.billing_postal_code,
            "total": self.total,
        }

    def __repr__(self):
        """
        Provides a string representation of the object for debugging.
        """
        return (
            f"<InvoiceModel(invoice_id={self.invoice_id}, "
            f"customer_id={self.customer_id}, total={self.total})>"
        )
