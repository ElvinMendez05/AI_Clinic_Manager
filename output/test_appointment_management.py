```python
import unittest
from datetime import datetime, timedelta
from appointment_management import AppointmentManagementSystem, Patient, Doctor, Specialty, Appointment

class TestAppointmentManagementSystem(unittest.TestCase):
    
    def setUp(self):
        self.system = AppointmentManagementSystem()
        self.specialty = self.system.add_specialty("Cardiology")
        self.doctor = self.system.register_doctor("Dr. Smith", self.specialty, [datetime.now() + timedelta(days=i) for i in range(1, 6)])
        self.patient = self.system.register_patient("John Doe", "1980-01-01", "1234567890")

    def test_patient_creation(self):
        self.assertEqual(self.patient.name, "John Doe")
        self.assertEqual(self.patient.dob, "1980-01-01")
        self.assertEqual(self.patient.contact_info, "1234567890")

    def test_doctor_creation(self):
        self.assertEqual(self.doctor.name, "Dr. Smith")
        self.assertEqual(self.doctor.specialty.name, "Cardiology")
        self.assertTrue(len(self.doctor.available_hours) > 0)

    def test_specialty_creation(self):
        self.assertEqual(self.specialty.name, "Cardiology")

    def test_appointment_scheduling(self):
        scheduled_time = self.doctor.available_hours[0]
        appointment = self.system.schedule_appointment(self.patient.patient_id, self.doctor.doctor_id, scheduled_time)
        self.assertIsNotNone(appointment)
        self.assertEqual(appointment.scheduled_time, scheduled_time)
        
    def test_appointment_conflicts(self):
        scheduled_time = self.doctor.available_hours[0]
        self.system.schedule_appointment(self.patient.patient_id, self.doctor.doctor_id, scheduled_time)
        conflict_appointment = self.system.schedule_appointment(self.patient.patient_id, self.doctor.doctor_id, scheduled_time)
        self.assertIsNone(conflict_appointment)

    def test_appointment_cancellation(self):
        scheduled_time = self.doctor.available_hours[1]
        appointment = self.system.schedule_appointment(self.patient.patient_id, self.doctor.doctor_id, scheduled_time)
        self.assertTrue(self.system.cancel_appointment(appointment.appointment_id))
        self.assertEqual(appointment.status, "Cancelled")

    def test_appointment_rescheduling(self):
        scheduled_time = self.doctor.available_hours[2]
        new_time = self.doctor.available_hours[3]
        appointment = self.system.schedule_appointment(self.patient.patient_id, self.doctor.doctor_id, scheduled_time)
        self.assertIsNotNone(self.system.reschedule_appointment(appointment.appointment_id, new_time))
        self.assertEqual(appointment.scheduled_time, new_time)

    def test_search_functionality(self):
        appointments = self.system.search_appointments("doctor", self.doctor.doctor_id)
        existing_appointments_count = len(appointments)
        self.system.schedule_appointment(self.patient.patient_id, self.doctor.doctor_id, self.doctor.available_hours[4])
        updated_appointments = self.system.search_appointments("doctor", self.doctor.doctor_id)
        self.assertEqual(len(updated_appointments), existing_appointments_count + 1)

    def test_report_generation(self):
        self.system.schedule_appointment(self.patient.patient_id, self.doctor.doctor_id, self.doctor.available_hours[0])
        self.system.cancel_appointment(1)
        total_appointments = self.system.generate_report("total_appointments")
        cancelled_appointments = self.system.generate_report("cancelled_appointments")
        self.assertEqual(total_appointments, 1)
        self.assertEqual(cancelled_appointments, 1)

    def test_validation_rules(self):
        invalid_patient = Patient(0, "", "2000-01-01", "")  # Missing name and contact
        invalid_doctor = Doctor(0, "", self.specialty, [])  # Missing name
        self.assertFalse(self.system.validate_data(invalid_patient))
        self.assertFalse(self.system.validate_data(invalid_doctor))

if __name__ == '__main__':
    unittest.main()
```