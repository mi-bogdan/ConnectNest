from app.db.base import Base

from datetime import datetime

from sqlalchemy import Boolean, String, DateTime, func, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from typing import List


import uuid


class Communities(Base):
    """Сообщества"""

    __tablename__ = "communities"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="id сообщества"
    )
    title: Mapped[str] = mapped_column(
        String(160),
        nullable=False,
        comment="Заголовок"
    )
    description: Mapped[str] = mapped_column(
        Text, nullable=True,
        comment="Описание сообщества"
    )
    date_create: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        comment="Дата создания"
    )
    image_logo: Mapped[str] = mapped_column(String(255), nullable=True)

    admin_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id'),
        nullable=False,
        comment="ID администратора сообщества"
    )

    

    # Определяем связь с моделью User
    admin: Mapped['User'] = relationship(
        'User',
        back_populates='administered_communities'
    )

    memberships: Mapped[List['UserCommunity']] = relationship(
        'UserCommunity', back_populates='community')

    # List of members (users)
    members: Mapped[List['User']] = relationship(
        'User',
        secondary='user_community',
        back_populates='communities'
    )

    post_linked_community: Mapped[List['Post']] = relationship(
        'Post',
        back_populates='communities'
    )
