
# Mamadou Mahaman Laouan
# CIS261
# WK10 VIBE Coding

import csv


# Hold each student's name, three scores, average, and letter grade in a dictionary.
students = []
STUDENT_FILE = "student_grades.txt"
SCORE_FIELDS = ["score1", "score2", "score3"]


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


# Collect a student's name and three scores, then add the calculated record.
def add_student():
    name = input("Student name: ").strip()
    while not name:
        print("Name cannot be blank.")
        name = input("Student name: ").strip()

    scores = [
        get_valid_score("Test score 1 (0-100): "),
        get_valid_score("Test score 2 (0-100): "),
        get_valid_score("Test score 3 (0-100): "),
    ]
    average = calculate_average(*scores)
    students.append(
        {
            "name": name,
            "scores": scores,
            "average": average,
            "letter_grade": calculate_letter_grade(average),
        }
    )
    print(f"Added {name} with a grade of {average:.2f} ({calculate_letter_grade(average)}).")


# Print one student record with all scores and the average rounded to two decimals.
def display_student(student):
    score_text = ", ".join(f"{score:.2f}" for score in student["scores"])
    print(
        f"{student['name']} | Scores: {score_text} | "
        f"Average: {student['average']:.2f} | Grade: {student['letter_grade']}"
    )


# Display every stored student, or explain when the list is empty.
def display_all_students():
    if not students:
        print("No student records to display.")
        return

    print("\nStudent records:")
    for student in students:
        display_student(student)


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

    for student in matches:
        display_student(student)


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


# Load valid student rows from the CSV-formatted text file at startup.
def load_students():
    students.clear()
    try:
        with open(STUDENT_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for line_number, record in enumerate(reader, start=2):
                try:
                    name = (record.get("name") or "").strip()
                    scores = [float(record.get(field, "")) for field in SCORE_FIELDS]
                    if not name or any(not 0 <= score <= 100 for score in scores):
                        raise ValueError
                except (TypeError, ValueError):
                    print(f"Skipping invalid student record on line {line_number}.")
                    continue

                average = calculate_average(*scores)
                students.append(
                    {
                        "name": name,
                        "scores": scores,
                        "average": average,
                        "letter_grade": calculate_letter_grade(average),
                    }
                )
        print(f"Loaded {len(students)} student record(s).")
    except FileNotFoundError:
        print("No saved records found; starting with an empty list.")
    except (OSError, UnicodeDecodeError, csv.Error) as error:
        print(f"Could not load student records: {error}")


# Save all records in a format that can be read back by load_students.
def save_students():
    try:
        with open(STUDENT_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["name", *SCORE_FIELDS])
            writer.writeheader()
            for student in students:
                writer.writerow(
                    {
                        "name": student["name"],
                        **{
                            field: f"{score:.2f}"
                            for field, score in zip(SCORE_FIELDS, student["scores"])
                        },
                    }
                )
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
