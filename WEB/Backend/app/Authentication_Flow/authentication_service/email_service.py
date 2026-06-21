import boto3
from botocore.exceptions import ClientError
from ...utils.config import setting
from fastapi import HTTPException,status

def get_ses_client():
    return boto3.client('ses',region_name=setting.AWS_REGION,
                        aws_secret_access_key=setting.AWS_SECRET_ACCESS_KEY,
                        aws_access_key_id=setting.AWS_SECRET_KEY_ID)

def send_email(to_email:str,subject:str,body:str):
    try:
        print(f"Sending OTP B - To Mail: {to_email} | From Mail : {setting.SES_FROM_EMAIL}")
        get_ses_client().send_email(
            Source=setting.SES_FROM_EMAIL,
            Destination={"ToAddresses":[to_email]},
            Message={
                "Subject":{"Data":subject},
                "Body":{"Text":{"Data":body}},
            })
        print(f"Sent OTP B - {to_email}")

    except ClientError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Unable to send the email --{e}")



def send_otp_email(email:str,otp:str):
    print(f"Sending OTP A - {email}")
    send_email(email,
               "Your login otp",
               f"Please enter you {otp}")
    

def send_actvation_link_email(email:str,otp:str):
    print(f"Sending activation link {email}")
    activation_link="http://localhost:5173/activate-admin"
    body=f"Activation otp is {otp} and Activation link is {activation_link}"
    send_email(email,
               "Activate admin",body)