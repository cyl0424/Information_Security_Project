from flask_wtf import FlaskForm
from wtforms import FileField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ImageForm(FlaskForm):
    file = FileField('Choose an image', validators=[DataRequired()])
    pool_size = IntegerField('Pooling window size', validators=[DataRequired(), NumberRange(min=1)])
    stride = IntegerField('Stride size', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Submit')
