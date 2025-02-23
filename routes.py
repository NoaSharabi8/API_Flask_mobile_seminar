from controllers.color_palettes import color_palette_blueprint

def initial_routes(app):
    app.register_blueprint(color_palette_blueprint)