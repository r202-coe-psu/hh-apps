
from hhservice import nutrition

def main():
    options = nutrition.get_program_options()
   
    app = nutrition.create_app()
    app.run(
        debug=options.debug,
        host=options.host,
        port=int(options.port)
    )
