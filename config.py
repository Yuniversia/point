class Config:
    SECRET_KEY = 'hard-to-guess-string'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///school_points.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'app/static/images/uploads/'
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

    IP = "127.0.0.1"
    PORT = 2000
    DEBUG = True

    REDIS_HOST = "localhost"
    REDIS_PORT = 6379

class Login_conf:
    login_time = 2