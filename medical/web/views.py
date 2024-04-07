from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Treatment, Role, Patient
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/treatments', methods=['GET', 'POST'])
@login_required
def treatments():
    user_assistant = User.query.join(Role).filter(User.id == current_user.id, Role.role_name == 'Assistant').first()
    if user_assistant:
        flash('You do not have permission to access this page!', 'error')
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        # Adding a new treatment
        if request.form.get('action') == 'add_treatment':
            treatment = request.form.get('treatment')

            if len(treatment) < 3:
                flash('Treatment must be at least 3 characters long!', category='error')
            else:
                treatment = Treatment(data=treatment)
                db.session.add(treatment)
                db.session.commit()
                flash('Treatment successfully added!', category='success')
                return redirect(url_for('views.treatments'))

        # Updating a treatment
        elif request.form.get('action') == 'update_treatment':
            treatment_id = request.form.get('treatment_id')
            treatment = Treatment.query.get(treatment_id)
            if treatment:
                # Update treatment details
                data = request.form.get('newTreatment')
                if data:
                    treatment.data = data
                db.session.commit()
                flash('Treatment details updated!', category='success')
            else:
                flash('Treatment not found!', category='error')
            return redirect(url_for('views.treatments'))

        # Deleting a treatment
        elif request.form.get('action') == 'delete_treatment':
            treatment_id = request.form.get('treatment_id')
            treatment = Treatment.query.get(treatment_id)
            if treatment:
                db.session.delete(treatment)
                db.session.commit()
                flash('Treatment deleted successfully!', category='success')
            else:
                flash('Treatment not found!', category='error')
            return redirect(url_for('views.treatments'))

        # Fetch all treatments for display
    treatment = Treatment.query.all()
    return render_template('treatments.html', user=current_user, treatment=treatment)


@views.route('/doctors', methods=['GET', 'POST'])
@login_required
def doctors():
    user_manager = User.query.join(Role).filter(User.id == current_user.id, Role.role_name == 'Manager').first()
    if not user_manager:
        flash('You do not have permission to access this page!', 'error')
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        # Adding a new doctor
        if request.form.get('action') == 'add_doctor':
            email = request.form.get('email')
            first_name = request.form.get('firstName')
            last_name = request.form.get('lastName')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')

            user = User.query.filter_by(email=email).first()
            if user:
                flash('There is already an user associated with this email!', category='error')

            if len(email) < 4:
                flash('Email length must be greater than 3 characters!', category='error')
            elif len(first_name) < 2:
                flash('First name length must be greater than 1 character!', category='error')
            elif len(last_name) < 2:
                flash('Last name length must be greater than 1 character!', category='error')
            elif password1 != password2:
                flash('Passwords don\'t match', category='error')
            elif len(password1) < 7:
                flash('Password must have at least 7 characters! ', category='error')
            else:
                doctor = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
                db.session.add(doctor)
                db.session.commit()
                new_user_id = doctor.id
                role = Role(role_name="Doctor", user_role_id=new_user_id)
                db.session.add(role)
                db.session.commit()
                flash('Doctor successfully added!', category='success')
                return redirect(url_for('views.doctors'))

        # Updating a doctor
        elif request.form.get('action') == 'update_doctor':
            doctor_id = request.form.get('doctor_id')
            doctor = User.query.get(doctor_id)
            if doctor:
                # Update doctor details
                email = request.form.get('newEmail')
                first_name = request.form.get('newFirstName')
                last_name = request.form.get('newLastName')
                if email:
                    doctor.email = email
                if first_name:
                    doctor.first_name = first_name
                if last_name:
                    doctor.last_name = last_name
                db.session.commit()
                flash('Doctor details updated!', category='success')
            else:
                flash('Doctor not found!', category='error')
            return redirect(url_for('views.doctors'))

        # Deleting a doctor
        elif request.form.get('action') == 'delete_doctor':
            doctor_id = request.form.get('doctor_id')
            doctor = User.query.get(doctor_id)
            if doctor:
                role = Role.query.filter_by(user_role_id=doctor_id).first()
                if role:
                    db.session.delete(role)
                db.session.delete(doctor)
                db.session.commit()
                flash('Doctor deleted successfully!', category='success')
            else:
                flash('Doctor not found!', category='error')
            return redirect(url_for('views.doctors'))

        # Fetch all doctors for display
    doctor = User.query.join(Role).filter(Role.role_name == 'Doctor').all()
    # After processing the form submissions, generate the report
    report = generate_report_data()
    return render_template('doctors.html', user=current_user, doctor=doctor, report=report)


def generate_report_data():
    doctors_with_patients = {}
    # Query all doctors and their associated patients
    for doctor in User.query.join(Role).filter(Role.role_name == 'Doctor').all():
        # Corrected placement of the variable definition
        patient = [patient.first_name + ' ' + patient.last_name for patient in doctor.patients]
        doctors_with_patients[doctor.first_name + ' ' + doctor.last_name] = patient

    # Calculate statistics
    total_doctors = len(doctors_with_patients)
    total_patients = sum(len(patient) for patient in doctors_with_patients.values())

    return {
        'doctors_with_patients': doctors_with_patients,
        'statistics': {
            'total_doctors': total_doctors,
            'total_patients': total_patients
        }
    }


@views.route('/assistants', methods=['GET', 'POST'])
@login_required
def assistants():
    user_manager = User.query.join(Role).filter(User.id == current_user.id, Role.role_name == 'Manager').first()
    if not user_manager:
        flash('You do not have permission to access this page!', 'error')
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        # Adding a new assistant
        if request.form.get('action') == 'add_assistant':
            email = request.form.get('email')
            first_name = request.form.get('firstName')
            last_name = request.form.get('lastName')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')

            user = User.query.filter_by(email=email).first()
            if user:
                flash('There is already an user associated with this email!', category='error')

            if len(email) < 4:
                flash('Email length must be greater than 3 characters!', category='error')
            elif len(first_name) < 2:
                flash('First name length must be greater than 1 character!', category='error')
            elif len(last_name) < 2:
                flash('Last name length must be greater than 1 character!', category='error')
            elif password1 != password2:
                flash('Passwords don\'t match', category='error')
            elif len(password1) < 7:
                flash('Password must have at least 7 characters! ', category='error')
            else:
                assistant = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
                db.session.add(assistant)
                db.session.commit()
                # assistant_id = assistant.id
                role = Role(role_name="Assistant", user_role_id=assistant.id)
                db.session.add(role)
                db.session.commit()
                flash('Assistant successfully added!', category='success')
                return redirect(url_for('views.assistants'))

        # Updating a patient
        elif request.form.get('action') == 'update_assistant':
            assistant_id = request.form.get('assistant_id')
            assistant = User.query.get(assistant_id)
            if assistant:
                # Update assistant details
                email = request.form.get('newEmail')
                first_name = request.form.get('newFirstName')
                last_name = request.form.get('newLastName')
                if email:
                    assistant.email = email
                if first_name:
                    assistant.first_name = first_name
                if last_name:
                    assistant.last_name = last_name
                db.session.commit()
                flash('Assistant details updated!', category='success')
            else:
                flash('Assistant not found!', category='error')
            return redirect(url_for('views.assistants'))

        # Deleting an assistant
        elif request.form.get('action') == 'delete_assistant':
            assistant_id = request.form.get('assistant_id')
            assistant = User.query.get(assistant_id)
            if assistant:
                role = Role.query.filter_by(user_role_id=assistant_id).first()
                if role:
                    db.session.delete(role)
                db.session.delete(assistant)
                db.session.commit()
                flash('Assistant deleted successfully!', category='success')
            else:
                flash('Assistant not found!', category='error')
            return redirect(url_for('views.assistants'))

        # Fetch all assistants for display
    assistant = User.query.join(Role).filter(Role.role_name == 'Assistant').all()
    return render_template('assistants.html', user=current_user, assistant=assistant)


@views.route('/patients', methods=['GET', 'POST'])
@login_required
def patients():
    user_assistant = User.query.join(Role).filter(User.id == current_user.id, Role.role_name == 'Assistant').first()
    if user_assistant:
        flash('You do not have permission to access this page!', 'error')
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        # Adding a new patient
        if request.form.get('action') == 'add_patient':
            email = request.form.get('email')
            first_name = request.form.get('firstName')
            last_name = request.form.get('lastName')
            patient = Patient(email=email, first_name=first_name, last_name=last_name)
            db.session.add(patient)
            db.session.commit()
            flash('Patient successfully added!', category='success')
            return redirect(url_for('views.patients'))

        # Updating a patient
        elif request.form.get('action') == 'update_patient':
            patient_id = request.form.get('patient_id')
            patient = Patient.query.get(patient_id)
            if patient:
                # Update patient details
                email = request.form.get('newEmail')
                first_name = request.form.get('newFirstName')
                last_name = request.form.get('newLastName')
                if email:
                    patient.email = email
                if first_name:
                    patient.first_name = first_name
                if last_name:
                    patient.last_name = last_name
                db.session.commit()
                flash('Patient details updated!', category='success')
            else:
                flash('Patient not found!', category='error')
            return redirect(url_for('views.patients'))

        # Deleting a patient
        elif request.form.get('action') == 'delete_patient':
            patient_id = request.form.get('patient_id')
            patient = Patient.query.get(patient_id)
            if patient:
                db.session.delete(patient)
                db.session.commit()
                flash('Patient deleted successfully!', category='success')
            else:
                flash('Patient not found!', category='error')
            return redirect(url_for('views.patients'))

        # Assigning a patient to a doctor
        elif request.form.get('action') == 'assign_doctor':
            patient_id = request.form.get('patient_id')
            doctor_first_name = request.form.get('doctor_first_name')
            doctor_last_name = request.form.get('doctor_last_name')
            doctor = User.query.filter_by(first_name=doctor_first_name, last_name=doctor_last_name).first()
            if doctor:
                patient = Patient.query.get(patient_id)
                if patient:
                    doctor.patients.append(patient)
                    db.session.commit()
                    flash('Patient assigned to doctor successfully!', category='success')
                else:
                    flash('Patient not found!', category='error')
            else:
                flash('Doctor not found!', category='error')
            return redirect(url_for('views.patients'))

        # Assigning a assistant to a doctor
        elif request.form.get('action') == 'assign_assistant':
            patient_id = request.form.get('patient_id')
            assistant_first_name = request.form.get('assistant_first_name')
            assistant_last_name = request.form.get('assistant_last_name')
            assistant = User.query.filter_by(first_name=assistant_first_name, last_name=assistant_last_name).first()
            if assistant:
                patient = Patient.query.get(patient_id)
                if patient:
                    assistant.patients.append(patient)
                    db.session.commit()
                    flash('Patient assigned to assistant successfully!', category='success')
                else:
                    flash('Patient not found!', category='error')
            else:
                flash('Assistant not found!', category='error')
            return redirect(url_for('views.patients'))
    # Fetch all patients for display
    patient = Patient.query.all()

    return render_template('patients.html', user=current_user, patient=patient)
