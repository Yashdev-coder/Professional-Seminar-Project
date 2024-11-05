import psycopg2
from datetime import datetime

class AttendanceManager:
    def __init__(self, db_name, user, password, host='localhost', port='5432'):
        try:
            self.conn = psycopg2.connect(
                dbname=db_name,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cursor = self.conn.cursor()
            self._create_table_if_not_exists()
        except Exception as e:
            print(f"Error connecting to PostgreSQL database: {e}")

    def _create_table_if_not_exists(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS attendance (
            id SERIAL PRIMARY KEY,
            student_id VARCHAR(50) NOT NULL,
            timestamp TIMESTAMP NOT NULL
        );
        '''
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def mark_attendance(self, student_id):
        try:
            timestamp = datetime.now()
            insert_query = '''
            INSERT INTO attendance (student_id, timestamp) VALUES (%s, %s);
            '''
            self.cursor.execute(insert_query, (student_id, timestamp))
            self.conn.commit()
            print(f"Attendance marked for student ID: {student_id}")
        except Exception as e:
            print(f"Error marking attendance: {e}")

    def get_attendance(self, student_id=None):
        try:
            if student_id:
                select_query = '''
                SELECT * FROM attendance WHERE student_id = %s;
                '''
                self.cursor.execute(select_query, (student_id,))
            else:
                select_query = '''
                SELECT * FROM attendance;
                '''
                self.cursor.execute(select_query)

            records = self.cursor.fetchall()
            for record in records:
                print(f"ID: {record[0]}, Student ID: {record[1]}, Timestamp: {record[2]}")
        except Exception as e:
            print(f"Error fetching attendance records: {e}")

    def delete_attendance(self, student_id):
        try:
            delete_query = '''
            DELETE FROM attendance WHERE student_id = %s;
            '''
            self.cursor.execute(delete_query, (student_id,))
            self.conn.commit()
            print(f"Attendance records deleted for student ID: {student_id}")
        except Exception as e:
            print(f"Error deleting attendance: {e}")

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    db_name = "attendance_db"
    user = "postgres"
    password = "your_password"
    
    manager = AttendanceManager(db_name, user, password)
    
    # Example usage
    manager.mark_attendance("student_123")
    manager.get_attendance()
    manager.delete_attendance("student_123")
    manager.close_connection()
