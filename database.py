import mysql.connector
from mysql.connector import Error
import os

class Database:
    def __init__(self):
        """
        Connect to the database using environment variables or default values.
        """
        self.host = os.getenv("DB_HOST", "db")
        self.port = int(os.getenv("DB_PORT", 3306))
        self.user = os.getenv("DB_USER", "mercury-user")
        self.password = os.getenv("DB_PASS", "mercury-password")
        self.database = os.getenv("DB_NAME", "mercury-database")

        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor(buffered=True)
            print("[Database] Connected successfully.")
        except Error as e:
            print(f"[Database] Error: {e}")
            raise

    def add_member(self, user_id, username=None, first_name=None, last_name=None):
        """
        Add a new member or check existence by ID.
        Only updates username, first_name, and last_name if they are empty.
        """
        sql = """
        INSERT INTO members (id, username, first_name, last_name)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            username = COALESCE(username, VALUES(username)),
            first_name = COALESCE(first_name, VALUES(first_name)),
            last_name = COALESCE(last_name, VALUES(last_name))
        """
        self.cursor.execute(sql, (user_id, username, first_name, last_name))
        self.connection.commit()

    def del_member(self, user_id):
        sql = "DELETE FROM members WHERE id = %s"
        self.cursor.execute(sql, (user_id,))
        self.connection.commit()

    def increment_messages(self, user_id):
        """
        Increment the message count for a member.
        """
        sql = "UPDATE members SET messages_count = messages_count + 1 WHERE id = %s"
        self.cursor.execute(sql, (user_id,))
        self.connection.commit()

    def add_warning(self, user_id):
        """
        Increment the warning count for a member.
        """
        sql = "UPDATE members SET warnings = warnings + 1 WHERE id = %s"
        self.cursor.execute(sql, (user_id,))
        self.connection.commit()

    def get_warning(self, user_id):
        """
        Get the number of warnings for a user by their Telegram user_id.
        Returns the number of warnings or 0 if user not found.
        """
        sql = "SELECT warnings FROM members WHERE id = %s"
        self.cursor.execute(sql, (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def get_member(self, user_id):
        """
        Retrieve member information by user ID.
        """
        sql = "SELECT * FROM members WHERE id = %s"
        self.cursor.execute(sql, (user_id,))
        return self.cursor.fetchone()

    def check_or_add_member(self, user_id, username=None, first_name=None, last_name=None):
        """
        Check if a member exists by user_id.
        If not, add a new member with the given username, first_name, last_name.
        Returns the member record.
        """
        # Try to get the member first
        self.cursor.execute("SELECT * FROM members WHERE id = %s", (user_id,))
        member = self.cursor.fetchone()

        if member is None:
            # Member does not exist → insert a new one
            sql = """
                  INSERT INTO members (id, username, first_name, last_name)
                  VALUES (%s, %s, %s, %s) \
                  """
            self.cursor.execute(sql, (user_id, username, first_name, last_name))
            self.connection.commit()

            # Fetch again to return
            self.cursor.execute("SELECT * FROM members WHERE id = %s", (user_id,))
            member = self.cursor.fetchone()

        return member

    def close(self):
        """
        Close the database connection.
        """
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("[Database] Connection closed.")
