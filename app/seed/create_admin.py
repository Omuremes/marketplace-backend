import argparse
import asyncio
import sys
from pathlib import Path

# Allow running this script directly from any working directory.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

async def create_admin(email: str, password: str) -> int:
    try:
        from app.domain.entities.admin import Admin
        from app.infrastructure.auth.password import get_password_hash
        from app.infrastructure.db.session import AsyncSessionLocal
        from app.infrastructure.db.uow import SqlAlchemyUnitOfWork
    except ModuleNotFoundError as exc:
        if exc.name == "asyncpg":
            print("Missing dependency: asyncpg")
            print("Install project dependencies first (recommended via poetry install in marketplace-backend).")
            return 2
        raise

    uow = SqlAlchemyUnitOfWork(session_factory=AsyncSessionLocal)

    async with uow:
        existing = await uow.admins.get_by_email(email)
        if existing:
            print(f"Admin with email '{email}' already exists")
            return 1

        admin = Admin.create(email=email, password_hash=get_password_hash(password))
        await uow.admins.add(admin)
        await uow.commit()

    print(f"Admin created successfully: {email}")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    from app.infrastructure.config.settings import settings

    parser = argparse.ArgumentParser(description="Create an admin user in the database")
    parser.add_argument(
        "--email",
        default=settings.ADMIN_USERNAME,
        help="Admin email (default: ADMIN_USERNAME from .env)",
    )
    parser.add_argument(
        "--password",
        default=settings.ADMIN_PASSWORD,
        help="Admin password (default: ADMIN_PASSWORD from .env)",
    )
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    exit_code = asyncio.run(create_admin(email=args.email, password=args.password))
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
