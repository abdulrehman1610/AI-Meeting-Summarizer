import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(recipient_email, subject, summary, action_items):
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    sender_email = os.getenv("SMTP_EMAIL")
    sender_password = os.getenv("SMTP_PASSWORD")
    
    if not sender_email or not sender_password:
        return False, "SMTP credentials not configured in .env"
        
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Format body
        body = f"<h2>Meeting Summary</h2>\n<p>{summary}</p>\n"
        body += "<h2>Action Items</h2>\n<ul>\n"
        for item in action_items:
            task = item.get('task', 'No task')
            assigned_to = item.get('assigned_to', 'Unassigned')
            deadline = item.get('deadline', 'None') or 'None'
            body += f"<li><strong>{task}</strong> (Assigned to: {assigned_to}, Deadline: {deadline})</li>\n"
        body += "</ul>"
        
        msg.attach(MIMEText(body, 'html'))
        
        # Connect to server and send
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls() # Secure the connection
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        return True, "Email sent successfully!"
    except Exception as e:
        return False, f"Error sending email: {e}"
