import smtplib
import os
from typing import List, Optional, Union
from io import BytesIO
import logging

from email.message import EmailMessage
from email_validator import validate_email


def send_email_simple(smtp_host: str, creds: tuple, dest_address: str, body: bytes, subject: str, smptp_port=465):
    """
    For more control, copy this code and make your own implementation.
    possibly raises:
    - EmailNotValidError
    Args:
        attachments: list of paths, or list of BytesIO objects
        smtp_user:
        creds:
        dest_address:
        body:
        subject:
        smptp_port: 465

    Returns:

    """
    msg = EmailMessage()
    # if isinstance(attachments, list):
    #     for attachment in attachments:
    #         if isinstance(attachment, str):
    #             if not os.path.isfile(attachment):
    #                 e = 1
    #             f = open(attachment, "rb")
    #             body = f.read()
    #             f.close()
    # msg.add_attachment()

    _dest_address = validate_email(dest_address).email
    subject = subject.replace("\r", "")
    subject = subject.replace("\n", "")

    msg['Subject'] = subject
    msg['From'] = creds[0]
    msg['To'] = _dest_address

    # server
    server = smtplib.SMTP_SSL(smtp_host, smptp_port)
    server.login(*creds)
    server.send_message(msg)
    server.quit()

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()