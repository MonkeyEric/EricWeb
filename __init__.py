from EricWeb.webapp.auth import auth_bp

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG','development')
    app = Flask('EricWeb')
    app.config.from_object(config[config_name])

    register_blueprints(app)

    return app

def register_blueprints(app):
    #app.register_blueprint(blog_bp)
    #app.register_blueprint(admin_bp,url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/admin')

