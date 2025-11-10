from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, BooleanField, DateTimeLocalField
from wtforms.validators import DataRequired, Length
from datetime import datetime, UTC
from .models import PostCategory

class PostForm(FlaskForm):

    title = StringField('Title', validators=[
        DataRequired(),
        Length(min=3, max=150, message="Title must be between 3 and 150 characters.")
    ])

    content = TextAreaField('Content', validators=[
        DataRequired(message="Content field is required.")
    ], render_kw={"rows": 10})


    category = SelectField('Category',
        choices=[(cat.value, cat.name.title()) for cat in PostCategory],
        validators=[DataRequired()]
    )

    publish_date = DateTimeLocalField('Publish Date',
                                      format='%Y-%m-%dT%H:%M',
                                      default=lambda: datetime.now(UTC),
                                      validators=[DataRequired()]
                                      )

    is_active = BooleanField('Active Post', default=True)

    submit = SubmitField('Submit Post')

class DeleteForm(FlaskForm):

    submit = SubmitField('Delete')