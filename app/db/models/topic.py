from datetime import datetime
from sqlalchemy import Boolean, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy
import uuid
from typing import List

from topic_post import TopicPost
from post import Post

from base import Base


class Topic(Base):
    """Темы постов"""

    __tablename__ = "topic"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="id темы"
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Тема"
    )

    # Связь с TopicPost
    topic_posts: Mapped[List['TopicPost']] = relationship(
        'TopicPost', back_populates='topic'
    )

    # Используем association_proxy для доступа к постам напрямую
    posts: Mapped[List['Post']] = association_proxy('topic_posts', 'post')
