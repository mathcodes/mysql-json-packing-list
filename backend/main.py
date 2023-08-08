import mysql.connector
from flask import Flask, request, jsonify, send_from_directory
import crud as crud  # Import your CRUD functions
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__, static_folder='../frontend')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory(app.static_folder, path)

@app.route('/create', methods=['POST'])
def create_item():
    data = request.json
    crud.create_item(data['item_type'], data['item_name'], data['quantity'], data['colors'], data['importance'])
    updated_items = crud.list_all_items()
    return jsonify(success=True, items=updated_items)

@app.route('/list', methods=['GET'])
def list_items():
    # Change this to a suitable function that lists items from MySQL
    data = crud.list_all_items()
    return jsonify(data)

# Similar endpoints for read, update, delete


def initialize_database():
    db = mysql.connector.connect(host="localhost", user="root", passwd="", db="PackingWithJSON")
    cursor = db.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS PackingWithJSON")
    cursor.execute("USE PackingWithJSON")

    tables = [
        "CREATE TABLE IF NOT EXISTS personal_items (id INT AUTO_INCREMENT PRIMARY KEY, type VARCHAR(255), item_name VARCHAR(255), quantity INT, colors VARCHAR(255), importance INT)",
        "CREATE TABLE IF NOT EXISTS household_items (id INT AUTO_INCREMENT PRIMARY KEY, type VARCHAR(255), item_name VARCHAR(255), quantity INT, colors VARCHAR(255), importance INT)",
        "CREATE TABLE IF NOT EXISTS work_essentials (id INT AUTO_INCREMENT PRIMARY KEY, type VARCHAR(255), item_name VARCHAR(255), quantity INT, colors VARCHAR(255), importance INT)"
    ]

    for table_query in tables:
        cursor.execute(table_query)

    cursor.close()
    db.close()




def create_item(item_type, item_name, quantity, colors, importance):
    crud.create_item(item_type, item_name, quantity, colors, importance)


def read_json_file():
    return crud.read_json_file()


def update_data(item_type, item_name, quantity=None, colors=None, importance=None):
    crud.update_data(item_type, item_name, quantity, colors, importance)


def read_item(item_type, item_name):
    return crud.read_item(item_type, item_name)


def delete_item(item_type, item_name):
    crud.delete_item(item_type, item_name)


if __name__ == "__main__":
    initialize_database()
    # CRUD Operations
    # Create item example
    create_item("personal", "laptop", 1, "grey", 3)
    # Read JSON file example
    data = read_json_file()
    # Update data example
    update_data("personal", "laptop", quantity=2, colors="silver", importance=4)
    # Read item example
    result, json_result = read_item("personal", "laptop")
    # Delete item example
    delete_item("personal", "laptop")
    app.run(debug=True)  # Start the Flask server
    # Additional CRUD calls as needed...
