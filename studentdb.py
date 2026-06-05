import mysql.connector
from rich.console import Console
from rich.table import Table

console = Console()

# ------------------- DB Connection -------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",       # Your DB server
        user="root",            # DB username
        password="password",    # DB password
        database="student_db"   # Your DB name (create manually first!)
    )

# ------------------- Insert Functions -------------------
def add_student(name, age, department):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Students(name, age, department) VALUES (%s, %s, %s)", (name, age, department))
    conn.commit()
    conn.close()

def add_course(course_name, credits):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Courses(course_name, credits) VALUES (%s, %s)", (course_name, credits))
    conn.commit()
    conn.close()

def add_grade(student_id, course_id, marks):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Grades(student_id, course_id, marks) VALUES (%s, %s, %s)", (student_id, course_id, marks))
    conn.commit()
    conn.close()

def add_attendance(student_id, course_id, attended, total):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Attendance(student_id, course_id, attended, total) VALUES (%s, %s, %s, %s)", (student_id, course_id, attended, total))
    conn.commit()
    conn.close()

# ------------------- Reports -------------------
def calculate_gpa(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT marks, credits FROM Grades 
        JOIN Courses ON Grades.course_id = Courses.course_id 
        WHERE student_id=%s
    """, (student_id,))
    records = cursor.fetchall()
    conn.close()

    if not records:
        return 0

    total_points = 0
    total_credits = 0

    for marks, credits in records:
        if marks >= 90:
            grade_point = 10
        elif marks >= 80:
            grade_point = 9
        elif marks >= 70:
            grade_point = 8
        elif marks >= 60:
            grade_point = 7
        elif marks >= 50:
            grade_point = 6
        else:
            grade_point = 0
        total_points += grade_point * credits
        total_credits += credits

    return total_points / total_credits if total_credits else 0

def calculate_attendance(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(attended), SUM(total) FROM Attendance WHERE student_id=%s", (student_id,))
    record = cursor.fetchone()
    conn.close()
    if record and record[1]:
        return (record[0] / record[1]) * 100
    return 0

def generate_report():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, name, age, department FROM Students")
    students = cursor.fetchall()
    conn.close()

    table = Table(title="📊 Student Academic Report", style="bold cyan")
    table.add_column("ID", justify="center", style="yellow", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Age", justify="center")
    table.add_column("Department", style="magenta")
    table.add_column("GPA", justify="center", style="bright_blue")
    table.add_column("Attendance %", justify="center", style="bright_red")

    for sid, name, age, dept in students:
        gpa = calculate_gpa(sid)
        att = calculate_attendance(sid)
        table.add_row(str(sid), name, str(age), dept, f"{gpa:.2f}", f"{att:.2f}%")

    console.print(table)

# ------------------- Menu Interface -------------------
def menu():
    while True:
        console.print("\\n[bold underline yellow]===== Student DBMS Menu =====[/]")
        console.print("1. Add Student")
        console.print("2. Add Course")
        console.print("3. Add Grade")
        console.print("4. Add Attendance")
        console.print("5. Generate Report")
        console.print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter name: ")
            age = int(input("Enter age: "))
            dept = input("Enter department: ")
            add_student(name, age, dept)
            console.print("[green]✔ Student added![/]")

        elif choice == "2":
            cname = input("Enter course name: ")
            credits = int(input("Enter credits: "))
            add_course(cname, credits)
            console.print("[green]✔ Course added![/]")

        elif choice == "3":
            sid = int(input("Enter student ID: "))
            cid = int(input("Enter course ID: "))
            marks = int(input("Enter marks: "))
            add_grade(sid, cid, marks)
            console.print("[green]✔ Grade added![/]")

        elif choice == "4":
            sid = int(input("Enter student ID: "))
            cid = int(input("Enter course ID: "))
            attended = int(input("Enter attended classes: "))
            total = int(input("Enter total classes: "))
            add_attendance(sid, cid, attended, total)
            console.print("[green]✔ Attendance added![/]")

        elif choice == "5":
            generate_report()

        elif choice == "6":
            console.print("[bold red]Exiting...[/]")
            break

        else:
            console.print("[red]Invalid choice. Try again.[/]")

# ------------------- Run -------------------
if __name__ == "__main__":
    # Run menu directly
    menu()
