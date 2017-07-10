from . import schemas
from . import nutrition

__all__ = [schemas,
           nutrition]


def register_blueprint(app):
    for view in __all__:
        app.register_blueprint(view.module)
