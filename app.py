#BEGIN CODE HERE
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
import numpy as np
#END CODE HERE

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/DATABASE"
mongo = PyMongo(app)
CORS(app)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

@app.route("/search", methods=["GET"])
def search():
    #BEGIN CODE HERE
    name = request.args.get('name', '')  
    query = {'name': {'$regex': name, '$options': 'i'}}
    products = mongo.db.products.find(query).sort('price', -1)
    results = []
    for product in products:
        results.append({
            'id': str(product['_id']),
            'name': product['name'],
            'production_year': product['production_year'],
            'price': product['price'],
            'color': product['color'],
            'size': product['size']
        })
    return jsonify(results)
    #END CODE HERE

@app.route("/add-product", methods=["POST"])
def add_product():
    #BEGIN CODE HERE
    product_data = request.get_json()  
    if not product_data:
        return jsonify({"error": "ERROR"}), 400
    update_keys = {"price", "production_year", "color", "size"}
    update_data = {key: product_data[key] for key in update_keys if key in product_data}
    result = mongo.db.products.find_one_and_update(
        {"name": product_data["name"]},  
        {"$set": update_data},          
        upsert=True,                     
        return_document=True            
    )
    return jsonify({
        "id": str(result["_id"]),
        "name": result["name"],
        "production_year": result["production_year"],
        "price": result["price"],
        "color": result["color"],
        "size": result["size"]
    })
    #END CODE HERE

@app.route("/content-based-filtering", methods=["POST"])
def content_based_filtering():
    #BEGIN CODE HERE
    data = request.get_json()
    if not data:
        return jsonify([]), 400
    input_vector = np.array([data['production_year'], data['price'], data['color'], data['size']])
    products = mongo.db.products.find()
    similar_products = []
    for product in products:
        product_vector = np.array([product['production_year'], product['price'], product['color'], product['size']])
        similarity = np.dot(input_vector, product_vector) / (np.linalg.norm(input_vector) * np.linalg.norm(product_vector))
        if similarity > 0.7:
            similar_products.append(product['name'])
    return jsonify(similar_products)
    #END CODE HERE
