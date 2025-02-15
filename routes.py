from controllers.myTable import color_palette_blueprint

def initial_routes(app):
    app.register_blueprint(color_palette_blueprint)