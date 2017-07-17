from . import schemas
from . import stocks
from . import items
from . import inventories

__all__ = [schemas,
           stocks,
           items,
           inventories]


def register_blueprint(app):
    for view in __all__:
        app.register_blueprint(view.module)
