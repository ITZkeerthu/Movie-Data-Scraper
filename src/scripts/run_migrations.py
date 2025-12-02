import os
import glob
from sqlalchemy import create_engine
from ..config.settings import settings

MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'migrations')


def run_migrations():
    engine = create_engine(settings.DATABASE_URL)
    sql_files = sorted(glob.glob(os.path.join(MIGRATIONS_DIR, '*.sql')))
    if not sql_files:
        print('No migration files found in', MIGRATIONS_DIR)
        return

    with engine.begin() as conn:
        for path in sql_files:
            print('Applying', path)
            with open(path, 'r', encoding='utf-8') as fh:
                sql = fh.read()
                conn.execute(sql)


if __name__ == '__main__':
    run_migrations()
