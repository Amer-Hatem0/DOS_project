
import sqlite3
import requests
from flask import Flask, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('/data/order.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/purchase/<item_num>', methods=['POST'])
def orders(item_num):
 
    response = requests.get("http://catalog1:5000/query", params={'item_number': item_num})

    if response.ok and response.status_code == 200:
        data = response.json()

        if data['quantity'] <= 0:
            return jsonify({'message': "This book is out of stock"}), 406

        response = requests.patch("http://catalog1:5000/update", json={
            "count": -1,
            "itemNumber": item_num
        })

        patch_response = response.json()
        if 'message' in patch_response and patch_response['message'].startswith("Updated record"):
            con = get_db_connection()
            con.cursor().execute("INSERT INTO 'order' (ItemNumber) VALUES (?)", (item_num,))
            con.commit()
            return jsonify({'message': f'Successfully purchased item {item_num}'}), 200

    return jsonify({'message': f'Failed to purchase item {item_num}'}), 404

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
