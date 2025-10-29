# (filename, table_name). Reordering would break constraints creation on table create
FILES = (
    ("olist_geolocation_dataset.csv", "geolocation"),
    ("olist_customers_dataset.csv", "customers"),
    ("olist_products_dataset.csv", "products"),
    ("product_category_name_translation.csv", "category_translation"),
    ("olist_orders_dataset.csv", "orders"),
    ("olist_sellers_dataset.csv", "sellers"),
    ("olist_order_items_dataset.csv", "order_items"),
    ("olist_order_payments_dataset.csv", "order_payments"),
    ("olist_order_reviews_dataset.csv", "order_reviews"),
)
