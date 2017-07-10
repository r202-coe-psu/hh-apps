from . import schemas
from . import inventories

__all__ = [schemas,
           inventories]

def register_blueprint(app):
    for view in __all__:
        app.register_blueprint(view.module)
