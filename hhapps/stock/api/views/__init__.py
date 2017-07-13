from . import schemas
from . import stocks

__all__ = [schemas,
           stocks]

def register_blueprint(app):
    for view in __all__:
        app.register_blueprint(view.module)
