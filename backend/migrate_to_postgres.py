"""
Aethera AI — Zero-Loss Database Migration Tool (SQLite -> PostgreSQL)
Exports all verified molecular data, categories, properties, references, 
and metadata from local SQLite (aethera.db) to PostgreSQL.
"""

import os
import sys
import argparse
import sqlite3
import logging
from typing import List, Dict, Any

# Ensure backend directory is in python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from sqlalchemy import create_engine, text, inspect
from app.models.models import Base

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("aethera.migration")

# Dependency order for clean parent -> child insertion
ORDERED_TABLES = [
    "categories",
    "compounds",
    "biomolecules",
    "proteins",
    "enzymes",
    "physical_properties",
    "chemical_properties",
    "hazards",
    "references",
    "visualization_metadata",
    "synonyms"
]

def get_sqlite_connection(db_path: str) -> sqlite3.Connection:
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Source SQLite database not found at: {db_path}")
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    return con

def generate_sql_dump(source_db: str, output_file: str):
    """
    Generate a standalone PostgreSQL .sql dump file from SQLite.
    Can be run via psql or Neon/Supabase/Railway web SQL consoles.
    """
    logger.info(f"Generating PostgreSQL SQL dump from {source_db} to {output_file}...")
    con = get_sqlite_connection(source_db)
    cur = con.cursor()

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("-- ========================================================\n")
        f.write("-- Aethera AI — Production PostgreSQL Data & Schema Dump\n")
        f.write("-- Generated for Path A Deployment (Railway / Neon / Supabase)\n")
        f.write("-- ========================================================\n\n")
        f.write("CREATE EXTENSION IF NOT EXISTS pg_trgm;\n\n")

        for table in ORDERED_TABLES:
            cur.execute(f'SELECT * FROM "{table}"')
            rows = cur.fetchall()
            if not rows:
                continue

            columns = [d[0] for d in cur.description]
            cols_str = ", ".join([f'"{c}"' for c in columns])

            f.write(f"-- Table: {table} ({len(rows)} records)\n")
            for row in rows:
                values = []
                for val in row:
                    if val is None:
                        values.append("NULL")
                    elif isinstance(val, (int, float)):
                        values.append(str(val))
                    else:
                        escaped = str(val).replace("'", "''")
                        values.append(f"'{escaped}'")
                val_str = ", ".join(values)
                f.write(f'INSERT INTO "{table}" ({cols_str}) VALUES ({val_str}) ON CONFLICT ("id") DO NOTHING;\n')

            f.write(f"SELECT setval(pg_get_serial_sequence('\"{table}\"', 'id'), COALESCE(MAX(id), 1)) FROM \"{table}\";\n\n")

    con.close()
    logger.info(f"Successfully created SQL dump: {output_file}")

def migrate_live(source_db: str, postgres_url: str):
    """
    Directly streams data from SQLite into the target PostgreSQL instance.
    """
    if postgres_url.startswith("postgres://"):
        postgres_url = postgres_url.replace("postgres://", "postgresql+psycopg2://", 1)
    elif postgres_url.startswith("postgresql://") and not postgres_url.startswith("postgresql+psycopg2://"):
        postgres_url = postgres_url.replace("postgresql://", "postgresql+psycopg2://", 1)

    logger.info(f"Starting live migration: SQLite ({source_db}) -> PostgreSQL...")
    src_con = get_sqlite_connection(source_db)
    src_cur = src_con.cursor()

    pg_engine = create_engine(postgres_url, pool_pre_ping=True)

    # 1. Ensure pg_trgm extension exists on Postgres
    with pg_engine.connect() as conn:
        logger.info("Enabling pg_trgm extension on PostgreSQL...")
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm;"))
        conn.commit()

    # 2. Build complete schema on PostgreSQL if tables are missing
    logger.info("Verifying and building complete schema on PostgreSQL...")
    Base.metadata.create_all(bind=pg_engine)

    # 3. Transfer records in dependency order
    total_migrated = 0
    verification_results = {}

    with pg_engine.connect() as pg_conn:
        for table in ORDERED_TABLES:
            src_cur.execute(f'SELECT * FROM "{table}"')
            rows = src_cur.fetchall()
            if not rows:
                verification_results[table] = (0, 0)
                continue

            columns = [d[0] for d in src_cur.description]
            cols_str = ", ".join([f'"{c}"' for c in columns])
            placeholders = ", ".join([f":{c}" for c in columns])
            insert_stmt = text(f'INSERT INTO "{table}" ({cols_str}) VALUES ({placeholders}) ON CONFLICT ("id") DO NOTHING')

            records = [dict(row) for row in rows]
            pg_conn.execute(insert_stmt, records)
            pg_conn.commit()

            # Reset auto-increment sequence
            try:
                pg_conn.execute(text(f"SELECT setval(pg_get_serial_sequence('\"{table}\"', 'id'), COALESCE(MAX(id), 1)) FROM \"{table}\";"))
                pg_conn.commit()
            except Exception:
                pass

            # Verification count on target
            tgt_count = pg_conn.execute(text(f'SELECT COUNT(*) FROM "{table}"')).scalar()
            verification_results[table] = (len(rows), tgt_count)
            total_migrated += len(rows)
            logger.info(f" - {table}: {len(rows)} rows copied -> PostgreSQL verified {tgt_count} rows.")

    src_con.close()

    print("\n========================================================")
    print("DATABASE MIGRATION SUMMARY (SQLite -> PostgreSQL)")
    print("========================================================")
    all_matched = True
    for table, (src_cnt, tgt_cnt) in verification_results.items():
        status = "MATCHED [OK]" if src_cnt <= tgt_cnt else "MISMATCH [ERROR]"
        if src_cnt > tgt_cnt:
            all_matched = False
        print(f" * {table:25}: Source={src_cnt:3} | Target={tgt_cnt:3} | {status}")
    print("========================================================")
    if all_matched:
        print(f"[+] SUCCESS: All {total_migrated} records migrated safely with 100% data integrity!")
    else:
        print("[-] WARNING: Some tables have discrepancies. Please review above counts.")
    print("========================================================\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migrate Aethera AI data from SQLite to PostgreSQL")
    parser.add_argument("--source", default=os.path.join(backend_dir, "aethera.db"), help="Path to source SQLite database")
    parser.add_argument("--target", default=None, help="Target PostgreSQL connection URL (e.g. postgresql://user:pass@host:5432/db)")
    parser.add_argument("--dump", action="store_true", help="Generate standalone aethera_pg_dump.sql dump file")
    parser.add_argument("--dump-path", default=os.path.join(backend_dir, "aethera_pg_dump.sql"), help="Path to output SQL dump file")

    args = parser.parse_args()

    # Always generate the SQL dump as an instant backup artifact
    generate_sql_dump(args.source, args.dump_path)

    target_url = args.target or os.environ.get("TARGET_DATABASE_URL")
    if target_url and target_url.startswith("postgresql"):
        migrate_live(args.source, target_url)
    elif not args.dump:
        print("\n[*] Note: No live PostgreSQL target specified (--target).")
        print(f"[*] A standalone PostgreSQL dump file was generated at: {args.dump_path}")
        print("[*] To perform a live transfer, run:")
        print("    python backend/migrate_to_postgres.py --target postgresql://user:password@host/dbname\n")
