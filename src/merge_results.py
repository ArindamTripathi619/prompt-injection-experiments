#!/usr/bin/env python3
"""
Merge multiple experiment databases into a single database.
Usage: python3 merge_results.py exp1_results.db exp2_results.db exp3_results.db exp4_results.db exp6_isolated.db exp6_adaptive_l3.db exp6_adaptive_l4.db exp6_full_adaptive.db
"""

import sqlite3
import sys
from pathlib import Path

def ensure_schema_compatibility(dst_conn, src_conn, table_name):
    """Ensure destination table has all columns from source table."""
    src_columns = src_conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    dst_columns = dst_conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    
    src_col_names = {col[1] for col in src_columns}
    dst_col_names = {col[1] for col in dst_columns}
    
    # Add missing columns to destination
    missing_columns = src_col_names - dst_col_names
    for col_name in missing_columns:
        # Get column info from source
        col_info = next(col for col in src_columns if col[1] == col_name)
        col_type = col_info[2]  # type
        not_null = "NOT NULL" if col_info[3] else ""
        default_val = f"DEFAULT {col_info[4]}" if col_info[4] is not None else ""
        
        alter_sql = f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type} {not_null} {default_val}"
        alter_sql = " ".join(alter_sql.split())  # Clean up extra spaces
        dst_conn.execute(alter_sql)

def merge_databases(input_dbs, output_db="experiments.db"):
    """Merge multiple SQLite databases into one."""
    
    print(f"========================================")
    print(f"Merging {len(input_dbs)} databases")
    print(f"========================================")
    
    # Remove output if it exists
    if Path(output_db).exists():
        Path(output_db).unlink()
        print(f"✓ Removed existing {output_db}")
    
    # Create output database with schema from first input
    print(f"\n1. Creating output database: {output_db}")
    first_db = input_dbs[0]
    
    # Copy schema from first database
    with sqlite3.connect(first_db) as src, sqlite3.connect(output_db) as dst:
        # Get schema (excluding sqlite_sequence which is auto-created)
        schema = src.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'"
        ).fetchall()
        for sql_statement in schema:
            if sql_statement[0]:
                dst.execute(sql_statement[0])
        dst.commit()
    
    print(f"✓ Schema created from {first_db}")
    
    # Merge data from all databases
    print(f"\n2. Merging data from {len(input_dbs)} databases...")
    
    total_traces = 0
    with sqlite3.connect(output_db) as dst:
        for i, db_path in enumerate(input_dbs, 1):
            print(f"\n   Merging {db_path}...")
            
            with sqlite3.connect(db_path) as src:
                # Get table names (exclude sqlite_sequence)
                tables = src.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'"
                ).fetchall()
                
                for (table_name,) in tables:
                    # Ensure schema compatibility
                    ensure_schema_compatibility(dst, src, table_name)
                    
                    # Get data from source
                    rows = src.execute(f"SELECT * FROM {table_name}").fetchall()
                    
                    if not rows:
                        continue
                    
                    # Get column info to check for id column
                    col_info = src.execute(f"PRAGMA table_info({table_name})").fetchall()
                    col_names = [col[1] for col in col_info]
                    has_id = 'id' in col_names
                    
                    # If table has id column, insert without id and let autoincrement handle it
                    if has_id:
                        # Get columns except id
                        non_id_cols = [col for col in col_names if col != 'id']
                        id_index = col_names.index('id')
                        
                        # Create rows without id column
                        rows_without_id = [tuple(row[j] for j in range(len(row)) if j != id_index) for row in rows]
                        placeholders = ','.join(['?'] * len(non_id_cols))
                        col_str = ','.join(non_id_cols)
                        
                        dst.executemany(
                            f"INSERT INTO {table_name} ({col_str}) VALUES ({placeholders})",
                            rows_without_id
                        )
                    else:
                        # Insert all columns as-is
                        col_count = len(rows[0])
                        placeholders = ','.join(['?'] * col_count)
                        dst.executemany(
                            f"INSERT INTO {table_name} VALUES ({placeholders})",
                            rows
                        )
                    
                    if table_name == 'execution_traces':
                        trace_count = len(rows)
                        total_traces += trace_count
                        print(f"     ✓ {table_name}: {trace_count} traces")
                    else:
                        print(f"     ✓ {table_name}: {len(rows)} rows")
        
        dst.commit()
    
    print(f"\n========================================")
    print(f"Merge Complete!")
    print(f"========================================")
    print(f"Output: {output_db}")
    print(f"Total traces: {total_traces}")
    print(f"Expected: 7,290 traces")
    
    if total_traces == 7290:
        print(f"✅ SUCCESS: All traces collected!")
    elif total_traces > 7000:
        print(f"⚠️  WARNING: Close to expected ({total_traces}/8830)")
    else:
        print(f"❌ ERROR: Missing traces ({total_traces}/8830)")
    
    print(f"\nNext step: Run statistical analysis")
    print(f"  cd /home/DevCrewX/Projects/ResearchPaper/prompt-injection-experiments")
    print(f"  python3 src/statistical_analysis.py")
    print(f"========================================")
    
    return output_db

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 merge_results.py <db1> <db2> [db3] [db4] ...")
        print("Example: python3 merge_results.py exp1_results.db exp2_results.db exp3_results.db exp4_results.db exp6_isolated.db exp6_adaptive_l3.db exp6_adaptive_l4.db exp6_full_adaptive.db")
        sys.exit(1)
    
    input_dbs = sys.argv[1:]
    
    # Verify all input databases exist
    missing = []
    for db in input_dbs:
        if not Path(db).exists():
            missing.append(db)
    
    if missing:
        print(f"❌ ERROR: Missing databases:")
        for db in missing:
            print(f"   - {db}")
        sys.exit(1)
    
    # Merge databases
    output_db = merge_databases(input_dbs)
    
    print(f"\n✓ Merge script completed successfully")

if __name__ == "__main__":
    main()