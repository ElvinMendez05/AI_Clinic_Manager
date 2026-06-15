class AppointmentManagementSystem:
    def __init__(self):
        self.patients = []
        self.doctors = []
        self.specialties = []
        self.appointments = []
        self.next_patient_id = 1
        self.next_doctor_id = 1
        self.next_appointment_id = 1

    def register_patient(self, name, dob, contact_info):
        patient = Patient(self.next_patient_id, name, dob, contact_info)
        self.next_patient_id += 1
        if self.validate_data(patient):
            self.patients.append(patient)
        return patient

    def register_doctor(self, name, specialty, available_hours):
        doctor = Doctor(self.next_doctor_id, name, specialty, available_hours)
        self.next_doctor_id += 1
        if self.validate_data(doctor):
            self.doctors.append(doctor)
        return doctor

    def add_specialty(self, name):
        specialty = Specialty(name)
        self.specialties.append(specialty)
        return specialty

    def schedule_appointment(self, patient_id, doctor_id, scheduled_time):
        patient = self._find_patient(patient_id)
        doctor = self._find_doctor(doctor_id)

        if not patient or not doctor:
            return None

        if not self._is_doctor_available(doctor, scheduled_time):
            return None

        if self._is_patient_scheduled(patient, scheduled_time):
            return None

        appointment = Appointment(self.next_appointment_id, patient, doctor, scheduled_time)
        self.next_appointment_id += 1
        self.appointments.append(appointment)
        return appointment

    def cancel_appointment(self, appointment_id):
        appointment = self._find_appointment(appointment_id)
        if appointment:
            appointment.status = "Cancelled"
            return True
        return False

    def reschedule_appointment(self, appointment_id, new_time):
        appointment = self._find_appointment(appointment_id)
        if appointment and self._is_doctor_available(appointment.doctor, new_time) and not self._is_patient_scheduled(appointment.patient, new_time):
            appointment.scheduled_time = new_time
            return appointment
        return None

    def search_appointments(self, filter_by, filter_value):
        results = []
        for app in self.appointments:
            if (filter_by == "patient" and app.patient.patient_id == filter_value) or \
               (filter_by == "doctor" and app.doctor.doctor_id == filter_value) or \
               (filter_by == "specialty" and app.doctor.specialty.name == filter_value) or \
               (filter_by == "date" and app.scheduled_time.date() == filter_value):
                results.append(app)
        return results

    def generate_report(self, report_type):
        if report_type == "total_appointments":
            return len(self.appointments)
        elif report_type == "appointments_by_doctor":
            return self._generate_appointments_by_doctor()
        elif report_type == "appointments_by_specialty":
            return self._generate_appointments_by_specialty()
        elif report_type == "cancelled_appointments":
            return len([app for app in self.appointments if app.status == "Cancelled"])
        elif report_type == "completed_appointments":
            return len([app for app in self.appointments if app.status == "Completed"])
        return None

    def validate_data(self, record):
        if isinstance(record, Patient):
            return bool(record.name and record.contact_info)

        if isinstance(record, Doctor):
            return bool(record.name and record.specialty)

        return False

    def _find_patient(self, patient_id):
        return next((p for p in self.patients if p.patient_id == patient_id), None)

    def _find_doctor(self, doctor_id):
        return next((d for d in self.doctors if d.doctor_id == doctor_id), None)

    def _find_appointment(self, appointment_id):
        return next((a for a in self.appointments if a.appointment_id == appointment_id), None)

    def _is_doctor_available(self, doctor, scheduled_time):
        available_times = doctor.get_available_times(scheduled_time.date())
        return scheduled_time in available_times and not any(app.scheduled_time == scheduled_time for app in self.appointments if app.doctor == doctor)

    def _is_patient_scheduled(self, patient, scheduled_time):
        return any(app.scheduled_time == scheduled_time for app in self.appointments if app.patient == patient)

    def _generate_appointments_by_doctor(self):
        report = {}
        for doctor in self.doctors:
            report[doctor.doctor_id] = len([app for app in self.appointments if app.doctor == doctor])
        return report

    def _generate_appointments_by_specialty(self):
        report = {}
        for specialty in self.specialties:
            report[specialty.name] = len([app for app in self.appointments if app.doctor.specialty.name == specialty.name])
        return report


class Patient:
    def __init__(self, patient_id, name, dob, contact_info):
        self.patient_id = patient_id
        self.name = name
        self.dob = dob
        self.contact_info = contact_info

    def view_upcoming_appointments(self, appointments):
        return [app for app in appointments if app.patient == self and app.status == "Scheduled"]

    def view_appointment_history(self, appointments):
        return [app for app in appointments if app.patient == self]


class Doctor:
    def __init__(self, doctor_id, name, specialty, available_hours):
        self.doctor_id = doctor_id
        self.name = name
        self.specialty = specialty
        self.available_hours = available_hours

    def get_available_times(self, date):
        return [dt for dt in self.available_hours if dt.date() == date]

    def view_appointments(self, appointments):
        return [app for app in appointments if app.doctor == self]


class Specialty:
    def __init__(self, name):
        self.name = name


class Appointment:
    def __init__(self, appointment_id, patient, doctor, scheduled_time, status="Scheduled"):
        self.appointment_id = appointment_id
        self.patient = patient
        self.doctor = doctor
        self.scheduled_time = scheduled_time
        self.status = status

    def mark_completed(self):
        self.status = "Completed"

    def mark_no_show(self):
        self.status = "No Show"


class Availability:
    def __init__(self, doctor_id, available_hours):
        self.doctor_id = doctor_id
        self.available_hours = available_hours


class Report:
    @staticmethod
    def generate_total_appointments(appointments):
        return len(appointments)

    @staticmethod
    def generate_appointments_by_doctor(appointments):
        report = {}
        for appointment in appointments:
            doctor_id = appointment.doctor.doctor_id
            if doctor_id not in report:
                report[doctor_id] = 0
            report[doctor_id] += 1
        return report

    @staticmethod
    def generate_appointments_by_specialty(appointments):
        report = {}
        for appointment in appointments:
            specialty_name = appointment.doctor.specialty.name
            if specialty_name not in report:
                report[specialty_name] = 0
            report[specialty_name] += 1
        return report

    @staticmethod
    def generate_cancelled_appointments(appointments):
        return len([a for a in appointments if a.status == "Cancelled"])

    @staticmethod
    def generate_completed_appointments(appointments):
        return len([a for a in appointments if a.status == "Completed"])