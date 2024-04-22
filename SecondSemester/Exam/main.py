from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field
from uuid import uuid4, UUID
from typing import List

app = FastAPI(title="Medical Appointment API")

# Simulated Databases
db_patients = []
db_doctors = []
db_appointments = []

# Pydantic Models for Data Validation
class Patient(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    age: int
    sex: str
    weight: float
    height: float
    phone: str

class Doctor(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    specialization: str
    phone: str
    is_available: bool = True

class Appointment(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    patient_id: UUID
    doctor_id: UUID
    date: str
    completed: bool = False  # Indicates if the appointment is completed
    

@app.get("/")
def home():
    return "Hello from my API"

# CRUD Operations for Patients
@app.post("/patients/", response_model=Patient, status_code=status.HTTP_201_CREATED)
def create_patient(patient: Patient):
    db_patients.append(patient)
    return patient

@app.get("/patients/", response_model=List[Patient])
def read_patients():
    return db_patients

@app.get("/patients/{patient_id}",
 response_model=Patient)
def read_patient(patient_id: UUID):
    for patient in db_patients:
        if patient.id == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")

@app.put("/patients/{patient_id}", response_model=Patient)
def update_patient(patient_id: UUID, updated_patient: Patient):
    for idx, patient in enumerate(db_patients):
        if patient.id == patient_id:
            db_patients[idx] = updated_patient
            return updated_patient
    raise HTTPException(status_code=404, detail="Patient not found")

@app.delete("/patients/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: UUID):
    global db_patients
    db_patients = [patient for patient in db_patients if patient.id != patient_id]
    return {"message": "Patient deleted"}

# CRUD Operations for Doctors
@app.post("/doctors/", response_model=Doctor, status_code=status.HTTP_201_CREATED)
def create_doctor(doctor: Doctor):
    db_doctors.append(doctor)
    return doctor

@app.get("/doctors/", response_model=List[Doctor])
def read_doctors():
    return db_doctors

@app.get("/doctors/{doctor_id}", response_model=Doctor)
def read_doctor(doctor_id: UUID):
    for doctor in db_doctors:
        if doctor.id == doctor_id:
            return doctor
    raise HTTPException(status_code=404, detail="Doctor not found")

@app.put("/doctors/{doctor_id}", response_model=Doctor)
def update_doctor(doctor_id: UUID, updated_doctor: Doctor):
    for idx, doctor in enumerate(db_doctors):
        if doctor.id == doctor_id:
            db_doctors[idx] = updated_doctor
            return updated_doctor
    raise HTTPException(status_code=404, detail="Doctor not found")

@app.delete("/doctors/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(doctor_id: UUID):
    global db_doctors
    db_doctors = [doctor for doctor in db_doctors if doctor.id != doctor_id]
    return {"message": "Doctor deleted"}

# Appointment Management
@app.post("/appointments/", response_model=Appointment, status_code=status.HTTP_201_CREATED)
def create_appointment(appointment: Appointment):
    available_doctor = next((doctor for doctor in db_doctors if doctor.is_available), None)
    if not available_doctor:
        raise HTTPException(status_code=503, detail="No available doctors at the moment")
    available_doctor.is_available = False
    appointment.doctor_id = available_doctor.id
    db_appointments.append(appointment)
    return appointment

@app.get("/appointments/", response_model=List[Appointment])
def read_appointments():
    return db_appointments

@app.get("/appointments/{appointment_id}", response_model=Appointment)
def read_appointment(appointment_id: UUID):
    for appointment in db_appointments:
        if appointment.id == appointment_id:
            return appointment
    raise HTTPException(status_code=404, detail="Appointment not found")

@app.put("/appointments/complete/{appointment_id}", status_code=status.HTTP_200_OK)
def complete_appointment(appointment_id: UUID):
    for appointment in db_appointments:
        if appointment.id == appointment_id and not appointment.completed:
            appointment.completed = True
            for doctor in db_doctors:
                if doctor.id == appointment.doctor_id:
                    doctor.is_available = True
                    break
            return {"message": "Appointment completed and doctor is now available"}
    raise HTTPException(status_code=404, detail="Appointment not found or already completed")



@app.delete("/appointments/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_appointment(appointment_id: UUID, patient_id: UUID):
    for appointment in db_appointments:
        if appointment.id == appointment_id:
            if appointment.patient_id != patient_id:
                raise HTTPException(status_code=403, detail="Unauthorized: You can only cancel your own appointments")
            for doctor in db_doctors:
                if doctor.id == appointment.doctor_id:
                    doctor.is_available = True
                    break
            db_appointments.remove(appointment)
            return {"message": "Appointment cancelled and doctor is now available"}
    raise HTTPException(status_code=404, detail="Appointment not found")