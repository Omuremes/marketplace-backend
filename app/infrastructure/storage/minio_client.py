from minio import Minio
from minio.error import S3Error
import io
import uuid
from app.infrastructure.config.settings import settings

class MinioStorageClient:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )
        self.bucket_name = settings.MINIO_BUCKET_NAME
        self._ensure_bucket()

    def _ensure_bucket(self):
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                # Setting public policy for prototype simplicity
                policy = f'{{"Version":"2012-10-17","Statement":[{{"Effect":"Allow","Principal":{{"AWS":["*"]}},"Action":["s3:GetObject"],"Resource":["arn:aws:s3:::{self.bucket_name}/*"]}}]}}'
                self.client.set_bucket_policy(self.bucket_name, policy)
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
        # Using localhost public URL for prototype
        protocol = "https" if settings.MINIO_SECURE else "http"
        return f"{protocol}://{settings.MINIO_ENDPOINT}/{self.bucket_name}/{unique_name}"

minio_client = MinioStorageClient()

def get_storage_client() -> MinioStorageClient:
    return minio_client
