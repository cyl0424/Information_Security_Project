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

        upload_folder = current_app.config['UPLOAD_FOLDER']
        filepath = os.path.join(upload_folder, filename)

        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        file.save(filepath)

        start_time = time.time()
        processed_image = ip.process_image(filepath, pool_size, stride)
        elapsed_time = time.time() - start_time

        processed_folder = current_app.config['PROCESSED_FOLDER']
        if not os.path.exists(processed_folder):
            os.makedirs(processed_folder)

        processed_filepath = os.path.join(processed_folder, 'processed_' + filename)
        processed_image.save(processed_filepath)

        return redirect(url_for('main.processed_file', filename='processed_' + filename, time=elapsed_time))
    return render_template('index.html', form=form)


@main_blueprint.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(current_app.config['PROCESSED_FOLDER'], filename)
