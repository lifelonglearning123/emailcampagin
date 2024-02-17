import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Streamlit interface
def send_email(final_response):

    final_response = str(final_response)
    print("\n\n*******************************************************")
    # Email settings
    sender_email = "chao@macaws.ai"
    receiver_email = "chao@macaws.ai"
    password = os.getenv("EMAIL_PASSWORD")
    smtp_server = "smtp.ionos.co.uk"
    port = 587  # For starttls

    # Create message
    message = MIMEMultipart("alternative")
    message["Subject"] = "RandD AI generation"
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Text"] = final_response

    # Create the plain-text version of your message
    text = final_response
    part1 = MIMEText(text, "plain")

    # Attach parts to message
    message.attach(part1)  # Corrected to attach the MIMEText part



    # Send email
    try:
        # Connect to the server and send the email
        server = smtplib.SMTP(smtp_server,port)
        server.starttls() # Secure the connection
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        st.success("Email sent successfully!")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

