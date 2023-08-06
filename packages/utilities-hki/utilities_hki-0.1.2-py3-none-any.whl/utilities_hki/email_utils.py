"""
Email utility functions.
Copyright (C) 2022 Humankind Investments
"""

from datetime import date
import smtplib
from email.mime.text import MIMEText


def send_email(content, subject, receiver, credentials):
    """
    Send an email alert.

    Parameters
    ----------
    content : str
        Content of the email to send.
    subject : str
        Subject of the email to send.
    receiver : str
        Email to send the alert to.
    credentials : dict
        Provides the credentials for sender, password, and port.
    """
    
    for key in ['sender', 'password', 'port']:
        assert key in credentials, f"credentials must have a key for {key}"
    
    sender = credentials['sender']
    passw = credentials['password']
    port = credentials['port']
    
    msg = MIMEText(content)
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.add_header('Content-Type', 'text/html')

    server = smtplib.SMTP('smtp.' + sender.split('@')[1], port)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(sender, passw)
    # server.sendmail(sender, receiver, msg.as_string())
    server.send_message(msg)
    server.quit()


def wrotetoday(platform, receivers, content, credentials):
    """
    Send an email notification that a script succeeded.

    Parameters
    ----------
    platform : str
        Name of the platform.
    receivers : list of str
        List of emails to send the alert to.
    content : str
        Content of the email alert.
    credentials : dict
        Provides the credentials for sender, password, and port.
    """
    
    subject = '[%s] finished writing %s' % (platform, date.today())

    if isinstance(receivers, list):
        receivers= ", ".join(receivers)
        send_email(content, subject, receivers, credentials)
    elif isinstance(receivers, str):
        send_email(content, subject, receivers, credentials)
    else:
        raise TypeError("receivers must be a str or list")

            
def error_alert(platform, receivers, filename, credentials):
    """
    Send an email alert that a script failed.

    Parameters
    ----------
    platform : str
        Name of the platform to be included in the subject line.
    receivers : list of str
        List of emails to send the alert to.
    filename : str
        Name of the script which ran into the error.
    credentials : dict
        Provides the credentials for sender, password, and port.
    """
    
    subject = '[ERROR] %s failed %s' % (platform, date.today())
    content = "{} did not run successfully. <br> Check log".format(filename)
    if isinstance(receivers, list):
        receivers= ", ".join(receivers)
        send_email(content, subject, receivers, credentials)
    elif isinstance(receivers, str):
        send_email(content, subject, receivers, credentials)
    else:
        raise TypeError("receivers must be a str or list")
    
    