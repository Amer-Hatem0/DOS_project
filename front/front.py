import requests
import time
from flask import Flask, request, jsonify

app = Flask(__name__)


purchase_services = ["http://purchase1:5000", "http://purchase2:5000"]
catalog_services = ["http://catalog1:5000", "http://catalog2:5000"]

cache = {}
CACHE_TTL = 60


def is_cache_valid(key):
    return key in cache and (time.time() - cache[key]['timestamp']) < CACHE_TTL

def try_request(services, method, path):
    for base_url in services:
        try:
            url = f"{base_url}{path}"
            if method == "GET":
                response = requests.get(url, timeout=2)
            elif method == "POST":
                response = requests.post(url, timeout=2)
            else:
                continue

            if response.status_code == 200:
                return jsonify(response.json()), 200
        except Exception as e:
            print(f"[Warning] Failed contacting {base_url}: {e}")
    return jsonify({"error": "All backend services are unreachable."}), 503


@app.route('/search/<topic>', methods=['GET'])
def search_by_topic(topic):
    cache_key = f"search:{topic}"
    if is_cache_valid(cache_key):
        return jsonify(cache[cache_key]['data']), 200
    data, status = try_request(catalog_services, "GET", f"/query?topic={topic}")
    if status == 200:
        cache[cache_key] = {'data': data.get_json(), 'timestamp': time.time()}
    return data, status

#
@app.route('/info/<item_number>', methods=['GET'])
def get_item_info(item_number):
    cache_key = f"info:{item_number}"
    if is_cache_valid(cache_key):
        return jsonify(cache[cache_key]['data']), 200
    data, status = try_request(catalog_services, "GET", f"/query?item_number={item_number}")
    if status == 200:
        cache[cache_key] = {'data': data.get_json(), 'timestamp': time.time()}
    return data, status


@app.route('/purchase/<item_number>', methods=['POST'])
def purchase_item(item_number):
    return try_request(purchase_services, "POST", f"/purchase/{item_number}")


@app.route('/invalidate/<item_number>', methods=['POST'])
def invalidate_cache(item_number):
    keys_to_remove = [
        f"info:{item_number}",
        f"search:{item_number}"
    ]
    removed = []
    for key in keys_to_remove:
        if key in cache:
            cache.pop(key)
            removed.append(key)
    return jsonify({"message": f"Invalidated keys: {removed}"}), 200


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
