import psycopg2
import time
import sys

def run_cycle():
    # Database connection settings
    # Although you mentioned "no specific DB," the PostgreSQL protocol 
    # requires a connection to a database.
    # The default administrative database name is usually 'postgres'.
    db_config = {
        "host": "postgres",
        "port": "5432",
        "user": "postgres",
        "password": "",    # Set password as an empty string or None
        "dbname": "postgres" 
    }

    try:
        while True:
            print("--- Starting a new cycle ---")

            # 1. Connect to PostgreSQL
            print("1. Connecting to the database...")
            conn = psycopg2.connect(**db_config)
            # Set autocommit to True to ensure create/drop actions take effect immediately
            conn.autocommit = True 
            cursor = conn.cursor()
            print("   Connection successful")

            # 2. Sleep for 10 seconds
            print("2. Waiting for 10 seconds...")
            time.sleep(10)

            # 3. Create a table
            table_name = "test_loop_table"
            print(f"3. Creating Table: {table_name}")
            create_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(create_query)

            # 4. Sleep for 10 seconds
            print("4. Waiting for 10 seconds...")
            time.sleep(10)

            # 5. Drop the table
            print(f"5. Dropping Table: {table_name}")
            drop_query = f"DROP TABLE IF EXISTS {table_name};"
            cursor.execute(drop_query)

            # 6. Sleep for 10 seconds
            print("6. Waiting for 10 seconds...")
            time.sleep(10)

            # Close connection (preparing for reconnection in the next cycle)
            cursor.close()
            conn.close()
            print("   Connection closed")

            # 7. Repeat all actions (The while loop will automatically return to the start)

    except psycopg2.OperationalError as e:
        print(f"Connection error: {e}")
        print("Retrying in 5 seconds...")
        time.sleep(5)
        run_cycle() # Recursive retry or re-enter loop
    except KeyboardInterrupt:
        print("\nProgram stopped manually")
        if 'conn' in locals() and conn:
            conn.close()
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_cycle()