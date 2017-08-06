from . import schemas
from . import stocks
from . import items
from . import inventories
from . import consumptions

__all__ = [schemas,
           stocks,
           items,
           inventories,
           consumptions]


def register_blueprint(app):
    for view in __all__:
        app.register_blueprint(view.module)
