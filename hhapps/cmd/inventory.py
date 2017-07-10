
from hhapps import inventory

def main():
    options = inventory.get_program_options()
    app = inventory.create_app()

    app.run(
        debug=options.debug,
        host=options.host,
        port=int(options.port)
    )
