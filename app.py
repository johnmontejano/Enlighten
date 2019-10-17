from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/contractor')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
products = db.products
price = db.price
products.insert_one({'title': 'Push Harder', 'quote': 'Push Harder Than Yesterday, if you want a different tomorrow'})
products.insert_one({'title': 'Time', 'quote': 'An inch of time, is an inch of gold'})
products.insert_one({'title': 'Dedication', 'quote': 'Long term dedication pays off'})
products.insert_one({'title': 'Money', 'quote': 'Never spend money you did not earn'})


app = Flask(__name__)

# home page
@app.route('/')
def contractor_index():
    return render_template('contractor_index.html', products=products.find())

# create flavor page
@app.route('/products/new')
def contractor_new():
    return render_template('contractor_new.html', product={}, title='New Item')

# shows homepage
@app.route('/products', methods=['POST'])
def contractor_submit():
    product = {
        'title': request.form.get('title'),
        'price': request.form.get('price'),
        'img': request.form.get('img')
    }
    print(product)
    product_id = products.insert_one(product).inserted_id
    return redirect(url_for('contractor_show', product_id=product_id))

# shows a sock's own page
@app.route('/products/<product_id>')
def contractor_show(product_id):
    product = products.find_one({'_id': ObjectId(product_id)})
    # product_price = price.find({'product_id': ObjectId(product_id)})
    return render_template('quote_view.html', product=product)

# updates an item
@app.route('/products/<product_id>', methods=['POST'])
def products_update(product_id):
    updated_product = {
        'title': request.form.get('title'),
        'price': request.form.get('price'),
        'img': request.form.get('img')
    }
    products.update_one(
        {'_id': ObjectId(product_id)},
        {'$set': updated_product})
    return redirect(url_for('contractor_show', product_id=product_id))

# shows the user the edit page
@app.route('/products/<product_id>/edit')
def playlists_edit(product_id):
    product = products.find_one({'_id': ObjectId(product_id)})
    return render_template('contractor_edit.html', product=product, title='Edit Socks')

# deletes a flavor
@app.route('/products/<product_id>/delete', methods=['POST'])
def playlists_delete(product_id):
    products.delete_one({'_id': ObjectId(product_id)})
    return redirect(url_for('contractor_index'))

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))