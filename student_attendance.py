from dataclasses import dataclass
from typing import List, Tuple, Dict
from collections import Counter
from datetime import datetime

# ---------------------------
# Data Model using Dataclasses
# ---------------------------

@dataclass
class Student:
    id: int
    name: str
    class_name: str

@dataclass
class AttendanceRecord:
    student_id: int
    records: List[Tuple[str, str]]  # List of tuples: (date as string, status)


# ---------------------------
# Static dataset (hardcoded)
# ---------------------------

students_data = [
    Student(101, "Anita Johnson", "10th Grade"),
    Student(102, "Dimyasree KV", "10th Grade"),
    Student(103, "Maryam Bhat", "10th Grade"),
    Student(104, "Musa K", "10th Grade"),
    Student(105, "Aamina Sid", "10th Grade"),
]

attendance_data = [
    AttendanceRecord(101, [('2025-02-25', 'Absent'), ('2025-02-26', 'Absent'), ('2025-02-27', 'Absent')]),
    AttendanceRecord(102, [('2025-02-25', 'Absent'), ('2025-02-26', 'Present'), ('2025-02-27', 'Present')]),
    AttendanceRecord(103, [('2025-02-25', 'Present'), ('2025-02-26', 'Absent'), ('2025-02-27', 'Present')]),
    AttendanceRecord(104, [('2025-02-25', 'Present'), ('2025-02-26', 'Present'), ('2025-02-27', 'Present')]),
    AttendanceRecord(105, [('2025-02-25', 'Absent'), ('2025-02-26', 'Present'), ('2025-02-27', 'Absent')]),
]

# Create dictionary for quick student lookup by ID
students_dict: Dict[int, Student] = {student.id: student for student in students_data}

# Create dictionary for quick attendance lookup by student ID
attendance_dict: Dict[int, List[Tuple[str, str]]] = {
    record.student_id: record.records for record in attendance_data
}


# ---------------------------
# Function to count unique attendance days
# ---------------------------

def count_number_of_days_using_dates() -> int:
    """
    Collects all unique attendance dates from all students and returns the count.
    """
    unique_dates = {date for records in attendance_dict.values() for date, _ in records}
    return len(unique_dates)


# ---------------------------
# Function to find student with most absent days using Counter
# ---------------------------

def find_most_absent_student() -> Tuple[str, int]:
    """
    Counts absences for each student and returns
    the student with the highest number of absences.
    """
    absence_counter = Counter()

    for student_id, records in attendance_dict.items():
        for _, status in records:
            if status == 'Absent':
                absence_counter[student_id] += 1

    if not absence_counter:
        return ("No absences recorded", 0)

    # Find the student with the max absences
    most_absent_student_id, max_absences = absence_counter.most_common(1)[0]
    student_name = students_dict[most_absent_student_id].name
    return (student_name, max_absences)


# ---------------------------
# Function to show all students' absences
# ---------------------------

def show_all_students_absences():
    """
    Prints the number of absent days for all students.
    """
    print("\nAttendance Summary (Absences):")
    absence_counter = Counter()
    for student_id, records in attendance_dict.items():
        absence_counter[student_id] = sum(1 for _, status in records if status == 'Absent')

    for student_id, absences in absence_counter.items():
        student_name = students_dict[student_id].name
        print(f"{student_name}: {absences} day(s) absent")


# ---------------------------
# Function to list students absent on a specific date
# ---------------------------

def list_absent_students_on_date():
    """
    Prompts user for a date and lists all students
    who were absent on that date.
    Includes input validation and helpful error messages.
    """
    date_input = input("Enter date (YYYY-MM-DD): ").strip()

    # Check empty input
    if not date_input:
        print(" Error: You must enter a valid date. Please try again.")
        return

    # Validate date format
    try:
        datetime.strptime(date_input, "%Y-%m-%d")
    except ValueError:
        print(" Error: Invalid date format. Please use YYYY-MM-DD.")
        return

    # Check if date exists in records
    all_dates = {date for records in attendance_dict.values() for date, _ in records}
    if date_input not in all_dates:
        print(f" Error: The date {date_input} was not found in attendance records.")
        print("Available dates:", ", ".join(sorted(all_dates)))
        return

    # List absent students on that date
    found = False
    print(f"\nStudents absent on {date_input}:")
    for student_id, records in attendance_dict.items():
        for date, status in records:
            if date == date_input and status == 'Absent':
                print(f"- {students_dict[student_id].name}")
                found = True
                break

    if not found:
        print("All students were present on that date.")


# ---------------------------
# Function to show attendance percentage per student
# ---------------------------

def attendance_percentage_per_student():
    """
    Calculates and displays attendance percentage for each student.
    """
    print("\nAttendance Percentage per Student:")
    for student_id, records in attendance_dict.items():
        total_days = len(records)
        present_days = sum(1 for _, status in records if status == 'Present')
        percentage = (present_days / total_days) * 100 if total_days > 0 else 0
        student_name = students_dict[student_id].name
        print(f"{student_name}: {percentage:.2f}% present")


# ---------------------------
# Menu display function
# ---------------------------

def show_menu():
    print("\n--- Student Attendance Management Menu ---")
    print("1. Count number of unique attendance days")
    print("2. Show student with most absences")
    print("3. Show all students' absences")
    print("4. List students absent on a specific date")
    print("5. Show attendance percentage per student")
    print("6. Exit")


# ---------------------------
# Main program loop
# ---------------------------

def main():
    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            result = count_number_of_days_using_dates()
            print(f"\nTotal unique attendance days: {result}")

        elif choice == '2':
            name, absents = find_most_absent_student()
            print(f"\nStudent with most absent days: {name} ({absents} day(s))")

        elif choice == '3':
            show_all_students_absences()

        elif choice == '4':
            list_absent_students_on_date()

        elif choice == '5':
            attendance_percentage_per_student()

        elif choice == '6':
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


# ---------------------------
# Entry point of program
# ---------------------------

if __name__ == "__main__":
    main()
