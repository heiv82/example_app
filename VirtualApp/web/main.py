from service.blueprint import service
from app import app


app.register_blueprint(service, url_prefix='/device_service')

from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
csrf.init_app(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
