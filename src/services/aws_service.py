import os
from datetime import datetime
from io import BytesIO

import boto3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class AWSService:
    def __init__(self):
        
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION"),
        )
        self.ses = boto3.client(
            "ses",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION"),
        )

    def generate_pdf(self, note, client, items) -> BytesIO:
        buf = BytesIO()
        c = canvas.Canvas(buf, pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(72, 750, f"Folio: {note.folio}")
        c.drawString(72, 735, f"Cliente: {client.razon_social} ({client.rfc})")
        c.drawString(72, 720, f"Email: {client.email}")
        y = 700
        c.drawString(72, y, "Items:")
        y -= 15
        for itm in items:
            line = f"{itm.product.name}  {itm.quantity} x {itm.unit_price} = {itm.total}"
            c.drawString(80, y, line)
            y -= 15
            if y < 72:
                c.showPage()
                y = 750
        c.drawString(72, 60, f"Total: {note.total}")
        c.showPage()
        c.save()
        buf.seek(0)
        return buf

    def upload_pdf(self, pdf_buffer: BytesIO, bucket: str, rfc: str, folio: str) -> str:
        """Upload the buffer to S3 and return the object key."""
        key = f"{rfc}/{folio}.pdf"
        metadata = {
            "hora-envio": datetime.utcnow().isoformat(),
            "nota-descargada": "false",
            "veces-enviado": "1",
        }
        self.s3.upload_fileobj(
            pdf_buffer,
            bucket,
            key,
            ExtraArgs={"Metadata": metadata, "ContentType": "application/pdf"},
        )
        return key

    def send_notification(self, to_address: str, subject: str, body: str) -> dict:
        
        sender = os.getenv("AWS_SES_SENDER", to_address)
        return self.ses.send_email(
            Source=sender,
            Destination={"ToAddresses": [to_address]},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": body}},
            },
        )
