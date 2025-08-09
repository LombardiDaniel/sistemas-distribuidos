import services
from flask import request
from minio import Minio

# MinIO configurations
MINIO_ENDPOINT = "localhost:9000"
MINIO_ACCESS_KEY = "itiufscar"
MINIO_SECRET_KEY = "itiufscar"
MINIO_BUCKET_NAME = "ml-models"

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False,
)


class UserHandler:
    """handlers regarding invoices"""

    def __init__(
        self,
        user_service: services.UserService,
        cache_service: services.CacheService,
    ):
        self.user_service = user_service
        self.cache_service = cache_service

    def get_user_by_id(self, user_id: int) -> str:
        """get usr"""

        cache_key = f"users:{user_id}"

        user = self.cache_service.get(cache_key)
        if user is None:
            print(f"cache miss!: {user_id}")
            user = self.user_service.get_user_by_id(user_id)

        self.cache_service.set(cache_key, user, 60)

        return user

    def update_user_name(self, user_id: int) -> str:
        """update usr"""

        body = request.json

        cache_key = f"users:{user_id}"
        self.cache_service.delete(cache_key)
        self.user_service.update_user(user_id, str(body["name"]))

        return "OK"
