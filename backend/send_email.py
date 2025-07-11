import os
import resend

resend.api_key = os.getenv("RESEND_API_KEY")
FROM_EMAIL = "newsletter@lsx.li"

def send_email(to, subject, content):
    params = {
        "from": FROM_EMAIL,
        "to": [to],
        "subject": subject,
        "html": content
    }
    email = resend.Emails.send(params)
    return email
