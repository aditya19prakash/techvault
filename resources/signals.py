from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Resource
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from techvault import settings
from .serializers import ResourceSignalsSerializerID
from aiservice.ai_summarizer import email_message_creation
User = get_user_model()

@receiver(post_save, sender=Resource)
def send_resource_added_email(sender, instance, created, **kwargs):
    if created:  # only when a new Resource is created
        sender = settings.SENDER  # your Zoho email
        app_password = settings.APP_PASSWORD  # Zoho App Password
        receiver = ["adyprakash19@gmail.com", "adiprakash1962001@gmail.com"]
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = ", ".join(receiver)
        msg["Subject"] = f"New resource added: {instance.title}"
        serializer = ResourceSignalsSerializerID(instance)

        body = email_message_creation(serializer.data)
        msg.attach(MIMEText(body, "plain"))
        
        server = smtplib.SMTP("smtp.zoho.in", 587)
        server.starttls()
        server.login(sender, app_password)
        server.send_message(msg)
        server.quit()

        print("Email sent successfully!")