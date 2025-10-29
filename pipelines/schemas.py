from typing import Any

PG_DDL = {
    # Parents
    "geolocation": """
CREATE TABLE IF NOT EXISTS geolocation (
    geolocation_zip_code_prefix     INT,
    geolocation_lat                 NUMERIC,
    geolocation_lng                 NUMERIC,
    geolocation_city                TEXT,
    geolocation_state               TEXT
);""",
    "customers": """
CREATE TABLE IF NOT EXISTS customers (
    customer_id                     TEXT PRIMARY KEY,
    customer_unique_id              TEXT,
    customer_zip_code_prefix        INT,
    customer_city                   TEXT,
    customer_state                  TEXT
);""",
    "products": """
CREATE TABLE IF NOT EXISTS products (
    product_id                      TEXT PRIMARY KEY,
    product_category_name           TEXT,
    product_name_lenght             INT,
    product_description_lenght      INT,
    product_photos_qty              INT,
    product_weight_g                INT,
    product_length_cm               INT,
    product_height_cm               INT,
    product_width_cm                INT
);""",
    "category_translation": """
CREATE TABLE IF NOT EXISTS category_translation (
    product_category_name           TEXT PRIMARY KEY,
    product_category_name_english   TEXT
);""",
    # Parents & Children
    "orders": """
CREATE TABLE IF NOT EXISTS orders (
    order_id                        TEXT PRIMARY KEY,
    customer_id                     TEXT,
    order_status                    TEXT,
    order_purchase_timestamp        TIMESTAMP,
    order_approved_at               TIMESTAMP,
    order_delivered_carrier_date    TIMESTAMP,
    order_delivered_customer_date   TIMESTAMP,
    order_estimated_delivery_date   TIMESTAMP,

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);""",
    # Children
    "sellers": """
CREATE TABLE IF NOT EXISTS sellers (
    seller_id                       TEXT PRIMARY KEY,
    seller_zip_code_prefix          INT,
    seller_city                     TEXT,
    seller_state                    TEXT
);""",
    "order_items": """
CREATE TABLE IF NOT EXISTS order_items (
    order_id                        TEXT,
    order_item_id                   INT,
    product_id                      TEXT,
    seller_id                       TEXT,
    shipping_limit_date             TIMESTAMP,
    price                           NUMERIC,
    freight_value                   NUMERIC,

    PRIMARY KEY (order_id, order_item_id),
    CONSTRAINT fk_items_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
    CONSTRAINT fk_items_product
        FOREIGN KEY (product_id) REFERENCES products(product_id),
    CONSTRAINT fk_items_seller
        FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);""",
    "order_payments": """
CREATE TABLE IF NOT EXISTS order_payments (
    order_id                        TEXT,
    payment_sequential              INT,
    payment_type                    TEXT,
    payment_installments            INT,
    payment_value                   NUMERIC,

    PRIMARY KEY (order_id, payment_sequential),
    CONSTRAINT fk_payments_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
);""",
    "order_reviews": """
CREATE TABLE IF NOT EXISTS order_reviews (
    review_id                       TEXT,
    order_id                        TEXT,
    review_score                    INT,
    review_comment_title            TEXT,
    review_comment_message          TEXT,
    review_creation_date            TIMESTAMP,
    review_answer_timestamp         TIMESTAMP,

    PRIMARY KEY (review_id, order_id),
    CONSTRAINT fk_reviews_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
);""",
}

PANDAS_DTYPES: dict[str, Any] = {
    "geolocation": {
        "geolocation_zip_code_prefix": "UInt16",
        "geolocation_lat": "Float32",
        "geolocation_lng": "Float32",
        "geolocation_city": "string",
        "geolocation_state": "string",
    },
    "customers": {
        "customer_id": "string",
        "customer_unique_id": "string",
        "customer_zip_code_prefix": "string",
        "customer_city": "string",
        "customer_state": "string",
    },
    "products": {
        "product_id": "string",
        "product_category_name": "string",
        "product_name_lenght": "UInt16",
        "product_description_lenght": "UInt16",
        "product_photos_qty": "UInt16",
        "product_weight_g": "UInt16",
        "product_length_cm": "UInt16",
        "product_height_cm": "UInt16",
        "product_width_cm": "UInt16",
    },
    "category_translation": {
        "product_category_name": "string",
        "product_category_name_english": "string",
    },
    "orders": {
        "order_id": "string",
        "customer_id": "string",
        "order_status": "string",
        # "order_purchase_timestamp": "datetime64[ns]",
        # "order_approved_at": "datetime64[ns]",
        # "order_delivered_carrier_date": "datetime64[ns]",
        # "order_delivered_customer_date": "datetime64[ns]",
        # "order_estimated_delivery_date": "datetime64[ns]",
    },
    "sellers": {
        "seller_id": "string",
        "seller_zip_code_prefix": "Int32",
        "seller_city": "string",
        "seller_state": "string",
    },
    "order_items": {
        "order_id": "string",
        "order_item_id": "UInt32",
        "product_id": "string",
        "seller_id": "string",
        # "shipping_limit_date": "datetime64[ns]",
        "price": "Float32",
        "freight_value": "Float32",
    },
    "order_payments": {
        "order_id": "string",
        "payment_sequential": "UInt16",
        "payment_type": "string",
        "payment_installments": "UInt16",
        "payment_value": "Float32",
    },
    "order_reviews": {
        "review_id": "string",
        "order_id": "string",
        "review_score": "UInt16",
        "review_comment_title": "string",
        "review_comment_message": "string",
        # "review_creation_date": "datetime64[ns]",
        # "review_answer_timestamp": "datetime64[ns]",
    },
}


PANDAS_DATE_COLS = {
    "order_items": ["shipping_limit_date"],
    "order_reviews": ["review_creation_date", "review_answer_timestamp"],
    "orders": [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
}
