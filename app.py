# app.py
import os
import boto3
import datetime


from flask import Flask, jsonify, request
app = Flask(__name__)

USERS_TABLE = os.environ.get('USERS_TABLE')
BOOKS_TABLE = os.environ.get('BOOKS_TABLE')
ORDERS_TABLE = os.environ.get('ORDERS_TABLE')

client = boto3.client('dynamodb')


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/users/<string:user_id>")
def get_user(user_id):
    resp = client.get_item(
        TableName=USERS_TABLE,
        Key={
            'userId': {'S': user_id}
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'User does not exist'}), 404

    return jsonify({
        'userId': item.get('userId').get('S'),
        'name': item.get('name').get('S')
    })


@app.route("/users", methods=["POST"])
def create_user():
    user_id = request.json.get('userId')
    name = request.json.get('name')

    if not user_id or not name:
        return jsonify({'error': 'Please provide userId and name'}), 400

    print("user_id", user_id)
    print("name", name)
    print('Table name', USERS_TABLE)

    resp = client.put_item(
        TableName=USERS_TABLE,
        Item={
            'userId': {'S': user_id},
            'name': {'S': name}
        }
    )
    return jsonify({
        'userId': user_id,
        'name': name
    })


@app.route("/books/<string:book_name>")
def get_book_info(book_name):
    resp = client.get_item(
        TableName=BOOKS_TABLE,
        Key={
            'book_name': {'S': book_name}
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'Book does not exist'}), 404

    return jsonify({
        'book_name': item.get('book_name').get('S'),
        'pages': item.get('pages').get('N'),
        'author': item.get('author').get('S'),
        'price': item.get('price').get('N')
    })


@app.route("/books", methods=["POST"])
def add_book():
    book_name = request.json.get('book_name')
    author = request.json.get('author')
    pages = request.json.get('pages')
    price = request.json.get('price')

    print("pages", type(pages))
    print("price", type(price))

    if not book_name or not author or not pages or not price:
        return jsonify({'error': 'Please provide book_name and author, '
                                 'pages, price'}), 400
    resp = client.put_item(
        TableName=BOOKS_TABLE,
        Item={
            'book_name': {'S': book_name},
            'author': {'S': author},
            'pages': {'N': str(pages)},
            'price': {'N': str(price)}
        }
    )
    return jsonify({
        'book_name': {'S': book_name},
        'author': {'S': author},
        'pages': {'N': str(pages)},
        'price': {'N': str(price)}
    })


@app.route("/orders/<string:order_id>")
def get_order_info(order_id):
    resp = client.get_item(
        TableName=ORDERS_TABLE,
        Key={
            'orderId': {'S': order_id}
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'Book does not exist'}), 404

    return jsonify({
        'book_name': item.get('book_name').get('S'),
        'order_id': item.get('orderId').get('S'),
        'UserId': item.get('userId').get('S'),
        'order_date': item.get('order_date').get('S'),
        'delivery_date': item.get('delivery_date').get('S')
    })


@app.route("/orders", methods=['POST'])
def order_books():
    book_name = request.json.get('book_name')
    userId = request.json.get('user_id')
    order_date = datetime.datetime.strftime(datetime.datetime.now(),
                                            '%m-%d-%Y:%H:%M:%S')
    order_id = userId + "@" + order_date
    delivery_date = request.json.get('delivery_date')

    if not book_name or not userId or not delivery_date:
        return jsonify({'error': 'Please provide book_name, user_id and '
                                 'delivery_date'}), 400

    resp = client.put_item(
        TableName=ORDERS_TABLE,
        Item={
            'book_name': {'S': book_name},
            'userId': {'S': userId},
            'order_date': {'S': order_date},
            'orderId': {'S': order_id},
            'delivery_date': {'S': delivery_date}
        }
    )

    return jsonify({
            'book_name': {'S': book_name},
            'userId': {'S': userId},
            'order_date': {'S': order_date},
            'orderId': {'S': order_id},
            'delivery_date': {'S': delivery_date}
        })
