# Rest-API
1.	Required python libraries: Flask, Werkzeug, OS
2.	How to run the application: run the main.py file using a python IDE then you can access the interface at the local address http://127.0.0.1:5000 .
3.	How to use the application:
•	You will be asked to login using an account already registered in the database. If the account does not exist, you can create one using the Sign Up page (see Apendix for available accounts).
•	I mainly use the Sign Up page to add a manager for the database, but it is possible to add other roles like Doctor or Assistant in the current version. (Roles must be written in this format so they could work: Manager, Doctor, Assistant)
•	After a successful Sign Up or Login, you will be redirected to the main page, where you can access (depending on the role) the following sections: Treatments (accessed by Manager and Doctor), Doctors (accessed by Manager) Assistants (accessed by Manager) and Patients (accessed by Manager and Doctor). The Home page can be accessed by everyone, including the Assistant.
•	In the Treatments section you can find two toggles: Display Treatments and Add Treatments. If you toggle Display Treatments you will be able to see a table with the name of the treatments and the date they’ve been available. Also, there is an extra column which contains the capabilities to delete or update a specific entry in the database. If you toggle Add Treatments you will be able to add a new treatment to the database.
•	The Doctors section is similar to the previously mentioned section, and there is also an additional toggle named Doctors Report which contains informations about what patients has a respective doctor (if it has) and two statistics that show the number of doctors and the number of patients in the system.
•	The Assistants section is similar to the Treatments section.
•	The Patients section is also similar to the Treatments section. This section has also 2 additional actions in the actions column: an action to assign a patient to a specific doctor or a specific assistant. In the current version you need to specific the first name and last name of the doctor/assistant you want to assign the patient to.
•	The last section available is the Logout section which will remove the user’s access to the described sections.

Apendix
Managers:
•	luca.andrei65@yahoo.com
Doctors:
•	tom_aurel@gmail.com 
•	otto_von_bismark@yahoo.com 
Assistants: 
•	ana_valentin@gmail.com 
•	marcus_aurelius@yahoo.com 
Patients (they do not have accounts, but are registered using an email):
•	pompeius_magnus@gmail.com 
•	iulius_cezar@yahoo.com 
Passwords: the password is universal for all accounts: 1234567.
