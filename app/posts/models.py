import enum
from datetime import datetime, UTC
from app import db

class PostCategory(enum.Enum):
    NEWS = 'news'
    PUBLICATION = 'publication'
    TECH = 'tech'
    OTHER = 'other'


class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted = db.Column(db.DateTime, default=lambda: datetime.now(UTC))

    category = db.Column(
        db.Enum(PostCategory, values_callable=lambda x: [e.value for e in x]),
        default=PostCategory.OTHER,
        nullable=False
    )


    is_active = db.Column(db.Boolean, default=True)
    author = db.Column(db.String(20), default='Anonymous')

    def __repr__(self):
        return f'<Post {self.title}>'