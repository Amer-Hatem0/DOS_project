import sqlite3
import requests
from flask import Flask, jsonify

app = Flask(__name__)

catalog_services = ["http://catalog1:5000", "http://catalog2:5000"]

def get_db_connection():
    conn = sqlite3.connect('/data/order.db')
    conn.row_factory = sqlite3.Row
    return conn

def try_request(method, path, **kwargs):
    for base_url in catalog_services:
        try:
            url = f"{base_url}{path}"
            if method == "GET":
                res = requests.get(url, timeout=2, **kwargs)
            elif method == "PATCH":
                res = requests.patch(url, timeout=2, **kwargs)
            else:
                continue

            if res.ok:
                return res
        except Exception as e:
            print(f"[Error] Failed contacting {base_url}: {e}")
    return None

@app.route('/purchase/<item_num>', methods=['POST'])
def orders(item_num):
    response = try_request("GET", "/query", params={'item_number': item_num})
    if not response:
        return jsonify({'message': 'Catalog service unreachable'}), 503

    data = response.json()
    if data['quantity'] <= 0:
        return jsonify({'message': "This book is out of stock"}), 406

    patch_res = try_request("PATCH", "/update", json={
        "count": -1,
        "itemNumber": item_num
    })
    if not patch_res:
        return jsonify({'message': 'Failed to update catalog'}), 500

    patch_response = patch_res.json()
    if 'message' in patch_response and patch_response['message'].startswith("Updated record"):
        con = get_db_connection()
        con.cursor().execute("INSERT INTO 'order' (ItemNumber) VALUES (?)", (item_num,))
        con.commit()
        return jsonify({'message': f'Successfully purchased item {item_num}'}), 200

    return jsonify({'message': f'Failed to purchase item {item_num}'}), 404

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
