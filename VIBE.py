
# Mamadou Mahaman Laouan
# CIS261
# WK10 VIBE Coding

import csv
import os
import tempfile


# Hold each student's name, ID, three scores, average, and letter grade in a dictionary.
students = []
STUDENT_FILE = "student_grades.txt"
SCORE_FIELDS = ["test1", "test2", "test3"]
GRADE_LETTERS = ("A", "B", "C", "D", "F")


# Return the arithmetic mean of three test scores.
def calculate_average(score1, score2, score3):
    return (score1 + score2 + score3) / 3


# Convert a numeric average to the corresponding letter grade.
def calculate_letter_grade(average):
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


# Ask for one score and repeat until the user enters a number from 0 to 100.
def get_valid_score(prompt):
    while True:
        try:
            score = float(input(prompt))
            if 0 <= score <= 100:
                return score
            print("Enter a score from 0 to 100.")
        except ValueError:
            print("Enter a valid number.")


def get_valid_student_id():
    while True:
        student_id = input("Student ID: ").strip()
        if not student_id:
            print("Student ID cannot be blank.")
        elif any(
            student_id.casefold() == student["id"].casefold()
            for student in students
        ):
            print("That student ID is already in use.")
        else:
            return student_id


# Collect a student's name, ID, and three scores, then add the calculated record.
def add_student():
    name = input("Student name: ").strip()
    while not name:
        print("Name cannot be blank.")
        name = input("Student name: ").strip()

    student_id = get_valid_student_id()
    scores = [
        get_valid_score("Test score 1 (0-100): "),
        get_valid_score("Test score 2 (0-100): "),
        get_valid_score("Test score 3 (0-100): "),
    ]
    average = calculate_average(*scores)
    students.append(
        {
            "name": name,
            "id": student_id,
            "scores": scores,
            "average": average,
            "letter_grade": calculate_letter_grade(average),
        }
    )
    print(f"Added {name} with a grade of {average:.2f} ({calculate_letter_grade(average)}).")


def _display_student_table(records):
    headers = ("Name", "ID", "Test 1", "Test 2", "Test 3", "Average", "Grade")
    rows = [
        (
            student["name"],
            student["id"],
            *(f"{score:.2f}" for score in student["scores"]),
            f"{student['average']:.2f}",
            student["letter_grade"],
        )
        for student in records
    ]
    widths = [
        max(len(header), *(len(row[index]) for row in rows))
        for index, header in enumerate(headers)
    ]

    def format_row(values):
        return " | ".join(
            value.ljust(widths[index]) if index < 2 else value.rjust(widths[index])
            for index, value in enumerate(values)
        )

    print(format_row(headers))
    print("-+-".join("-" * width for width in widths))
    for row in rows:
        print(format_row(row))


# Print one student record with all scores and the average rounded to two decimals.
def display_student(student):
    _display_student_table([student])


# Display every stored student, or explain when the list is empty.
def display_all_students():
    if not students:
        print("No student records to display.")
        return

    print("\nStudent records:")
    _display_student_table(students)


# Find and display every student whose name contains the search text.
def search_student():
    query = input("Enter a name to search for: ").strip().casefold()
    if not query:
        print("Enter a name to search for.")
        return

    matches = [student for student in students if query in student["name"].casefold()]
    if not matches:
        print("No matching students found.")
        return

    _display_student_table(matches)


# Summarize the class average and the students with the highest and lowest averages.
def show_class_statistics():
    if not students:
        print("No student records available for statistics.")
        return

    class_average = sum(student["average"] for student in students) / len(students)
    highest = max(students, key=lambda student: student["average"])
    lowest = min(students, key=lambda student: student["average"])
    print(f"Number of students: {len(students)}")
    print(f"Class average: {class_average:.2f}")
    print(f"Highest average: {highest['name']} ({highest['average']:.2f})")
    print(f"Lowest average: {lowest['name']} ({lowest['average']:.2f})")
    print("Grade distribution:")
    for grade in GRADE_LETTERS:
        count = sum(student["letter_grade"] == grade for student in students)
        print(f"{grade}: {count}")


def _next_student_id(used_ids):
    number = 1001
    while f"S{number}".casefold() in used_ids:
        number += 1
    return f"S{number}"


def _write_students():
    temporary_path = None
    try:
        directory = os.path.dirname(os.path.abspath(STUDENT_FILE))
        with tempfile.NamedTemporaryFile(
            "w", newline="", encoding="utf-8", dir=directory, delete=False
        ) as file:
            temporary_path = file.name
            writer = csv.writer(file, delimiter="|", lineterminator="\n")
            for student in students:
                writer.writerow(
                    (
                        student["name"],
                        student["id"],
                        *(f"{score:.2f}" for score in student["scores"]),
                        f"{student['average']:.2f}",
                        student["letter_grade"],
                    )
                )
        os.replace(temporary_path, STUDENT_FILE)
        temporary_path = None
    finally:
        if temporary_path is not None:
            try:
                os.unlink(temporary_path)
            except FileNotFoundError:
                pass


def _read_student_record(record, header, used_ids):
    fields = [field.strip().casefold() for field in header]
    if fields:
        name_index = fields.index("name")
        id_index = fields.index("id") if "id" in fields else None
        score_indices = [
            fields.index(test_field if test_field in fields else score_field)
            for test_field, score_field in zip(
                SCORE_FIELDS, ("score1", "score2", "score3")
            )
        ]
        if id_index is None:
            student_id = _next_student_id(used_ids)
        else:
            student_id = record[id_index].strip()
    else:
        if len(record) == 7:
            name_index, id_index, score_indices = 0, 1, (2, 3, 4)
            float(record[5])
            if record[6].strip().upper() not in GRADE_LETTERS:
                raise ValueError
            student_id = record[id_index].strip()
        elif len(record) == 5:
            name_index, id_index, score_indices = 0, 1, (2, 3, 4)
            student_id = record[id_index].strip()
        elif len(record) == 4:
            name_index, id_index, score_indices = 0, None, (1, 2, 3)
            student_id = _next_student_id(used_ids)
        else:
            raise ValueError

    name = record[name_index].strip()
    scores = [float(record[index]) for index in score_indices]
    if (
        not name
        or not student_id
        or any(not 0 <= score <= 100 for score in scores)
        or student_id.casefold() in used_ids
    ):
        raise ValueError

    average = calculate_average(*scores)
    used_ids.add(student_id.casefold())
    return {
        "name": name,
        "id": student_id,
        "scores": scores,
        "average": average,
        "letter_grade": calculate_letter_grade(average),
    }


# Load pipe-delimited records, migrating the earlier CSV format when necessary.
def load_students():
    students.clear()
    try:
        with open(STUDENT_FILE, "r", newline="", encoding="utf-8") as file:
            first_line = file.readline()
            if not first_line:
                print("Loaded 0 student record(s).")
                return

            delimiter = "|" if "|" in first_line else ","
            file.seek(0)
            reader = csv.reader(file, delimiter=delimiter)
            first_record = next(reader, None)
            if first_record is None:
                print("Loaded 0 student record(s).")
                return

            fields = [field.strip().casefold() for field in first_record]
            has_header = "name" in fields and any(
                field in fields
                for field in ("id", "test1", "score1")
            )
            header = first_record if has_header else []
            records = reader if has_header else [first_record, *reader]
            needs_migration = delimiter != "|" or has_header
            found_invalid_record = False
            used_ids = set()

            for line_number, record in enumerate(records, start=2 if has_header else 1):
                if not record:
                    continue
                try:
                    if not has_header and len(record) != 7:
                        needs_migration = True
                    student = _read_student_record(record, header, used_ids)
                except (IndexError, TypeError, ValueError):
                    found_invalid_record = True
                    print(f"Skipping invalid student record on line {line_number}.")
                    continue
                students.append(student)

        if needs_migration and not found_invalid_record:
            _write_students()
            print("Migrated saved records to pipe-delimited format.")
        elif needs_migration:
            print("Saved file was not migrated because it contains invalid records.")
        print(f"Loaded {len(students)} student record(s).")
    except FileNotFoundError:
        print("No saved records found; starting with an empty list.")
    except (OSError, UnicodeDecodeError, csv.Error) as error:
        print(f"Could not load student records: {error}")


# Save all records as pipe-delimited rows in the required field order.
def save_students():
    try:
        _write_students()
    except (OSError, csv.Error) as error:
        print(f"Could not save student records: {error}")
        return False

    print(f"Saved {len(students)} student record(s) to {STUDENT_FILE}.")
    return True


# Load existing records, handle menu actions, and save before exiting.
def main():
    load_students()
    while True:
        print("\nStudent Grade Calculator")
        print("1. Add a student")
        print("2. Display all students")
        print("3. Search by name")
        print("4. Show class statistics")
        print("5. Save and exit (or press ESC)")
        choice = input("Choose an option: ").strip()

        if choice in ("5", "\x1b"):
            if save_students():
                print("Goodbye.")
                break
        elif choice == "1":
            add_student()
        elif choice == "2":
            display_all_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            show_class_statistics()
        else:
            print("Choose an option from 1 to 5, or press ESC to save and exit.")


if __name__ == "__main__":
    main()
