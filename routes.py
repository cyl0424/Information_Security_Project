from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, current_app
from werkzeug.utils import secure_filename
import os
import image_processing as ip
import time
from forms import ImageForm

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/', methods=['GET', 'POST'])
def index():
    form = ImageForm()
    if form.validate_on_submit():
        file = form.file.data
        pool_size = form.pool_size.data
        stride = form.stride.data
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        start_time = time.time()
        processed_image = ip.process_image(filepath, pool_size, stride)
        elapsed_time = time.time() - start_time

        processed_filepath = os.path.join(current_app.config['PROCESSED_FOLDER'], 'processed_' + filename)
        processed_image.save(processed_filepath)

        return redirect(url_for('main.processed_file', filename='processed_' + filename, time=elapsed_time))
    return render_template('index.html', form=form)


@main_blueprint.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(current_app.config['PROCESSED_FOLDER'], filename)
