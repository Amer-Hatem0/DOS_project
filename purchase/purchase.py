import sqlite3
import requests as requests
from flask import Flask, jsonify

def get_db_connection():
    conn = sqlite3.connect('/data/order.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route('/purchase/<item_num>', methods=['POST'])
def orders(item_num):
    base_url = 'http://172.17.0.1:5050/query'

    response = requests.get(base_url, params={'item_number': item_num})

    if response.ok and response.status_code == 200:
        data = response.json()

        if data['quantity'] <= 0:
            return jsonify({'message': "this book is out of stock"}), 406

        response = requests.patch('http://172.17.0.1:5050/update', json={
            "count": -1,
            "itemNumber": item_num})

        patch_response = response.json()
        print(patch_response)

        if 'message' in patch_response and patch_response['message'] == f"Updated record {item_num} successfully":
            new_count = patch_response.get('new_count', 'N/A')
            new_cost = patch_response.get('new_cost', 'N/A')

            con = get_db_connection()
            con.cursor().execute("INSERT INTO 'order' (ItemNumber) VALUES (?)", (item_num,))
            con.commit()

            return jsonify({'message': f'successfully purchased item {item_num}'}), 200
        else:
            return jsonify({'message': f'failed to Purchase item {item_num}'}), 404
    else:
        return jsonify({'message': f'failed to Purchase item {item_num}'}), 404

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
