from .main import bp as main_bp
from .auth import bp as auth_bp
from .quiz import bp as quiz_bp

def init_app(app):
    """Initialize all blueprints."""
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(quiz_bp, url_prefix='/quiz')
