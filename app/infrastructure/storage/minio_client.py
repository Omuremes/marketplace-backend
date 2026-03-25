from minio import Minio
from minio.error import S3Error
import io
import uuid
from app.infrastructure.config.settings import settings
from datetime import timedelta

class MinioStorageClient:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
            region="us-east-1"
        )
        # Client specifically initialized with the public endpoint
        # so that presigned URLs are signed for the correct Host header.
        public_endpoint = getattr(settings, "MINIO_PUBLIC_ENDPOINT", "localhost:9000")
        self.presigned_client = Minio(
            public_endpoint,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
            region="us-east-1"
        )
        self.bucket_name = settings.MINIO_BUCKET_NAME
        self._ensure_bucket()

    def _ensure_bucket(self):
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except S3Error as e:
            print(f"MinIO bucket error: {e}")

    def upload_file(self, filename: str, content: bytes, content_type: str = "image/jpeg") -> str:
        unique_name = f"{uuid.uuid4()}-{filename}"
        self.client.put_object(
            self.bucket_name,
            unique_name,
            io.BytesIO(content),
            length=len(content),
            content_type=content_type
        )
        return unique_name

    def get_file_url(self, object_key: str) -> str:
        if object_key.startswith("http://") or object_key.startswith("https://"):
            return object_key
            
        # Generate the presigned URL using the presigned_client (signed for localhost:9000)
        url = self.presigned_client.presigned_get_object(self.bucket_name, object_key, expires=timedelta(hours=1))
        return url

minio_client = MinioStorageClient()

def get_storage_client() -> MinioStorageClient:
    return minio_client
