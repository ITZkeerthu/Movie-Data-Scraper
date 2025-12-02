import os
import glob
from sqlalchemy import create_engine

MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'migrations')


def run_migrations():
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print('DATABASE_URL not set in environment')
        return

    engine = create_engine(db_url)
    sql_files = sorted(glob.glob(os.path.join(MIGRATIONS_DIR, '*.sql')))
    if not sql_files:
        print('No migration files found in', MIGRATIONS_DIR)
        return

    with engine.begin() as conn:
        for path in sql_files:
            print('Applying', path)
            with open(path, 'r', encoding='utf-8') as fh:
                sql = fh.read()
                # Use driver-level execution for raw SQL scripts
                conn.exec_driver_sql(sql)


if __name__ == '__main__':
    run_migrations()
