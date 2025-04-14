import hashlib 
from django.conf import settings
from django.core.mail import send_mail
def generate_hash(str):
    result = hashlib.sha256(str.encode()) 
    return result.hexdigest()

def send_match_result(email,email_token):
    print('sending email to ',email," with token ",email_token)

    subject = "We found your item!"
    email_from =settings.EMAIL_HOST_USER
    message = email_token
    send_mail(subject,message,email_from,[email])


def send_forgot_mail(email, email_token):
    print('Sending password reset email to', email, "with token", email_token)

    subject = "Reset Your Password - Findzy"
    email_from = settings.EMAIL_HOST_USER
    message = f"""Hi,

    We received a request to reset your Findzy account password.

    Click the link below to reset your password:
    http://127.0.0.1:8000/users/forgotpassword/{email_token}

    If you did not request this, please ignore this email.

    Regards,  
    Findzy Team
    """
    send_mail(subject, message, email_from, [email])
    print("forgot mail sent successfully")


def send_account_activation_email(email, email_token):
    print('Sending account activation email to', email, "with token", email_token)

    subject = "Activate Your Findzy Account"
    email_from = settings.EMAIL_HOST_USER
    message = f"""Hi,

    Thank you for registering with Findzy!

    Please click the link below to activate your account:
    http://127.0.0.1:8000/users/verify/{email_token}

    If you did not create this account, you can safely ignore this email.

    Regards,  
    Findzy Team
    """
    send_mail(subject, message, email_from, [email])
