import sqlite3

# Initial table setup connection
conn = sqlite3.connect("studentmanagement.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

conn.execute('''CREATE TABLE IF NOT EXISTS user(id INTEGER PRIMARY KEY AUTOINCREMENT,name VARCHAR(30) UNIQUE NOT NULL,password TEXT NOT NULL,role TEXT NOT NULL CHECK(role IN('admin','staff')))''')
conn.execute('''CREATE TABLE IF NOT EXISTS course(id INTEGER PRIMARY KEY AUTOINCREMENT,cname VARCHAR(30) UNIQUE NOT NULL)''')
conn.execute('''CREATE TABLE IF NOT EXISTS student(id INTEGER PRIMARY KEY AUTOINCREMENT,sname VARCHAR(30) NOT NULL,email TEXT UNIQUE NOT NULL,course_id INTEGER NOT NULL,FOREIGN KEY(course_id) REFERENCES course(id))''')
conn.commit()
conn.close()


def sub(role):
    while True:
        print(f"\n--- Manage Students ({role}) ---")
        print("1. Add Student\n2. View Students\n3. Search Student\n4. Edit Student\n5. View Courses")
        if role == "admin":
            print("6. Delete Student\n7. Add Course\n8. Delete Course")
        print("0. Logout")
        
        try:
            ch_input = input("Enter choice: ")
            if not ch_input.isdigit():
                print("Invalid choice. Please enter a number.")
                continue
            ch = int(ch_input)
            
            if ch == 1:
                addstudent()
            elif ch == 2:
                view()
            elif ch == 3:
                search()
            elif ch == 4:
                editstudent()
            elif ch == 5:
                viewcourses()
            elif ch == 6 and role == "admin":
                delete()
            elif ch == 7 and role == "admin":
                addcourse()
            elif ch == 8 and role == "admin":
                deletecourse()
            elif ch == 0:
                print("Logged out successfully.")
                return
            else:
                print("Invalid choice or unauthorized action.")
        except sqlite3.Error as e:
            print("Database error:", e)

def addstudent():
    conn = sqlite3.connect("studentmanagement.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    name = input("Enter student name: ")
    email = input("Enter student email: ")
    if "@" not in email:
        print("Invalid email format.")
        conn.close()
        return
    viewcourses()
    try:
        course_id = int(input("Enter course ID: "))
    except ValueError:
        print("Invalid course ID. Must be a number.")
        conn.close()
        return
    
    try:
        cursor.execute("INSERT INTO student(sname, email, course_id) VALUES(?, ?, ?)", (name, email, course_id))
        conn.commit()
        print("Student added successfully.")
    except sqlite3.IntegrityError as e:
        print("Error: Email already exists or invalid course ID.", e)
    finally:
        conn.close()


def viewcourses():
    conn = sqlite3.connect("studentmanagement.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    cursor.execute("SELECT * FROM course")
    courses = cursor.fetchall()
    print("\n--- Available Courses ---")
    for i in courses:
        print(f"-- ID: {i[0]} -- Name: {i[1]} --")
    conn.close()


def addcourse():
    conn = sqlite3.connect("studentmanagement.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    cname = input("Enter course name: ")
    try:
        cursor.execute("INSERT INTO course(cname) VALUES(?)", (cname,))
        conn.commit()
        print("Course added successfully.")
    except sqlite3.IntegrityError:
        print("Course already exists.")
    finally:
        conn.close()


def deletecourse():
    conn = sqlite3.connect("studentmanagement.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    try:
        id_ = int(input("Enter course ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        conn.close()
        return
        
    if input("Confirm to delete (y/n): ").lower() == "y":
        cursor.execute("DELETE FROM course WHERE id=?", (id_,))
        conn.commit()
        print("Deleted" if cursor.rowcount else "Invalid ID")
    else:
        print("Deletion cancelled.")
    conn.close()


def view():
    conn = sqlite3.connect("studentmanagement.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    cursor.execute("SELECT s.id, s.sname, s.email, c.cname FROM student s JOIN course c ON c.id = s.course_id")
    data = cursor.fetchall()
    print(f"\nStudents found: {len(data)}")
    for i in data:
        print(f"-- ID: {i[0]} -- Name: {i[1]} -- Email: {i[2]} -- Course: {i[3]} --")
    conn.close()


def search():
    conn = sqlite3.connect("studentmanagement.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    try:
        id_ = int(input("Enter the student ID to be searched: "))
    except ValueError:
        print("Invalid ID.")
        conn.close()
        return
        
    cursor.execute("SELECT s.id, s.sname, s.email, c.cname FROM student s JOIN course c ON c.id = s.course_id WHERE s.id=?", (id_,))
    data = cursor.fetchone()
    if data:
        print("Student found:")
        print(f"-- ID: {data[0]} -- Name: {data[1]} -- Email: {data[2]} -- Course: {data[3]} --")
    else:
        print("Student not found.")
    conn.close()


def editstudent():
    conn = sqlite3.connect("studentmanagement.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    try:
        id_ = int(input("Enter the student ID to be updated: "))
    except ValueError:
        print("Invalid ID.")
        conn.close()
        return
        
    name = input("Enter new name: ")
    email = input("Enter new email: ")
    viewcourses()
    try:
        course_id = int(input("Enter new course ID: "))
    except ValueError:
        print("Invalid course ID.")
        conn.close()
        return
        
    cursor.execute("UPDATE student SET sname=?, email=?, course_id=? WHERE id=?", (name, email, course_id, id_))
    conn.commit()
    print("Student updated successfully" if cursor.rowcount else "Invalid student ID")
    conn.close()


def delete():
    conn = sqlite3.connect("studentmanagement.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    try:
        id_ = int(input("Enter the student ID to be deleted: "))
    except ValueError:
        print("Invalid ID.")
        conn.close()
        return
        
    if input("Confirm to delete row (y/n): ").lower() == "y":
        cursor.execute("DELETE FROM student WHERE id=?", (id_,))
        conn.commit()
        print("Deleted" if cursor.rowcount else "Invalid student ID")
    else:
        print("Deletion cancelled.")
    conn.close()


def register():
    conn = sqlite3.connect("studentmanagement.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    username = input("Enter username: ")
    password = input("Enter password (min 6 characters): ")
    role=input(" enter designation")
    if len(password) < 6:
        print("Password too short.")
        conn.close()
        return
    try:
        cursor.execute("INSERT INTO user(name, password, role) VALUES(?, ?, ?)", (username, password,role))
        conn.commit()
        print("User created successfully.")
    except sqlite3.IntegrityError:
        print("Username already taken.")
    finally:
        conn.close()


def login():
    conn = sqlite3.connect("studentmanagement.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    username = input("Enter username: ")
    password = input("Enter password: ")
    cursor.execute("SELECT id, role FROM user WHERE name=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return user[1]  # role: 'admin' or 'staff'
    print("Invalid username or password.")


def main():
    print("Welcome to Student Management System")
    while True:
        print("\n1. Login\n2. Register\n3. Exit")
        ch_input = input("Enter choice: ")
        if not ch_input.isdigit():
            print("Invalid choice. Please enter a number.")
            continue
        ch = int(ch_input)
        
        if ch == 1:
            role = login()
            if role:
                sub(role)
        elif ch == 2:
            register()
        elif ch == 3:
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please choose 1, 2, or 3.")
            
            
if __name__ == "__main__":
    main()