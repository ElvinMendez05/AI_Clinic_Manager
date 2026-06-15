
import gradio as gr
from datetime import datetime, date, timedelta
from appointment_management import AppointmentManagementSystem, Patient, Doctor, Specialty, Appointment, Availability, Report

# Instantiate the Appointment Management System
ams = AppointmentManagementSystem()

def register_patient(name, dob, contact_info):
    patient = ams.register_patient(name, dob, contact_info)
    return f"Patient Registered: {patient.name}, ID: {patient.patient_id}"

def register_doctor(name, specialty_name, available_start_hour, available_end_hour):
    specialty = next((s for s in ams.specialties if s.name == specialty_name), None)
    if not specialty:
        specialty = ams.add_specialty(specialty_name)
    available_hours = [datetime.combine(date.today(), datetime.min.time()) + timedelta(hours=i) for i in range(available_start_hour, available_end_hour)]
    doctor = ams.register_doctor(name, specialty, available_hours)
    return f"Doctor Registered: {doctor.name}, ID: {doctor.doctor_id}"

def create_specialty(name):
    specialty = ams.add_specialty(name)
    return f"Specialty Created: {specialty.name}"

def schedule_appointment(patient_id, doctor_id, scheduled_time):
    scheduled_time = datetime.fromisoformat(scheduled_time)
    appointment = ams.schedule_appointment(patient_id, doctor_id, scheduled_time)
    if appointment:
        return f"Appointment Scheduled: {appointment.appointment_id}"
    return "Failed to schedule appointment. Check for conflicts or invalid IDs."

def cancel_appointment(appointment_id):
    success = ams.cancel_appointment(appointment_id)
    if success:
        return "Appointment Cancelled"
    return "Failed to cancel appointment. Invalid ID."

def reschedule_appointment(appointment_id, new_time):
    new_time = datetime.fromisoformat(new_time)
    appointment = ams.reschedule_appointment(appointment_id, new_time)
    if appointment:
        return f"Appointment Rescheduled to {appointment.scheduled_time}"
    return "Failed to reschedule appointment. Check for availability conflicts."

def view_appointments():
    return [(app.appointment_id, app.patient.name, app.doctor.name, app.scheduled_time.isoformat(), app.status) for app in ams.appointments]

def search_appointments(filter_by, filter_value):
    if filter_by == "date":
        filter_value = datetime.fromisoformat(filter_value).date()
    results = ams.search_appointments(filter_by, filter_value)
    return [(app.appointment_id, app.patient.name, app.doctor.name, app.scheduled_time.isoformat(), app.status) for app in results]

def generate_report(report_type):
    result = ams.generate_report(report_type)
    return str(result)

with gr.Blocks() as demo:
    with gr.Tab("Register Patient"):
        name = gr.Textbox(label="Patient Name")
        dob = gr.Textbox(label="Date of Birth (YYYY-MM-DD)")
        contact_info = gr.Textbox(label="Contact Info")
        btn_register_patient = gr.Button("Register Patient")
        result_register_patient = gr.Textbox(label="Result")
        
        btn_register_patient.click(register_patient, [name, dob, contact_info], result_register_patient)

    with gr.Tab("Register Doctor"):
        doctor_name = gr.Textbox(label="Doctor Name")
        specialty_name = gr.Textbox(label="Specialty Name")
        available_start_hour = gr.Number(label="Available Start Hour")
        available_end_hour = gr.Number(label="Available End Hour")
        btn_register_doctor = gr.Button("Register Doctor")
        result_register_doctor = gr.Textbox(label="Result")
        
        btn_register_doctor.click(register_doctor, [doctor_name, specialty_name, available_start_hour, available_end_hour], result_register_doctor)

    with gr.Tab("Create Specialty"):
        specialty_name_create = gr.Textbox(label="Specialty Name")
        btn_create_specialty = gr.Button("Create Specialty")
        result_create_specialty = gr.Textbox(label="Result")
        
        btn_create_specialty.click(create_specialty, specialty_name_create, result_create_specialty)

    with gr.Tab("Schedule Appointment"):
        patient_id = gr.Number(label="Patient ID")
        doctor_id = gr.Number(label="Doctor ID")
        scheduled_time = gr.Textbox(label="Scheduled Time (YYYY-MM-DDTHH:MM:SS)")
        btn_schedule_appointment = gr.Button("Schedule Appointment")
        result_schedule_appointment = gr.Textbox(label="Result")
        
        btn_schedule_appointment.click(schedule_appointment, [patient_id, doctor_id, scheduled_time], result_schedule_appointment)

    with gr.Tab("Cancel Appointment"):
        appointment_id_cancel = gr.Number(label="Appointment ID")
        btn_cancel_appointment = gr.Button("Cancel Appointment")
        result_cancel_appointment = gr.Textbox(label="Result")
        
        btn_cancel_appointment.click(cancel_appointment, appointment_id_cancel, result_cancel_appointment)

    with gr.Tab("Reschedule Appointment"):
        appointment_id_reschedule = gr.Number(label="Appointment ID")
        new_time = gr.Textbox(label="New Time (YYYY-MM-DDTHH:MM:SS)")
        btn_reschedule_appointment = gr.Button("Reschedule Appointment")
        result_reschedule_appointment = gr.Textbox(label="Result")
        
        btn_reschedule_appointment.click(reschedule_appointment, [appointment_id_reschedule, new_time], result_reschedule_appointment)

    with gr.Tab("View Appointments"):
        btn_view_appointments = gr.Button("View Appointments")
        result_view_appointments = gr.Dataframe(headers=["ID", "Patient", "Doctor", "Time", "Status"])
        
        btn_view_appointments.click(view_appointments, None, result_view_appointments)

    with gr.Tab("Search Appointments"):
        filter_by = gr.Dropdown(choices=["patient", "doctor", "specialty", "date"], label="Filter By")
        filter_value = gr.Textbox(label="Filter Value")
        btn_search_appointments = gr.Button("Search Appointments")
        result_search_appointments = gr.Dataframe(headers=["ID", "Patient", "Doctor", "Time", "Status"])
        
        btn_search_appointments.click(search_appointments, [filter_by, filter_value], result_search_appointments)

    with gr.Tab("Generate Report"):
        report_type = gr.Dropdown(choices=["total_appointments", "appointments_by_doctor", "appointments_by_specialty", "cancelled_appointments", "completed_appointments"], label="Report Type")
        btn_generate_report = gr.Button("Generate Report")
        result_generate_report = gr.Textbox(label="Result")
        
        btn_generate_report.click(generate_report, report_type, result_generate_report)

demo.launch()
