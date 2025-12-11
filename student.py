import mysql.connector
from mysql.connector import Error
import sys
import getpass

class StudentManagementSystem:
    def __init__(self, host, database, user, password):
        """
        Initialize the Student Management System with database connection parameters.
        
        Args:
            host: MySQL server hostname
            database: Database name
            user: MySQL username
            password: MySQL password
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        
    def connect(self):
        """
        Establish a connection to the MySQL database.
        Handles connection errors gracefully.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                auth_plugin='mysql_native_password'  # Added for MySQL 8.0+
            )
            
            if self.connection.is_connected():
                print("✓ Successfully connected to MySQL database")
                self.create_table_if_not_exists()
                return True
                
        except Error as e:
            print(f"✗ Error connecting to MySQL: {e}")
            print("\nTroubleshooting tips:")
            print("1. Check if MySQL server is running")
            print("2. Verify username and password")
            print("3. Check if database exists: Run 'CREATE DATABASE student_db;' in MySQL")
            print("4. Try using 'root' as username with empty password")
            return False
    
    def create_table_if_not_exists(self):
        """
        Create the students table if it doesn't exist.
        This ensures the required table structure is in place.
        """
        create_table_query = """
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INT NOT NULL,
            class VARCHAR(50) NOT NULL,
            marks DECIMAL(5,2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_query)
            self.connection.commit()
            print("✓ Students table is ready")
        except Error as e:
            print(f"✗ Error creating table: {e}")
        finally:
            if cursor:
                cursor.close()
    
    def add_student(self, name, age, class_name, marks):
        """
        Add a new student to the database.
        
        Args:
            name: Student's full name
            age: Student's age
            class_name: Student's class/grade
            marks: Student's marks (decimal)
            
        Returns:
            The ID of the newly inserted student
        """
        insert_query = """
        INSERT INTO students (name, age, class, marks)
        VALUES (%s, %s, %s, %s)
        """
        
        student_data = (name, age, class_name, marks)
        cursor = None
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(insert_query, student_data)
            self.connection.commit()
            student_id = cursor.lastrowid
            print(f"✓ Student added successfully with ID: {student_id}")
            return student_id
        except Error as e:
            print(f"✗ Error adding student: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def update_student(self, student_id, name=None, age=None, class_name=None, marks=None):
        """
        Update student information. Only provided fields will be updated.
        
        Args:
            student_id: ID of the student to update
            name: New name (optional)
            age: New age (optional)
            class_name: New class (optional)
            marks: New marks (optional)
            
        Returns:
            Number of rows affected
        """
        # Build dynamic update query based on provided parameters
        update_fields = []
        values = []
        
        if name:
            update_fields.append("name = %s")
            values.append(name)
        if age is not None:
            update_fields.append("age = %s")
            values.append(age)
        if class_name:
            update_fields.append("class = %s")
            values.append(class_name)
        if marks is not None:
            update_fields.append("marks = %s")
            values.append(marks)
        
        # If no fields to update, return early
        if not update_fields:
            print("ℹ No fields provided for update")
            return 0
        
        # Add student_id to values
        values.append(student_id)
        
        # Create the update query
        update_query = f"""
        UPDATE students 
        SET {', '.join(update_fields)}
        WHERE id = %s
        """
        
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(update_query, values)
            self.connection.commit()
            rows_affected = cursor.rowcount
            
            if rows_affected > 0:
                print(f"✓ Student with ID {student_id} updated successfully")
            else:
                print(f"⚠ No student found with ID {student_id}")
                
            return rows_affected
        except Error as e:
            print(f"✗ Error updating student: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()
    
    def delete_student(self, student_id):
        """
        Delete a student from the database.
        
        Args:
            student_id: ID of the student to delete
            
        Returns:
            Number of rows affected
        """
        delete_query = "DELETE FROM students WHERE id = %s"
        
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(delete_query, (student_id,))
            self.connection.commit()
            rows_affected = cursor.rowcount
            
            if rows_affected > 0:
                print(f"✓ Student with ID {student_id} deleted successfully")
            else:
                print(f"⚠ No student found with ID {student_id}")
                
            return rows_affected
        except Error as e:
            print(f"✗ Error deleting student: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()
    
    def view_all_students(self):
        """
        Retrieve and display all students from the database.
        
        Returns:
            List of all student records
        """
        select_query = """
        SELECT id, name, age, class, marks, 
               DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') as created_at,
               DATE_FORMAT(updated_at, '%Y-%m-%d %H:%i:%s') as updated_at
        FROM students 
        ORDER BY id
        """
        
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(select_query)
            students = cursor.fetchall()
            
            # Display results in a formatted table
            if students:
                print("\n" + "="*90)
                print(f"{'ID':<5} {'Name':<25} {'Age':<5} {'Class':<15} {'Marks':<10} {'Created':<20}")
                print("="*90)
                
                for student in students:
                    print(f"{student['id']:<5} {student['name']:<25} {student['age']:<5} "
                          f"{student['class']:<15} {student['marks']:<10} {student['created_at']:<20}")
                print("="*90)
                print(f"Total students: {len(students)}")
            else:
                print("ℹ No students found in the database")
                
            return students
        except Error as e:
            print(f"✗ Error retrieving students: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
    
    def search_students(self, search_term=None, student_id=None):
        """
        Search for students by name or ID.
        
        Args:
            search_term: Name or partial name to search for (optional)
            student_id: Specific student ID to search for (optional)
            
        Returns:
            List of matching student records
        """
        cursor = None
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            if student_id:
                # Search by specific ID
                search_query = """
                SELECT id, name, age, class, marks, 
                       DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') as created_at,
                       DATE_FORMAT(updated_at, '%Y-%m-%d %H:%i:%s') as updated_at
                FROM students 
                WHERE id = %s
                """
                cursor.execute(search_query, (student_id,))
            elif search_term:
                # Search by name (partial match)
                search_query = """
                SELECT id, name, age, class, marks, 
                       DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') as created_at,
                       DATE_FORMAT(updated_at, '%Y-%m-%d %H:%i:%s') as updated_at
                FROM students 
                WHERE name LIKE %s
                ORDER BY name
                """
                cursor.execute(search_query, (f"%{search_term}%",))
            else:
                print("ℹ Please provide either a search term or student ID")
                return []
            
            students = cursor.fetchall()
            
            # Display results
            if students:
                print("\n" + "="*90)
                print(f"{'ID':<5} {'Name':<25} {'Age':<5} {'Class':<15} {'Marks':<10} {'Updated':<20}")
                print("="*90)
                
                for student in students:
                    print(f"{student['id']:<5} {student['name']:<25} {student['age']:<5} "
                          f"{student['class']:<15} {student['marks']:<10} {student['updated_at']:<20}")
                print("="*90)
                print(f"Found {len(students)} matching student(s)")
            else:
                if student_id:
                    print(f"⚠ No student found with ID {student_id}")
                else:
                    print(f"⚠ No students found matching '{search_term}'")
                    
            return students
        except Error as e:
            print(f"✗ Error searching students: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
    
    def get_student_count(self):
        """
        Get the total number of students in the database.
        
        Returns:
            Total student count
        """
        count_query = "SELECT COUNT(*) as total FROM students"
        
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(count_query)
            result = cursor.fetchone()
            return result['total'] if result else 0
        except Error as e:
            print(f"✗ Error getting student count: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()
    
    def close_connection(self):
        """
        Close the database connection.
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ Database connection closed")

def display_menu():
    """
    Display the main menu for the Student Management System.
    """
    print("\n" + "="*60)
    print("📚 STUDENT MANAGEMENT SYSTEM")
    print("="*60)
    print("1. ➕ Add New Student")
    print("2. ✏️  Update Student Information")
    print("3. ❌ Delete Student")
    print("4. 👥 View All Students")
    print("5. 🔍 Search Student by Name")
    print("6. 🔎 Search Student by ID")
    print("7. 📊 Display Student Count")
    print("8. 🚪 Exit")
    print("="*60)

def get_student_input():
    """
    Get student details from user input.
    
    Returns:
        Tuple of (name, age, class_name, marks)
    """
    print("\n📝 Enter Student Details:")
    name = input("Name: ").strip()
    if not name:
        print("⚠ Name cannot be empty!")
        return None
    
    while True:
        try:
            age = int(input("Age: "))
            if age < 5 or age > 25:
                print("⚠ Please enter a valid age (5-25)")
                continue
            break
        except ValueError:
            print("⚠ Please enter a valid number for age")
    
    class_name = input("Class: ").strip()
    if not class_name:
        print("⚠ Class cannot be empty!")
        return None
    
    while True:
        try:
            marks = float(input("Marks (0-100): "))
            if marks < 0 or marks > 100:
                print("⚠ Please enter marks between 0 and 100")
                continue
            break
        except ValueError:
            print("⚠ Please enter a valid number for marks")
    
    return name, age, class_name, marks

def setup_database():
    """
    Interactive database setup with multiple connection attempts.
    """
    print("\n" + "="*60)
    print("🔧 DATABASE SETUP")
    print("="*60)
    
    # Try common configurations
    configs = [
        # Most common - root with no password
        {'host': 'localhost', 'database': 'student_db', 'user': 'root', 'password': ''},
        # Root with password 'root'
        {'host': 'localhost', 'database': 'student_db', 'user': 'root', 'password': 'root'},
        # Local MySQL with default credentials
        {'host': '127.0.0.1', 'database': 'student_db', 'user': 'root', 'password': ''},
    ]
    
    print("\nAttempting to connect with common configurations...")
    
    for config in configs:
        print(f"\nTrying: {config['user']}@{config['host']} (password: {'*' * len(config['password']) if config['password'] else 'none'})")
        
        sms = StudentManagementSystem(**config)
        if sms.connect():
            return sms
        
        # Try to create database if it doesn't exist
        try:
            temp_conn = mysql.connector.connect(
                host=config['host'],
                user=config['user'],
                password=config['password']
            )
            cursor = temp_conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS student_db")
            print("✓ Created database 'student_db'")
            cursor.close()
            temp_conn.close()
            
            # Try connecting again
            if sms.connect():
                return sms
        except:
            continue
    
    # Manual configuration
    print("\n" + "="*60)
    print("Please enter your MySQL credentials manually:")
    print("="*60)
    
    host = input("Host (default: localhost): ").strip() or "localhost"
    user = input("Username (default: root): ").strip() or "root"
    password = getpass.getpass("Password (press Enter if none): ")
    database = input("Database name (default: student_db): ").strip() or "student_db"
    
    config = {
        'host': host,
        'database': database,
        'user': user,
        'password': password
    }
    
    sms = StudentManagementSystem(**config)
    if sms.connect():
        return sms
    
    # Try without database first, then create it
    print("\n⚠ Could not connect to database. Trying to create it...")
    try:
        temp_conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = temp_conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        print(f"✓ Created database '{database}'")
        cursor.close()
        temp_conn.close()
        
        if sms.connect():
            return sms
    except Error as e:
        print(f"✗ Failed to create database: {e}")
    
    return None

def main():
    """
    Main function to run the Student Management System.
    """
    print("\n" + "="*60)
    print("🎓 WELCOME TO STUDENT MANAGEMENT SYSTEM")
    print("="*60)
    
    # Setup database connection
    sms = setup_database()
    if not sms:
        print("\n❌ Failed to connect to database.")
        print("\n🔧 MANUAL SETUP INSTRUCTIONS:")
        print("1. Open MySQL command line or phpMyAdmin")
        print("2. Run: CREATE DATABASE student_db;")
        print("3. For root with no password, run:")
        print("   ALTER USER 'root'@'localhost' IDENTIFIED BY '';")
        print("4. Try running the program again")
        return
    
    print("\n✅ Database connection established successfully!")
    
    try:
        while True:
            display_menu()
            
            try:
                choice = input("\n👉 Enter your choice (1-8): ").strip()
                
                if choice == '1':
                    # Add new student
                    student_data = get_student_input()
                    if student_data:
                        sms.add_student(*student_data)
                    
                elif choice == '2':
                    # Update student information
                    try:
                        student_id = int(input("Enter student ID to update: "))
                        
                        print("\nEnter new information (leave blank to keep current value):")
                        name = input("Name: ").strip() or None
                        
                        age_input = input("Age: ").strip()
                        age = int(age_input) if age_input else None
                        
                        class_name = input("Class: ").strip() or None
                        
                        marks_input = input("Marks: ").strip()
                        marks = float(marks_input) if marks_input else None
                        
                        if any([name, age is not None, class_name, marks is not None]):
                            sms.update_student(student_id, name, age, class_name, marks)
                        else:
                            print("ℹ No changes provided")
                            
                    except ValueError:
                        print("⚠ Please enter valid numeric values for ID, age, and marks")
                        
                elif choice == '3':
                    # Delete student
                    try:
                        student_id = int(input("Enter student ID to delete: "))
                        confirm = input(f"⚠ Are you sure you want to delete student with ID {student_id}? (yes/no): ").lower()
                        if confirm == 'yes':
                            sms.delete_student(student_id)
                        else:
                            print("❌ Deletion cancelled")
                    except ValueError:
                        print("⚠ Please enter a valid student ID")
                        
                elif choice == '4':
                    # View all students
                    sms.view_all_students()
                    
                elif choice == '5':
                    # Search by name
                    search_term = input("Enter student name or part of name to search: ").strip()
                    if search_term:
                        sms.search_students(search_term=search_term)
                    else:
                        print("⚠ Please enter a search term")
                        
                elif choice == '6':
                    # Search by ID
                    try:
                        student_id = int(input("Enter student ID to search: "))
                        sms.search_students(student_id=student_id)
                    except ValueError:
                        print("⚠ Please enter a valid student ID")
                        
                elif choice == '7':
                    # Display student count
                    count = sms.get_student_count()
                    print(f"\n📊 Total students in database: {count}")
                    
                elif choice == '8':
                    # Exit
                    print("\n👋 Thank you for using Student Management System. Goodbye!")
                    break
                    
                else:
                    print("❌ Invalid choice. Please enter a number between 1 and 8.")
                    
            except KeyboardInterrupt:
                print("\n\n⚠ Program interrupted by user")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                
    finally:
        # Ensure database connection is closed
        sms.close_connection()

if __name__ == "__main__":
    # Check if mysql-connector is installed
    try:
        import mysql.connector
    except ImportError:
        print("\n❌ mysql-connector-python is not installed!")
        print("Install it using: pip install mysql-connector-python")
        sys.exit(1)
    
    main()