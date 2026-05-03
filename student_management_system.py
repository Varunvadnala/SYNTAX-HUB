"""
Student Management System

A professional command-line interface application for managing student records.
Features robust error handling, type hinting, and persistent JSON storage.
"""

import json
import os
import logging
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from datetime import datetime

# Configure logging for internal application events
logging.basicConfig(
    filename='student_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class StudentManagementError(Exception):
    """Base exception class for Student Management System."""
    pass

class StudentNotFoundError(StudentManagementError):
    """Raised when a requested student ID does not exist."""
    pass

class DuplicateStudentError(StudentManagementError):
    """Raised when attempting to add a student with an existing ID."""
    pass

@dataclass
class Student:
    """Represents a single student entity."""
    student_id: str
    name: str
    grade: str
    created_at: str = ""

    def __post_init__(self) -> None:
        if not self.created_at:
            self.created_at = datetime.now().isoformat(timespec="seconds")

    def to_dict(self) -> dict:
        """Serializes the student instance to a dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Student':
        """Deserializes a dictionary into a Student instance."""
        # Ensure we only pass expected keys in case of schema evolution
        valid_keys = {"student_id", "name", "grade", "created_at"}
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered_data)


class StudentManager:
    """Handles the business logic and data persistence for students."""
    
    def __init__(self, storage_file: str = "students.json") -> None:
        self._storage_file = storage_file
        self._students: Dict[str, Student] = {}
        self._load_data()

    def _load_data(self) -> None:
        """Loads data from the JSON file into memory."""
        if not os.path.exists(self._storage_file):
            logging.info("Storage file not found. Starting with an empty database.")
            return

        try:
            with open(self._storage_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    student = Student.from_dict(item)
                    self._students[student.student_id] = student
            logging.info(f"Successfully loaded {len(self._students)} students.")
        except json.JSONDecodeError:
            logging.error("Corrupted JSON file. Starting fresh.")
        except Exception as e:
            logging.error(f"Unexpected error loading data: {e}")

    def _save_data(self) -> None:
        """Persists the current in-memory students to the JSON file."""
        try:
            with open(self._storage_file, 'w', encoding='utf-8') as f:
                data = [student.to_dict() for student in self._students.values()]
                json.dump(data, f, indent=4)
            logging.info("Data successfully saved.")
        except Exception as e:
            logging.error(f"Failed to save data: {e}")
            raise StudentManagementError(f"Could not save data: {e}")

    def add_student(self, student_id: str, name: str, grade: str) -> None:
        """
        Adds a new student to the system.
        
        Args:
            student_id (str): Unique identifier for the student.
            name (str): Full name of the student.
            grade (str): Grade or class of the student.
            
        Raises:
            DuplicateStudentError: If the student_id already exists.
        """
        if student_id in self._students:
            raise DuplicateStudentError(f"Student ID '{student_id}' already exists.")
        
        new_student = Student(student_id=student_id, name=name, grade=grade)
        self._students[student_id] = new_student
        self._save_data()
        logging.info(f"Added new student: {student_id} - {name}")

    def update_student(self, student_id: str, name: Optional[str] = None, grade: Optional[str] = None) -> None:
        """Updates an existing student's information."""
        if student_id not in self._students:
            raise StudentNotFoundError(f"Student ID '{student_id}' not found.")
        
        student = self._students[student_id]
        if name:
            student.name = name
        if grade:
            student.grade = grade
            
        self._save_data()
        logging.info(f"Updated student: {student_id}")

    def delete_student(self, student_id: str) -> Student:
        """Deletes a student and returns the deleted record."""
        if student_id not in self._students:
            raise StudentNotFoundError(f"Student ID '{student_id}' not found.")
        
        deleted_student = self._students.pop(student_id)
        self._save_data()
        logging.info(f"Deleted student: {student_id}")
        return deleted_student

    def get_all_students(self) -> List[Student]:
        """Returns a list of all students sorted by ID."""
        return sorted(self._students.values(), key=lambda s: s.student_id)


class CLIView:
    """Handles the user interface and interactions."""
    
    def __init__(self, manager: StudentManager) -> None:
        self.manager = manager

    @staticmethod
    def print_header(title: str) -> None:
        """Prints a nicely formatted header."""
        print("\n" + "=" * 60)
        print(f"{title.center(60)}")
        print("=" * 60)

    @staticmethod
    def print_error(message: str) -> None:
        """Prints an error message clearly."""
        print(f"\n[!] ERROR: {message}")

    @staticmethod
    def print_success(message: str) -> None:
        """Prints a success message clearly."""
        print(f"\n[*] SUCCESS: {message}")

    def get_input(self, prompt: str, required: bool = True) -> str:
        """Robust input collection."""
        while True:
            value = input(prompt).strip()
            if not value and required:
                self.print_error("This field cannot be empty. Please try again.")
            else:
                return value

    def run(self) -> None:
        """Main application loop."""
        while True:
            self.print_header("Student Management System")
            print("  1. Add New Student")
            print("  2. Update Existing Student")
            print("  3. Delete Student")
            print("  4. List All Students")
            print("  5. Exit")
            print("-" * 60)
            
            choice = input("Select an option (1-5): ").strip()
            
            try:
                if choice == '1':
                    self._handle_add()
                elif choice == '2':
                    self._handle_update()
                elif choice == '3':
                    self._handle_delete()
                elif choice == '4':
                    self._handle_list()
                elif choice == '5':
                    self.print_header("Thank you for using the system. Goodbye!")
                    break
                else:
                    self.print_error("Invalid selection. Please enter a number between 1 and 5.")
            except StudentManagementError as e:
                self.print_error(str(e))
            except Exception as e:
                self.print_error(f"An unexpected error occurred. Check logs.")
                logging.error(f"Unhandled UI exception: {e}", exc_info=True)

    def _handle_add(self) -> None:
        print("\n--- Add New Student ---")
        student_id = self.get_input("Enter Student ID: ")
        name = self.get_input("Enter Student Name: ")
        grade = self.get_input("Enter Student Grade: ")
        
        self.manager.add_student(student_id, name, grade)
        self.print_success(f"Student '{name}' added successfully.")

    def _handle_update(self) -> None:
        print("\n--- Update Student ---")
        student_id = self.get_input("Enter Student ID to update: ")
        
        print("(Press Enter to keep current value)")
        name = self.get_input("Enter new Name: ", required=False)
        grade = self.get_input("Enter new Grade: ", required=False)
        
        if not name and not grade:
            print("\nNo changes made.")
            return
            
        self.manager.update_student(
            student_id, 
            name=name if name else None, 
            grade=grade if grade else None
        )
        self.print_success(f"Student ID '{student_id}' updated successfully.")

    def _handle_delete(self) -> None:
        print("\n--- Delete Student ---")
        student_id = self.get_input("Enter Student ID to delete: ")
        
        confirmation = self.get_input(f"Are you sure you want to delete ID '{student_id}'? (y/n): ")
        if confirmation.lower() == 'y':
            deleted = self.manager.delete_student(student_id)
            self.print_success(f"Student '{deleted.name}' deleted successfully.")
        else:
            print("\nDeletion cancelled.")

    def _handle_list(self) -> None:
        students = self.manager.get_all_students()
        
        if not students:
            print("\nNo student records found in the system.")
            return
            
        print("\n" + "-" * 75)
        print(f"| {'ID':<10} | {'Name':<25} | {'Grade':<10} | {'Joined':<16} |")
        print("-" * 75)
        for s in students:
            date_str = s.created_at[:10] if s.created_at else "N/A"
            print(f"| {s.student_id:<10} | {s.name:<25} | {s.grade:<10} | {date_str:<16} |")
        print("-" * 75)
        print(f"Total Records: {len(students)}")


def main() -> None:
    try:
        manager = StudentManager()
        app = CLIView(manager)
        app.run()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user. Exiting gracefully.")
    except Exception as e:
        print(f"\n[!] Critical failure: {e}")
        logging.critical(f"App crashed: {e}", exc_info=True)

if __name__ == "__main__":
    main()
