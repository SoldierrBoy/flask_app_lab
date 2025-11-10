import enum
from datetime import datetime, UTC
from app import db
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional



class PostCategory(enum.Enum):
    NEWS = 'news'
    PUBLICATION = 'publication'
    TECH = 'tech'
    OTHER = 'other'

class Post(db.Model):

    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(150), nullable=False)
    content: Mapped[str] = mapped_column(db.Text, nullable=False)

    posted: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    category: Mapped[PostCategory] = mapped_column(
        db.Enum(PostCategory, values_callable=lambda x: [e.value for e in x]),
        default=PostCategory.OTHER,
        nullable=False
    )

    is_active: Mapped[Optional[bool]] = mapped_column(default=True)
    author: Mapped[Optional[str]] = mapped_column(db.String(20), default='Anonymous')


    def __repr__(self):
        return f'<Post {self.title}>'