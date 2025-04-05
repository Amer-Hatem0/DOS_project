import sqlite3
from itertools import count
 
from flask import Flask, request, jsonify

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('/data/catalog_service.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/query', methods=['GET'])
def query_catalog_items():
    params = request.args
    if len(params) == 0:
        return jsonify({"message": "No query string found in the request"}), 400
    elif params.keys().__contains__("topic"):
        conn = get_db_connection()
        topic = params["topic"]
        query_res = conn.cursor().execute("SELECT * FROM catalog_item WHERE topic = ?", (topic,))
        rows = query_res.fetchall()
        if rows is None or len(rows) == 0:
            return jsonify({"error": f"Something went wrong,make sure that topic {topic} exists"}), 404
        return jsonify([{"id": row["ItemNumber"], "title": row["Name"]} for row in rows])
    elif params.keys().__contains__("item_number"):
        conn = get_db_connection()
        item_number = params["item_number"]
        query_res = conn.cursor().execute("SELECT * FROM catalog_item WHERE ItemNumber = ?", (item_number,))
        rows = query_res.fetchall()
        if rows is None or len(rows) == 0:
            return jsonify({"error": f"Something went wrong,make sure that item {item_number} exists"}), 404
        return jsonify({"title": rows[0]["Name"], "quantity": rows[0]["Count"], "price": rows[0]["Cost"]}), 200

    else:
        return jsonify({"message": "Invalid query parameters"}), 400


@app.route('/update', methods=['PATCH'])
def update_catalog_item():
    data = request.json
    if data is None or not data:
        return jsonify("Invalid request data"), 400
    conn = get_db_connection()
    cursor = conn.cursor()

    if 'itemNumber' in data and ('count' in data or 'cost' in data):

        item_number = data['itemNumber']

        cursor.execute("SELECT Count, Cost FROM catalog_item WHERE ItemNumber = ?", (item_number,))
        row = cursor.fetchone()

        if row is None:
            return jsonify({"error": f"Item {item_number} not found"}), 404

        current_count, current_cost = row

        if 'count' in data:
            new_count = data['count']
            print(f"Executing: UPDATE catalog_item SET Count = {new_count} WHERE ItemNumber = {item_number}")  # For debugging
            cursor.execute("UPDATE catalog_item SET Count = ? WHERE ItemNumber = ?", (new_count, item_number))
            conn.commit()

        if 'cost' in data:
            new_cost = data['cost']
            print(f"Executing: UPDATE catalog_item SET Cost = {new_cost} WHERE ItemNumber = {item_number}")  # For debugging
            cursor.execute("UPDATE catalog_item SET Cost = ? WHERE ItemNumber = ?", (new_cost, item_number))
            conn.commit()

        cursor.execute("SELECT * FROM catalog_item WHERE ItemNumber = ?", (item_number,))
        row = cursor.fetchone()

        if row:
            return jsonify({"message": f"Updated record {item_number} successfully",
                             "new_count": row["Count"], "new_cost": row["Cost"]}), 200
        else:
            return jsonify({"error": "Item not found after update"}), 404
    else:
        return jsonify({"message": "Invalid request data or missing item number"}), 400



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
