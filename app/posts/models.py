import enum
from datetime import datetime, UTC
from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, Boolean, ForeignKey, func
from typing import Optional, List

post_tags = db.Table(
    'post_tags',
    db.Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class Tag(db.Model):
    __tablename__ = 'tags'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    posts: Mapped[List["Post"]] = relationship(
        "Post",
        secondary=post_tags,
        back_populates="tags"
    )

    def __repr__(self):
        return f'<Tag {self.name}>'


class PostCategory(enum.Enum):
    NEWS = 'news'
    PUBLICATION = 'publication'
    TECH = 'tech'
    OTHER = 'other'


class Post(db.Model):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(db.Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), nullable=False,
                                             default=lambda: datetime.now(UTC))

    category: Mapped[PostCategory] = mapped_column(
        db.Enum(PostCategory, values_callable=lambda x: [e.value for e in x]),
        default=PostCategory.OTHER,
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    author: Mapped[Optional["User"]] = relationship("User", back_populates="posts")
    tags: Mapped[List["Tag"]] = relationship(
        "Tag",
        secondary=post_tags,
        back_populates="posts"
    )

    def __repr__(self):
        return f'<Post {self.title}>'