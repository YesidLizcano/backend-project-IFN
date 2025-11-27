from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
import os
import tempfile

class EmailService:
    def __init__(self):
        # Configuración para usar con Contraseña de Aplicación
        mail_username = os.getenv("MAIL_USERNAME", "")
        mail_port = int(os.getenv("MAIL_PORT", 587))
        
        # Detección automática del servidor SMTP según el dominio
        mail_server = os.getenv("MAIL_SERVER")
        if not mail_server:
            domain = mail_username.split("@")[-1].lower() if "@" in mail_username else ""
            if domain in ["udi.edu.co", "outlook.com", "hotmail.com", "live.com", "office365.com"]:
                mail_server = "smtp.office365.com"
            else:
                mail_server = "smtp.gmail.com"

        # Ajuste automático de SSL/TLS según el puerto
        use_ssl = mail_port == 465
        use_tls = mail_port == 587
        
        print(f"Email Config: Server={mail_server}, Port={mail_port}, SSL={use_ssl}, TLS={use_tls}")

        self.conf = ConnectionConfig(
            MAIL_USERNAME = mail_username,
            MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "password"),
            MAIL_FROM = os.getenv("MAIL_FROM", mail_username),
            MAIL_PORT = mail_port,
            MAIL_SERVER = mail_server,
            MAIL_STARTTLS = use_tls,
            MAIL_SSL_TLS = use_ssl,
            USE_CREDENTIALS = True,
            VALIDATE_CERTS = False
        )

    async def send_email_with_pdf(self, email_to: EmailStr, subject: str, body: str, pdf_content: bytes, pdf_filename: str):
        # Create a temporary file for the attachment
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf_content)
            tmp_path = tmp.name
            
        try:
            message = MessageSchema(
                subject=subject,
                recipients=[email_to],
                body=body,
                subtype=MessageType.html,
                attachments=[tmp_path]
            )
            fm = FastMail(self.conf)
            await fm.send_message(message)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
