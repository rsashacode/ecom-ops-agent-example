import os
import tomllib
from pathlib import Path

import duckdb
import pandas as pd
from dotenv import load_dotenv
from prefect import flow, get_run_logger, task
from sqlalchemy import create_engine, text

from pipelines._manifest import FILES
from pipelines.download_data import download_all
from pipelines.schemas import PANDAS_DATE_COLS, PANDAS_DTYPES, PG_DDL

load_dotenv()


def load_cfg():
    with open("configs/settings.toml", "rb") as f:
        return tomllib.load(f)


def read_csv(path: str, table: str) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=PANDAS_DTYPES[table], encoding="utf-8", low_memory=True)

    for c in PANDAS_DATE_COLS.get(table, []):
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce", utc=True)

    return df


@task
def t_download() -> dict[str, str]:
    logger = get_run_logger()
    logger.info("Downloading raw files ...")
    saved = download_all()
    logger.info("Downloaded %d files.", len(saved))
    return saved


@task
def t_duckdb_load(files: dict[str, str]) -> str:
    logger = get_run_logger()
    cfg = load_cfg()
    duck_path = Path(os.getenv("DUCKDB_PATH", cfg["data"]["processed_dir"] + "/olist.duckdb"))
    duck_path.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(duck_path))
    for filename, table in FILES:
        logger.info("Loading %s into DuckDB table %s", filename, table)
        df = read_csv(files[filename], table)

        con.execute(f"CREATE TABLE IF NOT EXISTS {table} AS SELECT * FROM df LIMIT 0;")
        con.register("df", df)

        con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM df;")
        con.unregister("df")

    con.close()
    logger.info("DuckDB file at %s", duck_path)
    return str(duck_path)


@task
def t_postgres_load(files: dict[str, str]) -> str:
    logger = get_run_logger()
    db_url = os.getenv("DATABASE_URL", "postgresql+psycopg2://ecom:ecom@localhost:5432/ecom")
    engine = create_engine(db_url, future=True)

    with engine.begin() as conn:
        for filename, table in FILES:
            logger.info("Creating Postgres table %s", table)
            ddl = PG_DDL[table]
            conn.execute(text(ddl))

            logger.info("Loading %s into Postgres table %s", filename, table)
            df = read_csv(files[filename], table)
            conn.execute(text(f"TRUNCATE TABLE {table} CASCADE;"))
            df.to_sql(
                table, con=conn, if_exists="append", index=False, method="multi", chunksize=10000
            )

    engine.dispose()
    return db_url


@flow(name="Ingest Olist into DuckDB and Postgres")
def ingest_flow():
    files = t_download()
    duckdb_path = t_duckdb_load(files)
    pg_url = t_postgres_load(files)
    return {"duckdb": duckdb_path, "postgres": pg_url}


if __name__ == "__main__":
    ingest_flow()
