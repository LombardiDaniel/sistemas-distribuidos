"""
Checar interface: http://127.0.0.1:9001/ para criar o acesso
"""

import os

from minio import Minio
from minio.error import InvalidResponseError

# MinIO configurations
MINIO_ENDPOINT = "localhost:9000"
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_BUCKET_NAME = "ml-models"

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False,
)


def upload_model(model_path):
    try:
        # Check if the bucket exists, if not, create it
        if not minio_client.bucket_exists(MINIO_BUCKET_NAME):
            minio_client.make_bucket(MINIO_BUCKET_NAME)

        # Upload the model file to the MinIO bucket
        minio_client.fput_object(
            MINIO_BUCKET_NAME, os.path.basename(model_path), model_path
        )

        print("Model uploaded successfully!")

    except InvalidResponseError as err:
        print(err)


def download_model(model_name, save_path):
    try:
        # Download the model file from the MinIO bucket
        minio_client.fget_object(MINIO_BUCKET_NAME, model_name, save_path)

        print("Model downloaded successfully!")

    except InvalidResponseError as err:
        print(err)


# Example usage
if __name__ == "__main__":
    model_path = "models/HAR-CNN-Keras-model.h5"  # Path to your machine learning model
    upload_model(model_path)

    # Specify the name to download and save the model
    model_name = "HAR-CNN-Keras-model.h5"
    save_path = "downloaded_model.h5"
    download_model(model_name, save_path)
