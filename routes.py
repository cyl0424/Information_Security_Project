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

        # 파일 저장 경로 설정
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        filepath = os.path.join(upload_folder, filename)

        file.save(filepath)

        start_time = time.time()
        # pooling_result, processed_image = ip.process_image(filepath, pool_size, stride)
        pooling_result, processed_image = ip.process_image_approx(filepath, pool_size, stride)
        elapsed_time = time.time() - start_time

        processed_folder = current_app.config['PROCESSED_FOLDER']
        if not os.path.exists(processed_folder):
            os.makedirs(processed_folder)

        # 파일 확장자 추가
        name, ext = os.path.splitext(filename)
        if ext == '':
            ext = '.jpg'  # 기본 확장자를 jpeg로 설정
        processed_filename = f'processed_{name}{ext}'
        processed_filepath = os.path.join(processed_folder, processed_filename)

        processed_image.save(processed_filepath)

        # 결과 페이지로 리다이렉트 대신 render_template 사용
        return render_template('processed_result.html', filename=processed_filename, time=elapsed_time,
                               max_pooling_result=pooling_result.tolist())
    return render_template('index.html', form=form)


@main_blueprint.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(current_app.config['PROCESSED_FOLDER'], filename)


@main_blueprint.route('/result')
def result():
    filename = request.args.get('filename')
    elapsed_time = request.args.get('time')
    max_pooling_result = request.args.get('max_pooling_result')
    return render_template('processed_result.html', filename=filename, time=elapsed_time,
                           max_pooling_result=max_pooling_result)
