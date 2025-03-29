from app.db.base import Base

from datetime import datetime

from sqlalchemy import Boolean, String, DateTime, func, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID



import uuid


class TopicPost(Base):
    """Темы к посту"""

    __tablename__ = "topic_post"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="id"
    )

    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('topic.id')
    )
    post_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('post.id')
    )

    # Определяем отношения с Post и Topic
    topic: Mapped['Topic'] = relationship(
        'Topic', back_populates='topic_posts')
    post: Mapped['Post'] = relationship('Post', back_populates='topic_posts')
