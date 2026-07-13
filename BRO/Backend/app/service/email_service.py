import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException, status

from app.utils.config import setting


def get_ses_client():
    if not all(
        [
            setting.AWS_SECRET_ACCESS_KEY,
            setting.AWS_SECRET_KEY_ID,
            setting.SES_FROM_EMAIL,
        ]
    ):
        return None

    return boto3.client(
        "ses",
        region_name=setting.AWS_REGION,
        aws_secret_access_key=setting.AWS_SECRET_ACCESS_KEY,
        aws_access_key_id=setting.AWS_SECRET_KEY_ID,
    )


def send_email(to_email: str, subject: str, body: str):
    client = get_ses_client()
    if client is None:
        print(f"[email skipped] To: {to_email} | Subject: {subject} | Body: {body}")
        return {"message": "Email skipped because SES is not configured"}

    try:
        client.send_email(
            Source=setting.SES_FROM_EMAIL,
            Destination={"ToAddresses": [to_email]},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": body}},
            },
        )
    except ClientError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Unable to send email: {exc}",
        ) from exc

    return {"message": "Email sent"}


def send_otp_email(email: str, otp: str):
    return send_email(
        email,
        "Your Talenta login OTP",
        f"Your Talenta login OTP is {otp}. It expires in 10 minutes.",
    )


def send_actvation_link_email(email: str, message: str):
    activation_link = "http://localhost:5173/login"
    body = f"{message}\n\nLogin here: {activation_link}"
    return send_email(email, "Welcome to Talenta", body)
