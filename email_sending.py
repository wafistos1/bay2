def email_sending(request, email, data, subject, path_temp, auto_notif=True):
    # General sending
    email_subject = subject
    email_template = path_temp

    email_body_html = render_to_string(email_template, data)
    email_body_text = strip_tags(email_body_html)

    if auto_notif:
        #no-reply for automatic notifications (like email verification and appointment taken)
        email_from = settings.EMAIL_HOST_USER

    else:
        #info for email sent in the homepage
        email_from = settings.EMAIL_SENDER_ID

    connection = get_connection(host=settings.EMAIL1_HOST, 
                    port=settings.EMAIL1_PORT, 
                    username=settings.EMAIL1_HOST_USER, 
                    password=settings.EMAIL1_HOST_PASSWORD, 
                    use_tls=settings.EMAIL1_USE_TLS)  # SMTP Credentials info/no-reply

    connection.open()

    email_send = EmailMultiAlternatives(
        email_subject,
        email_body_text,
        email_from,
        [email],
        connection=connection
    )
    email_send.attach_alternative(email_body_html, "text/html")
    email_send.send()

    connection.close() # Cleanup

def email_to_patient(request, patient, doctor, date_rdv, appointment):

    now = datetime.datetime.now()
    date_time_now = now.strftime("%b %d, %Y à %H:%M:%S")

    doc_first_name = doctor.first_name
    doc_last_name = doctor.last_name
    doc_phone = doctor.landline

    doc_address = doctor.address
    doc_url = doctor.url

    data = {
    'order_datetime': date_time_now,
    'appointment':appointment,
    'date_rdv': date_rdv,
    'name':patient.first_name,
    'first_name': doc_first_name,
    'last_name': doc_last_name,
    'phone': doc_phone,
    'address': doc_address,
    'url': doc_url,
    }

    email_sending(request, patient.email, data, subject='Nouveau rendez-vous', path_temp='dashboard/email/booking_confirmation_patient.html')

def email_to_doctor(request, patient, doctor, date_rdv, appointment):

    now = datetime.datetime.now()
    date_time_now = now.strftime("%b %d, %Y à %H:%M:%S")
    

    pat_first_name = patient.first_name
    pat_last_name = patient.last_name
    pat_phone = patient.phone

    data = {
    'order_datetime': date_time_now,
    'appointment':appointment,
    'date_rdv': date_rdv,
    'name':doctor.first_name,
    'first_name': pat_first_name,
    'last_name': pat_last_name,
    'phone': pat_phone,
    }

    email_sending(request, doctor.email, data, subject='Nouveau rendez-vous', path_temp='dashboard/email/booking_doctor.html')

def email_new_patient(request, patient, password):
    data = {
    'password':password,
    'patient':patient
    }

    email_sending(request, patient.email, data, subject='Bienvenue à Toubib!', path_temp='dashboard/email/appointment_new_patient.html')
