import os

import duckdb
import pytest
from sqlalchemy import create_engine, text

TABLES = [
    "customers",
    "geolocation",
    "order_items",
    "order_payments",
    "order_reviews",
    "orders",
    "products",
    "sellers",
    "category_translation",
]


def test_duckdb_tables_exist():
    duckdb_path = os.getenv("DUCKDB_PATH", "data/processed/data.duckdb")
    con = duckdb.connect(database=duckdb_path)

    res = set(x[0] for x in con.execute("SHOW TABLES").fetchall())
    for table_name in TABLES:
        assert table_name in res
    con.close()


def test_postgres_tables_not_empty():
    db_url = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432")
    eng = create_engine(db_url)

    with eng.connect() as c:
        for table_name in TABLES:
            n = c.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
            assert n is not None and n > 0
    eng.dispose()
