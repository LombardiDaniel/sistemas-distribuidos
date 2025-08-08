import services


class InvoiceHandler:
    """handlers regarding invoices"""

    def __init__(
        self,
        invoice_service: services.InvoiceService,
        cache_service: services.CacheService,
    ):
        self.invoice_service = invoice_service
        self.cache_service = cache_service

    def get_all(self):
        """get all invoices"""
        invoices = self.invoice_service.get_invoices()
        return [invoice.to_dict() for invoice in invoices]

    def get_invoice(self, invoice_id: int) -> dict:
        """get specific"""
        invoice = self.cache_service.get_invoice(invoice_id)
        if invoice is None:
            invoice = self.invoice_service.get_invoice_by_id(invoice_id)
        self.cache_service.set_invoice(invoice)  # reset ttl

        return invoice.to_dict()

    def get_join(self) -> str:
        """get large table join"""
        join = self.cache_service.get_join()
        if join is None:
            join = self.invoice_service.join_all()
        self.cache_service.set_join(join)  # reset ttl

        return join

    def create_mock_invoices(self, count: int):
        self.invoice_service.insert_mock(count)
        return "OK"
