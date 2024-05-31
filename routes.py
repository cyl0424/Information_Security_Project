from flask import Blueprint, render_template, request, send_from_directory, current_app
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

        # Set the file save path
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        filepath = os.path.join(upload_folder, filename)

        file.save(filepath)

        action = request.form.get('action')
        start_time = time.time()

        pooling_result = None
        approx_pooling_result = None
        time_max = None
        time_approx = None
        filename_max = None
        filename_approx = None

        processed_folder = current_app.config['PROCESSED_FOLDER']
        if not os.path.exists(processed_folder):
            os.makedirs(processed_folder)

        # Add file extension
        name, ext = os.path.splitext(filename)
        if ext == '':
            ext = '.jpg'  # Set default extension to jpeg

        if action == 'sort':
            pooling_result, processed_image = ip.process_image(filepath, pool_size, stride)
            action_text = "Sort Max Function"
            elapsed_time = time.time() - start_time

            processed_filename = f'processed_{name}{ext}'
            processed_filepath = os.path.join(processed_folder, processed_filename)
            processed_image.save(processed_filepath)

            filename = processed_filename
        elif action == 'approx':
            pooling_result, processed_image = ip.process_image_approx(filepath, pool_size, stride)
            action_text = "Approx Max Function"
            elapsed_time = time.time() - start_time

            processed_filename = f'processed_{name}{ext}'
            processed_filepath = os.path.join(processed_folder, processed_filename)
            processed_image.save(processed_filepath)

            filename = processed_filename
        elif action == 'compare':
            # Max Pooling
            start_time_max = time.time()
            pooling_result, processed_image_max = ip.process_image(filepath, pool_size, stride)
            time_max = time.time() - start_time_max

            processed_filename_max = f'processed_max_{name}{ext}'
            processed_filepath_max = os.path.join(processed_folder, processed_filename_max)
            processed_image_max.save(processed_filepath_max)

            filename_max = processed_filename_max

            # Approx Max Pooling
            start_time_approx = time.time()
            approx_pooling_result, processed_image_approx = ip.process_image_approx(filepath, pool_size, stride)
            time_approx = time.time() - start_time_approx

            processed_filename_approx = f'processed_approx_{name}{ext}'
            processed_filepath_approx = os.path.join(processed_folder, processed_filename_approx)
            processed_image_approx.save(processed_filepath_approx)

            filename_approx = processed_filename_approx

            action_text = "Comparison of Max Pooling and Approx Max Pooling"
            elapsed_time = None

        return render_template('processed_result.html', filename=filename, time=elapsed_time,
                               max_pooling_result=pooling_result.tolist(), action_text=action_text,
                               approx_pooling_result=approx_pooling_result.tolist() if approx_pooling_result is not None else None,
                               time_max=time_max, time_approx=time_approx, filename_max=filename_max, filename_approx=filename_approx)
    return render_template('index.html', form=form)


@main_blueprint.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(current_app.config['PROCESSED_FOLDER'], filename)


@main_blueprint.route('/result')
def result():
    filename = request.args.get('filename')
    elapsed_time = request.args.get('time')
    max_pooling_result = request.args.get('max_pooling_result')
    approx_pooling_result = request.args.get('approx_pooling_result')
    return render_template('processed_result.html', filename=filename, time=elapsed_time,
                           max_pooling_result=max_pooling_result, approx_pooling_result=approx_pooling_result)
