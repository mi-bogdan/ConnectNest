from datetime import datetime
from typing import Mapping
from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from app.db.base import Base
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID


from typing import List




class Post(Base):
    """Посты"""

    __tablename__ = "post"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="id поста"
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Заголовок"
    )
    create_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        comment="Дата создания"
    )
    update_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="Дата обновления"
    )
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    author_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id'),
        nullable=False,
        comment="ID автора поста"
    )
    communities_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('communities.id'),
        nullable=False,
        comment="ID сообщества"
    )

    author: Mapped['User'] = relationship(
        'User',
        back_populates="author_the_post"
    )
    communities: Mapped['Communities'] = relationship(
        'Communities', back_populates="post_linked_community")

    # Связь с TopicPost
    topic_posts: Mapped[List['TopicPost']] = relationship(
        'TopicPost', back_populates='post'
    )

    # Используем association_proxy для доступа к темам напрямую
    topics: Mapped[List['Topic']] = association_proxy('topic_posts', 'topic')
