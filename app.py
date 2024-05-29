import os

from flask import Flask
from flask_wtf import CSRFProtect

from routes import main_blueprint

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
csrf = CSRFProtect(app)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['PROCESSED_FOLDER'] = 'static/processed/'

app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
