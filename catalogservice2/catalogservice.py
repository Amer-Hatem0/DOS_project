import sqlite3
import requests
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
        query_res = cursor.execute("SELECT * FROM catalog_item WHERE topic = ?", (topic,))
        rows = query_res.fetchall()
        if not rows:
            return jsonify({"error": f"No items found for topic: {topic}"}), 404
        return jsonify([{"id": row["ItemNumber"], "title": row["Name"]} for row in rows]), 200

    elif "item_number" in params:
        item_number = params["item_number"]
        query_res = cursor.execute("SELECT * FROM catalog_item WHERE ItemNumber = ?", (item_number,))
        row = query_res.fetchone()
        if not row:
            return jsonify({"error": f"Item {item_number} not found"}), 404
        return jsonify({
            "title": row["Name"],
            "quantity": row["Count"],
            "price": row["Cost"]
        }), 200

    return jsonify({"message": "Invalid query parameters"}), 400

@app.route('/update', methods=['PATCH'])
def update_catalog_item():
    data = request.json
    if not data or 'itemNumber' not in data:
        return jsonify({"error": "Missing itemNumber"}), 400

    item_number = data['itemNumber']
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM catalog_item WHERE ItemNumber = ?", (item_number,))
    row = cursor.fetchone()
    if not row:
        return jsonify({"error": f"Item {item_number} not found"}), 404

    if 'count' in data:
        cursor.execute("UPDATE catalog_item SET Count = Count + ? WHERE ItemNumber = ?", (data['count'], item_number))

    if 'cost' in data:
        cursor.execute("UPDATE catalog_item SET Cost = ? WHERE ItemNumber = ?", (data['cost'], item_number))

    conn.commit()

    # 🔁 Invalidate cache in front-end
    for endpoint in ["http://front_api:5000", "http://localhost:8080"]:
        try:
            requests.post(f"{endpoint}/invalidate/{item_number}")
        except Exception as e:
            print(f"[Warning] Failed to notify frontend: {e}")

    cursor.execute("SELECT * FROM catalog_item WHERE ItemNumber = ?", (item_number,))
    updated_row = cursor.fetchone()
    return jsonify({
        "message": f"Updated record {item_number} successfully",
        "new_count": updated_row["Count"],
        "new_cost": updated_row["Cost"]
    }), 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
