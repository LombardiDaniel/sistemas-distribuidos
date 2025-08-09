"""git clone https://github.com/lerocha/chinook-database"""

import time

import handlers
import psycopg2
import redis
import services
from flask import Flask, request

app = Flask(__name__)

# CLIENTS
db_conn = psycopg2.connect(
    dbname="chinook",
    user="user",
    password="password",
    host="localhost",
    port="5432",
)
redis_client = redis.Redis(host="0.0.0.0", port=6379, db=0)

# SERVICES
invoice_service = services.InvoiceService(db_conn)
cache_service = services.CacheService(redis_client)
user_service = services.UserService(db_conn)

# HANDLERS
invoice_handler = handlers.InvoiceHandler(invoice_service, cache_service)
user_handler = handlers.UserHandler(user_service, cache_service)

# ROUTES
app.add_url_rule(
    "/invoices",
    view_func=invoice_handler.get_all,
    endpoint="get_invoices",
    methods=["GET"],
)
app.add_url_rule(
    "/invoices/<int:invoice_id>",
    view_func=invoice_handler.get_invoice,
    endpoint="get_invoices_by_id",
    methods=["GET"],
)
app.add_url_rule(
    "/invoices/add_mock/<int:count>",
    view_func=invoice_handler.create_mock_invoices,
    endpoint="insert_mock",
    methods=["GET"],
)
app.add_url_rule(
    "/join",
    view_func=invoice_handler.get_join,
    endpoint="get_join",
    methods=["GET"],
)

app.add_url_rule(
    "/users/<int:user_id>",
    view_func=user_handler.get_user_by_id,
    endpoint="get_user",
    methods=["GET"],
)

app.add_url_rule(
    # "/users/update/<int:user_id>/<string:user_name>",
    "/users/<int:user_id>",
    view_func=user_handler.update_user_name,
    endpoint="update_user",
    methods=["POST"],
)


@app.before_request
def before_request_func():
    request.start_time = time.time()


@app.after_request
def after_request_func(response):
    duration = time.time() - request.start_time
    print(f"Request to {request.path} took {duration:.4f} seconds")
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)
