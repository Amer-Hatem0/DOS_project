
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('/data/catalog_service.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/query', methods=['GET'])
def query_catalog_items():
    params = request.args
    if not params:
        return jsonify({"message": "No query string found in the request"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    if "topic" in params:
        topic = params["topic"]
        rows = cursor.execute("SELECT * FROM catalog_item WHERE topic = ?", (topic,)).fetchall()
        if not rows:
            return jsonify({"error": f"No items found for topic: {topic}"}), 404
        return jsonify([{"id": row["ItemNumber"], "title": row["Name"]} for row in rows]), 200

    elif "item_number" in params:
        item_number = params["item_number"]
        row = cursor.execute("SELECT * FROM catalog_item WHERE ItemNumber = ?", (item_number,)).fetchone()
        if not row:
            return jsonify({"error": f"Item {item_number} not found"}), 404
        return jsonify({
            "title": row["Name"],
            "quantity": row["Count"],
            "price": row["Cost"]
        }), 200

    return jsonify({"message": "Invalid query parameters"}), 400

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
