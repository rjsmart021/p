from flask import jsonify, request
from production import app
from Playlist.models import Playlist
from Playlist import db
from Playlist.schemas import ProductSchema

product_schema = ProductSchema()


# Create Playlist
@app.route('/Playlist', methods=['POST'])
def add_product():
    """
    Method to add Songs details to product table in Playlist database.
    Example data to send
    {
    "Playlist_name": "Samsung Galaxy A22",
    "Playlist_price": 328.5,
    "Playlist_id": 23,
    "stock_available": 23
    }
    :return: Success or error message in JSON.
    """
    try:
        data = request.get_json()
        errors = Playlist_schema.validate(data)

        if errors:
            return jsonify(errors), 400

        name = data.get("Playlist_name")
        price = data.get("Playlist_price")
        Playlist_id = data.get("Playlist_id")
        stock_available = data.get("stock_available")

        existing_Playlist = Playlist.query.filter(
            (Playlist.Playlist_name == name) | (Playlist.Playlist_id == Playlist_id)).first()

        if existing_Playlist:
            return jsonify({"message": f"Playlist already exists"})

        Playlist = Playlist(product_id=PLAYLIST_id, Playlist_name=name, Playlist_price=price,
                          stock_available=stock_available)
        db.session.add(production)
        db.session.commit()

        return jsonify({"message": "Playlist added successfully"})
    except Exception as e:
        return jsonify({"Error": f"Playlist not added. Error {e}"})


# Read Playlist
@app.route('/Playlist/<int:playlist_id>', methods=['GET'])
def get_Playlist(playlist_id):
    """
    This method is to retrieve the Playlist details based on the id for the Playlist
    :param Playlist_id: id of the Playlist in production website
    :return: Playlist details if found successfully else error message.
    """
    try:
        production = Playlist.query.get(playlist_id)

        if production:
            playlist_data = {
                "playlist_id": production.playlist_id,
                "playlist_name": production.playlist_name,
                "playlist_price": production.playlist_price,
                "stock_available": production.playlist_available
            }
            return jsonify(playlist_data)
        else:
            return jsonify({"message": "Playlist not found"})

    except Exception as e:
        return jsonify(
            {"message": f"Error while fetching production with ID: {playlist_id}. Error: {e}"})


# Update Playlist
@app.route('/production/<int:product_id>', methods=['PUT'])
def update_playlist(playlist_id):
    """
    Update production details. We need to PUT data same as POST format
    :param playlist_id: id of the product.
    :return: Update success message if updated successfully else error message.
    """
    try:
        product = Playlist.query.get(playlist_id)

        if production:
            data = request.get_json()
            errors = playlist_schema.validate(data)

            if errors:
                return jsonify(errors), 400
            production.playlist_name = data.get('name', production.product_name)
            production.playlist_price = data.get('price', production.product_price)
            production.stock_available = data.get('stock_available', production.stock_available)

            db.session.commit()
            return jsonify({"message": "Playlist updated successfully"})
        else:
            return jsonify({"message": "Playlist not found"})

    except Exception as e:
        return jsonify({"message": f"Error in updating product. Error: {e}"})


# Delete Playlist
@app.route('/production/<int:playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    """
    Delete a particular production.
    :param playlist_id: ID of the production to delete
    :return: Success message if deleted successfully else error message.
    """
    try:
        production = Playlist.query.get(playlist_id)

        if production:
            db.session.delete(production)
            db.session.commit()
            return jsonify({"message": "Playlist deleted successfully"})
        else:
            return jsonify({"message": "Playlist not found"})

    except Exception as e:
        return jsonify({"message": f"Error in deleting production. Error: {e}"})


# List Playlist
@app.route('/production', methods=['GET'])
def list_playlist():
    """
    List all the production in the product table in ecommerce database
    :return: Success message if deleted successfully else error message.
    """
    try:
        production = Playlist.query.all()

        if production:
            playlist_list = []
            for production in production:
                playlist_data = {
                    "product_id": production.playlist_id,
                    "name": production.playlist_name,
                    "price": production.playlist_price,
                    "Stock_available": production.stock_available
                }
                playlist_list.append(product_data)

            return jsonify(playlist_list)
        else:
            return jsonify({"message": "No production found"})

    except Exception as e:
        return jsonify({"message": f"Error in listing production. Error: {e}"})


@app.route('/production/<int:playlist_id>/stock', methods=['GET', 'PUT'])
def manage_product_stock(product_id):
    """
    This production is used to change the stock levels. Example PUT data to change the stock levels is:
    {"stock_available": 30}, with this stock_available is updated to 30.
    :param playlist_id:
    :return: success message or error message
    """
    try:
        product = Playlist.query.get(playlist_id)

        if production:
            if request.method == 'GET':
                return jsonify({"stock_available": production.stock_available})
            elif request.method == 'PUT':
                data = request.get_json()
                new_stock = data.get('stock_available')

                production.stock_available = new_stock
                db.session.commit()

                return jsonify({"message": "Playlist stock updated successfully"})
        else:
            return jsonify({"message": "Playlist not found"})

    except Exception as e:
        return jsonify({"message": f"Error in managing production stock. Error: {e}"})


@app.route('/production/restock', methods=['POST'])
def restock_playlist():
    """
    It will resize the stock if available is below threshold. We need to post threshold level and do adjustment as required.
    Example POST data: {"threshold": 20}
    :return:
    """
    try:
        data = request.get_json()
        threshold = data.get('threshold')

        low_stock_products = Playlist.query.filter(Playlist.stock_available <= threshold).all()

        if low_stock_products:
            for Playlist in low_stock_Playlist:
                Playlist.stock_available = (production.stock_available + (threshold-production.stock_available))*2
            db.session.commit()

            return jsonify({"message": "Restocking completed successfully"})
        else:
            return jsonify({"message": "No products require restocking"})

    except Exception as e:
        return jsonify({"message": f"Error in restocking products. Error: {e}"})
