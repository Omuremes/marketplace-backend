from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.infrastructure.config.settings import settings

engine = create_async_engine(
    settings.async_database_url,
    echo=False,
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()

async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
