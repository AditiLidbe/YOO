from uuid import uuid4

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import HTTPException, UploadFile, status

from app.utils.config import setting


def get_s3_client():
    if not all(
        [
            setting.AWS_S3_BUCKET_NAME,
            setting.AWS_SECRET_KEY_ID,
            setting.AWS_SECRET_ACCESS_KEY,
        ]
    ):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="S3 is not configured",
        )

    return boto3.client(
        "s3",
        region_name=setting.AWS_REGION,
        aws_access_key_id=setting.AWS_SECRET_KEY_ID,
        aws_secret_access_key=setting.AWS_SECRET_ACCESS_KEY,
    )


def make_file_name(file: UploadFile):
    clean_name = file.filename.replace(" ", "_")
    return f"{uuid4()}_{clean_name}"


def upload_file(file: UploadFile, folder: str):
    client = get_s3_client()
    file_name = make_file_name(file)
    file_path = f"{folder}/{file_name}"

    try:
        client.upload_fileobj(
            file.file,
            setting.AWS_S3_BUCKET_NAME,
            file_path,
            ExtraArgs={"ContentType": file.content_type},
        )
    except (BotoCoreError, ClientError) as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not upload file to S3: {exc}",
        ) from exc

    return file_path


def get_file_url(file_path: str):
    client = get_s3_client()

    try:
        return client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": setting.AWS_S3_BUCKET_NAME,
                "Key": file_path,
            },
            ExpiresIn=3600,
        )
    except (BotoCoreError, ClientError) as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not create file URL: {exc}",
        ) from exc
