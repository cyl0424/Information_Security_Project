from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets import Input

class ReadOnlyInput(Input):
    """
    Custom widget to render a read-only input field.
    """
    input_type = 'text'

    def __call__(self, field, **kwargs):
        kwargs.setdefault('readonly', True)
        return super(ReadOnlyInput, self).__call__(field, **kwargs)

class ImageForm(FlaskForm):
    file = FileField('Choose an image', validators=[DataRequired()])
    pool_size = IntegerField('Pooling window size', default=2, widget=ReadOnlyInput(), render_kw={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500'
    })
    stride = IntegerField('Stride size', validators=[DataRequired(), NumberRange(min=1)], render_kw={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500'
    })
    submit = SubmitField('Submit')

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ImageForm()
    if form.validate_on_submit():
        # Process the form data
        return redirect(url_for('success'))
    return render_template('index.html', form=form)

@app.route('/success')
def success():
    return "Form successfully submitted!"

if __name__ == '__main__':
    app.run(debug=True)
