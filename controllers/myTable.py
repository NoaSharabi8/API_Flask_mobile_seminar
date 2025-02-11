from flask import request, jsonify, Blueprint
from mongodb_connection_manager import MongoConnectionHolder
from datetime import datetime
import uuid

feature_toggle_blueprint = Blueprint('cluster0', __name__)

# 1. Create a new feature toggle
@feature_toggle_blueprint.route('/feature-toggle', methods=['POST'])
def create_feature_toggle():
    """
    Create a new feature toggle
    ---
    parameters:
        - name: feature_toggle
          in: body
          required: true
          description: The feature toggle to create
          schema:
            id: feature_toggle
            required:
                - name
                - c1
                - c2
                - c3
            properties:
                name:
                    type: string
                    description: The name of the feature
                description:
                    type: string
                    description: The description of the feature toggle
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
            description: The feature toggle was created successfully
        400:
            description: The request was invalid
        500:
            description: An error occurred while creating the feature toggle
    """
    data = request.json
    db = MongoConnectionHolder.get_db()

    # Check if the database connection was successful
    if db is None:
        return jsonify({"error": "Could not connect to the database"}), 500

    # Check if the request is valid
    if not all(key in data for key in ['name', 'description', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6']):
        return jsonify({"error": "Invalid request"}), 400

    # Create the feature toggle item
    feature_toggle_item = {
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

    
    # Insert the feature toggle into the database
    package_collection = db["colorsPalette"]
    package_collection.insert_one(feature_toggle_item)

    return jsonify({"message": "Feature toggle created successfully", '_id': feature_toggle_item['_id']}), 201


# 2. Get all feature toggles for package name
@feature_toggle_blueprint.route('/feature-toggles', methods=['GET'])
def get_all_feature_names():
    """
    Get all feature toggle names
    ---
    responses:
        200:
            description: List of all feature toggle names    
    """
    db = MongoConnectionHolder.get_db()
    if db is None:
        return jsonify({'error': 'Database not initialized'}), 500

    package_collection = db["colorsPalette"]

    # שליפת רק את השדה 'name' מכל האובייקטים
    feature_names = list(package_collection.find({}, {"name": 1, "_id": 0}))

    if not feature_names:
        return jsonify({'error': 'No feature names found'}), 404

    return jsonify(feature_names), 200


# 3. Get a feature toggle by id for package name
@feature_toggle_blueprint.route('/feature-toggle/<feature_name>', methods=['GET'])
def get_feature_toggle_details(feature_name):
    """
    Get details of a specific feature toggle by name
    ---
    parameters:
        - name: feature_name
          in: path
          type: string
          required: true
          description: Name of the feature toggle to get
    responses:
        200:
            description: Feature toggle details
        404:
            description: Feature toggle not found
    """
    db = MongoConnectionHolder.get_db()
    if db is None:
        return jsonify({'error': 'Database not initialized'}), 500

    package_collection = db["colorsPalette"]  # מסד נתונים קבוע מראש

    # חיפוש הרשומה לפי name (Case-Sensitive)
    feature = package_collection.find_one({"name": feature_name})

    if not feature:
        return jsonify({'error': 'Feature toggle not found'}), 404

    # המרת ObjectId למחרוזת כדי למנוע בעיית JSON
    feature["_id"] = str(feature["_id"])

    return jsonify(feature), 200




