import psycopg2
from pgvector.psycopg2 import register_vector
from config.settings import Settings
from dotenv import load_dotenv
import logging
from pathlib import Path


logger = logging.getLogger(__name__)

load_dotenv()

def get_db_connection():
    """
    Establishes and returns a connection to the PostgreSQL database.
    Registers the pgvector extension on the connection.
    """
    try:
        logger.info("Connecting to PostgreSQL database")
        conn = psycopg2.connect(
            Settings().DATABASE_URL
        )


        logger.info("Connected to PostgreSQL database")
        return conn
    except psycopg2.Error as e:
        logger.error(f"Error connecting to PostgreSQL database: {e}")
        raise


def init_db():
    """
    Reads the pure SQL file and executes it to initialize the database.
    """

    conn = get_db_connection()

    # 1. Dynamically find the path to the SQL file
    # go to root directory and then to src/sql/init_db.sql

    current_dir = Path(__file__).parent.parent
    sql_file_path = current_dir / "src" / "sql" / "init_db.sql"

    # 2. Read the SQL queries directly from the file
    try:
        logger.info("Initializing database schema from init_db.sql")
        sql_queries = sql_file_path.read_text()
    except FileNotFoundError:
        logger.error(f"SQL file not found at: {sql_file_path}")
        raise

    # 3. Execute the queries
    try:
        logger.info("Running the queries from init_db.sql")
        with conn.cursor() as cur:
            cur.execute(sql_queries)
        conn.commit()  # Commit the DDL changes
        logger.info("Database schema initialized successfully from init_db.sql.")
        logger.info("Registering pgvector extension")
        register_vector(conn)
        logger.info("pgvector extension registered successfully")
    except Exception as e:
        conn.rollback()
        logger.error(f"Failed to initialize database: {e}")
        raise

def drop_db():
    """
    Reads the pure SQL file and executes it to drop the database.
    """
    conn = get_db_connection()

    current_dir = Path(__file__).parent.parent
    sql_file_path = current_dir / "src" / "sql" / "drop_db.sql"

    try:
        logger.info("Dropping database schema from drop_db.sql")
        sql_queries = sql_file_path.read_text()
    except FileNotFoundError:
        logger.error(f"SQL file not found at: {sql_file_path}")
        raise

    try:
        logger.info("Running the queries from drop_db.sql")
        with conn.cursor() as cur:
            cur.execute(sql_queries)
        conn.commit()  # Commit the DDL changes
        logger.info("Database schema dropped successfully from drop_db.sql.")
    except Exception as e:
        conn.rollback()
        logger.error(f"Failed to drop database: {e}")
        raise

if __name__ == "__main__":
    get_db_connection()
    init_db()
