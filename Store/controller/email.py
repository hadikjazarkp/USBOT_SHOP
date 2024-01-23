from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings






def send_otp_email(email, username, otp):
    
    html_content = render_to_string(
        'store/auth/emailOTP.html', {'username': username, 'otp': otp})
    
    subject = 'Account verification OTP'
    send_mail(subject, '',settings.EMAIL_HOST_USER,
              [email], html_message=html_content)
   
   
   
def reset_password_email(email,reset_link):
     subject =  'Password Reset Request'
     message = f'Click the following link to reset your password: {reset_link}\n This link will expaire within i min'
     form_email = settings.EMAIL_HOST_USER
     recipient_list = [email]
     send_mail(subject, message, form_email, recipient_list)  