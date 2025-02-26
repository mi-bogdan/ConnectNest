from base import Base

from datetime import datetime

from sqlalchemy import Boolean, String, DateTime, func, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from user import User
from communities import Communities

import uuid


class UserCommunity(Base):
    """Таблица пользователей которые подписанные на сообщества"""
    
    __tablename__ = 'user_community'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id')
    )
    community_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('communities.id')
    )
    date_joined: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        comment="Дата вступления в сообщество"
    )

    # Уникальное ограничение на пару user_id и community_id
    __table_args__ = (
        UniqueConstraint('user_id', 'community_id', name='uix_user_community'),
    )

    user: Mapped['User'] = relationship('User', back_populates='memberships')
    community: Mapped['Communities'] = relationship(
        'Communities', back_populates='memberships')
