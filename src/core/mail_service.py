import os
from pathlib import Path
from typing import List, Any, Dict
from pydantic import EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

root_dir = os.getenv("ROOT")


email_template_path = (
    Path(root_dir) / "templates/email"
    if root_dir is not None
    else Path("templates/email")
)

conf = None


async def setup_email_connection():
    global conf
    conf = ConnectionConfig(
        MAIL_USERNAME=os.getenv("MAIL_USERNAME", "default_username"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "default_password"),
        MAIL_FROM=os.getenv("MAIL_FROM", "default_email@example.com"),
        MAIL_PORT=int(os.getenv("MAIL_PORT", "587")),
        MAIL_SERVER=os.getenv("MAIL_SERVER", "default_smtp_server.com"),
        MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME", "Default Name"),
        MAIL_SSL_TLS=False,
        MAIL_STARTTLS=True,
        USE_CREDENTIALS=True,
        TEMPLATE_FOLDER=email_template_path,
    )


async def send_email(subject: str, email: List[EmailStr], body: Dict[str, Any]):
    if conf:
        message = MessageSchema(
            subject=subject,
            recipients=email,
            template_body=body,
            subtype=MessageType.html,
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email.html")
    else:
        raise ValueError("Invalid email config")
