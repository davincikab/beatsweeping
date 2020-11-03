from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from django.http import HttpResponse, JsonResponse

def send_activation_mail(to_address, message, subject):
    from_address = settings.EMAIL_HOST_USER
    msg = MIMEText(message)
    msg['From'] = from_address
    msg['to'] = to_address
    msg['Subject'] = subject

    try:      
        smtp = smtplib.SMTP(settings.EMAIL_HOST)
        smtp.starttls()
        smtp.login(from_address, settings.EMAIL_HOST_PASSWORD)
        smtp.sendmail(from_address, to_address, msg.as_string())
        smtp.quit()
        return "Success"
    except smtplib.SMTPException as error:
        print(error)
        return JsonResponse({'message':'error', 'error':"SMTP Error"})