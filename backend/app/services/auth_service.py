"""
TeeDesign AI — Authentication Service
"""
from typing import Optional
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email.lower().strip())
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    stmt = select(User).where(User.username == username.lower().strip())
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def authenticate_user(
    db: AsyncSession,
    username_or_email: str,
    password: str,
) -> Optional[User]:
    identifier = username_or_email.lower().strip()
    stmt = select(User).where(
        or_(User.email == identifier, User.username == identifier)
    )
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def create_user(db: AsyncSession, user_create: UserCreate) -> User:
    hashed_pwd = hash_password(user_create.password)
    user = User(
        email=user_create.email.lower().strip(),
        username=user_create.username.lower().strip(),
        hashed_password=hashed_pwd,
        is_active=True,
        is_admin=user_create.is_admin,
        avatar_url=user_create.avatar_url,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user
