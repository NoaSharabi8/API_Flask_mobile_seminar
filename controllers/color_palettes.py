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
                - package_name
                - name
                - colorsList
            properties:
                package_name:
                    type: string
                    description: The name of the package
                name:
                    type: string
                    description: The name of the palette
                description:
                    type: string
                    description: The description of the color palette
                colorsList:
                    type: array
                    description: An array of colors
                    items:
                        type: string                   
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
    if not all(key in data for key in ['package_name', 'name']):
        return jsonify({"error": "Invalid request"}), 400
    
    # בדיקה האם colorsList הוא רשימה
    if not isinstance(data['colorsList'], list):
        return jsonify({"error": "colorsList must be a list"}), 400
    



    # Create the color palette item
    color_palette_item = {
        "_id": str(uuid.uuid4()),
        "name": data['name'],
        "description": data.get('description', ""),
        "colorsList": data['colorsList'] 
    }

    
    # Insert the color palette into the database
    package_collection = db[data['package_name']]
    # בדיקה אם כבר קיים צבע עם אותו שם באותו package
    existing_palette = package_collection.find_one({"name": data['name']})
    if existing_palette:
        return jsonify({"error": "A color palette with this name already exists in the package"}), 400

    package_collection.insert_one(color_palette_item)

    return jsonify({"message": "Color palette created successfully", '_id': color_palette_item['_id']}), 201


# 2. Get palette names for package name
@color_palette_blueprint.route('/color-palette/<package_name>', methods=['GET'])
def get_palette_names(package_name):
    """
    Get all colors palette names
    ---
    parameters:
        - name: package_name
          in: path
          type: string
          required: true
          description: Name of the package
    responses:
        200:
            description: List of all color palette names    
    """
    db = MongoConnectionHolder.get_db()
    if db is None:
        return jsonify({'error': 'Database not initialized'}), 500

    package_collection = db[package_name]

    # שליפת רק את השדה 'name' מכל האובייקטים
    colors_names = list(package_collection.find({}, {"name": 1, "_id": 0}))

    if not colors_names:
        return jsonify({'error': 'No color palette names found'}), 404

    return jsonify(colors_names), 200


# 3. Get a color palette by name
@color_palette_blueprint.route('/color-palette/<package_name>/<palette_name>', methods=['GET'])
def get_color_palette_details(package_name, palette_name):
    """
    Get details of a specific color palette by name
    ---
    parameters:
        - name: package_name
          in: path
          type: string
          required: true
          description: Name of the package    
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

    package_collection = db[package_name]  # מסד נתונים קבוע מראש

    # חיפוש הרשומה לפי name (Case-Sensitive)
    palette = package_collection.find_one({"name" : palette_name})

    if not palette:
        return jsonify({'error': 'Color palette not found'}), 404

    # המרת ObjectId למחרוזת כדי למנוע בעיית JSON
    palette["_id"] = str(palette["_id"])

    return jsonify(palette), 200




