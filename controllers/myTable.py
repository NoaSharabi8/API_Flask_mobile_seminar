from flask import request, jsonify, Blueprint
from mongodb_connection_manager import MongoConnectionHolder
from datetime import datetime
import uuid

color_palette_blueprint = Blueprint('cluster0', __name__)

# 1. Create a new color palette
@color_palette_blueprint.route('/color-palette', methods=['POST'])
def create_color_palette():
    """
    Create a new color palette
    ---
    parameters:
        - name: color_palette
          in: body
          required: true
          description: The color palette to create
          schema:
            id: color_palette
            required:
                - name
                - c1
                - c2
                - c3
            properties:
                name:
                    type: string
                    description: The name of the palette
                description:
                    type: string
                    description: The description of the color palette
                c1:
                    type: string
                    description: color number 1
                c2:
                    type: string
                    description: color number 2
                c3:
                    type: string
                    description: color number 3
                c4:
                    type: string
                    description: color number 4
                c5:
                    type: string
                    description: color number 5
                c6:
                    type: string
                    description: color number 6
    responses:
        201:
            description: The color palette was created successfully
        400:
            description: The request was invalid
        500:
            description: An error occurred while creating the color palette
    """
    data = request.json
    db = MongoConnectionHolder.get_db()

    # Check if the database connection was successful
    if db is None:
        return jsonify({"error": "Could not connect to the database"}), 500

    # Check if the request is valid
    if not all(key in data for key in ['name', 'description', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6']):
        return jsonify({"error": "Invalid request"}), 400

    # Create the color palette item
    color_palette_item = {
        "_id": str(uuid.uuid4()),
        "name": data['name'],
        "description": data['description'],
        "c1": data['c1'],
        "c2": data['c2'],
        "c3": data['c3'],
        "c4": data['c4'],
        "c5": data['c5'],
        "c6": data['c6']
    }

    
    # Insert the color palette into the database
    package_collection = db["colorsPalette"]
    package_collection.insert_one(color_palette_item)

    return jsonify({"message": "Color palette created successfully", '_id': color_palette_item['_id']}), 201


# 2. Get all colors palette's name
@color_palette_blueprint.route('/color-palette', methods=['GET'])
def get_all_colors_names():
    """
    Get all colors palette names
    ---
    responses:
        200:
            description: List of all color palette names    
    """
    db = MongoConnectionHolder.get_db()
    if db is None:
        return jsonify({'error': 'Database not initialized'}), 500

    package_collection = db["colorsPalette"]

    # שליפת רק את השדה 'name' מכל האובייקטים
    colors_names = list(package_collection.find({}, {"name": 1, "_id": 0}))

    if not colors_names:
        return jsonify({'error': 'No color palette names found'}), 404

    return jsonify(colors_names), 200


# 3. Get a color palette by name
@color_palette_blueprint.route('/color-palette/<color_name>', methods=['GET'])
def get_color_palette_details(palette_name):
    """
    Get details of a specific color palette by name
    ---
    parameters:
        - name: palette_name
          in: path
          type: string
          required: true
          description: Name of the color palette to get
    responses:
        200:
            description: Color palette details
        404:
            description: Color palette not found
    """
    db = MongoConnectionHolder.get_db()
    if db is None:
        return jsonify({'error': 'Database not initialized'}), 500

    package_collection = db["colorsPalette"]  # מסד נתונים קבוע מראש

    # חיפוש הרשומה לפי name (Case-Sensitive)
    colors = package_collection.find_one({"name": palette_name})

    if not colors:
        return jsonify({'error': 'Color palette not found'}), 404

    # המרת ObjectId למחרוזת כדי למנוע בעיית JSON
    colors["_id"] = str(colors["_id"])

    return jsonify(colors), 200




