from django.template.loader import get_template
from django.contrib.auth.models import User
from django.core.mail.message import EmailMultiAlternatives
from email.mime.image import MIMEImage
import os
from Sakura import settings

def send_email(email , tmp_name , data , title ):
    user = User.objects.get(email=email)
    message = get_template(tmp_name).render(data)
    mail = EmailMultiAlternatives(
                        title,
                        message,
                        from_email=settings.EMAIL_HOST_USER ,
                        to=[email],
                    )
    mail.mixed_subtype = 'related'
    # add img to email :
    mail.attach_alternative(message, "text/html")
    image = "reset_email_Sakura.png"
    file_path = os.path.join('static', image)
    with open(file_path, mode='rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-ID', '<{name}>'.format(name=image))
        img.add_header('Content-Disposition', 'inline', filename=image)
    mail.attach(img)
    mail.send()