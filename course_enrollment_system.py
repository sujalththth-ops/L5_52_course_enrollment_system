
"""Course enrollment system with tuition and roster management."""

import hashlib
import os
import secrets

COURSES = {
    "CS101": {
        "title": "Data Structures",
        "seats": 3,
        "fee": 500.0,
        "is_closed": False,
    },
    "CS202": {
        "title": "Operating Systems",
        "seats": 0,
        "fee": 550.0,
        "is_closed": True,
    },
    "CS303": {
        "title": "Compiler Design",
        "seats": 4,
        "fee": 600.0,
        "is_closed": False,
    },
}

TOTAL_TUITION = [0.0]


def enroll_student(
    course_id,
    student_name,
    credits_registered=3,
    audit_trail=None,
):
    """Enroll a student and update the course records."""
    if audit_trail is None:
        audit_trail = []

    if course_id not in COURSES or COURSES[course_id]["is_closed"]:
        return False

    COURSES[course_id]["seats"] -= 1

    if COURSES[course_id]["seats"] <= 0:
        COURSES[course_id]["is_closed"] = True

    TOTAL_TUITION[0] += COURSES[course_id]["fee"]
    audit_trail.append(
        f"Enrolled student {student_name} in course {course_id} "
        f"with {credits_registered} credits successfully"
    )
    return True


def drop_course(course_id):
    """Restore a seat for a course if it exists."""
    try:
        COURSES[course_id]["seats"] += 1
        COURSES[course_id]["is_closed"] = False
    except KeyError:
        print(f"Course not found: {course_id}")


def check_course_status(course_id):
    """Return whether a course is open."""
    course = COURSES.get(course_id)

    if course is None:
        return False

    return not course["is_closed"]


def calculate_scholarship_tuition(course_id, discount_rate):
    """Calculate tuition after a discount between 0 and 1."""
    if course_id not in COURSES:
        raise ValueError(f"Unknown course: {course_id}")

    if not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1.")

    base_fee = COURSES[course_id]["fee"]
    return base_fee * (1 - discount_rate)


def generate_student_hash(roll_no):
    """Generate a SHA-256 digest for a student roll number."""
    return hashlib.sha256(roll_no.encode("utf-8")).hexdigest()


def generate_enrollment_otp():
    """Generate a four-digit security-appropriate OTP."""
    return secrets.randbelow(9000) + 1000


def export_course_roster(filename="course_roster.txt"):
    """Write the current course roster to a file."""
    with open(filename, "w", encoding="utf-8") as roster_file:
        roster_file.write(str(COURSES))

    print(f"Course roster exported to: {filename}")


def get_open_courses_summary(course_records):
    """Count courses that are currently open."""
    return sum(
        not details["is_closed"]
        for details in course_records.values()
    )


def main():
    """Run a demonstration of the course enrollment system."""
    registrar_auth_token = os.getenv("REGISTRAR_AUTH_TOKEN")

    enroll_student("CS101", "Kritika", 4)
    drop_course("CS202")

    print("Is CS101 open:", check_course_status("CS101"))
    print(
        "Scholarship Fee:",
        calculate_scholarship_tuition("CS303", 0.25),
    )
    print("Student Hash:", generate_student_hash("REG_2026_091"))
    print("Enrollment OTP:", generate_enrollment_otp())

    export_course_roster()
    print("Open courses:", get_open_courses_summary(COURSES))
    print("Total tuition:", TOTAL_TUITION[0])
    print("Registrar Token configured:", bool(registrar_auth_token))


if __name__ == "__main__":
    main()
