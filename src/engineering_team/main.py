#!/usr/bin/env python

import warnings
import os

from engineering_team.crew import EngineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)

requirements = """
Build a Clinic and Hospital Appointment Management System.

The system should allow:

- Patient registration and management.
- Doctor registration and management.
- Medical specialty management.
- Scheduling appointments between patients and doctors.
- Preventing appointment conflicts and overlapping schedules.
- Appointment cancellation.
- Appointment rescheduling.
- Tracking appointment statuses (Scheduled, Completed, Cancelled, No Show).
- Searching appointments by patient, doctor, specialty, or date.
- Managing doctor availability and working schedules.
- Generating reports for appointments, doctors, and patients.
- Viewing upcoming appointments.
- Viewing appointment history.
- Basic validation of patient and doctor data.

Business Rules:

- A doctor cannot have two appointments at the same time.
- A patient cannot have multiple appointments at the same date and time.
- Appointments can only be scheduled within a doctor's available hours.
- Cancelled appointments should remain in the history.
- Rescheduled appointments should preserve audit information.
- The system should provide statistics such as:
    - Total appointments
    - Appointments by doctor
    - Appointments by specialty
    - Cancelled appointments
    - Completed appointments

Technical Requirements:

- Everything should be implemented in a single Python module.
- Use object-oriented programming.
- Keep the module self-contained.
- Do not require an external database.
- Store data in memory using classes and collections.
- The module should be ready for unit testing.
- The module should be simple enough for a Gradio interface to consume.
"""

module_name = "appointment_management.py"
class_name = "AppointmentManagementSystem"


def run():
    """
    Run the Engineering Team crew.
    """

    inputs = {
        "requirements": requirements,
        "module_name": module_name,
        "class_name": class_name,
    }

    result = EngineeringTeam().crew().kickoff(inputs=inputs)

    print("\n" + "=" * 60)
    print("PROJECT GENERATION COMPLETED")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    run()