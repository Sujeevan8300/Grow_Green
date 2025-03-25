from flask import Blueprint, render_template, flash , redirect, request, jsonify, Flask
from .models import Product, Cart, Order, Category
from flask_login import login_required, current_user
from . import db

#Crop Recommendation
import numpy as np
import pandas
import sklearn
import pickle


views = Blueprint('views', __name__)


@views.route('/')
def home():
    items = Product.query.filter_by(flash_sale=True).all()
    categories = Category.query.all()
    return render_template('home.html', items=items, categories=categories, cart=Cart.query.filter_by(customer_link=current_user.id).all() 
                           if current_user.is_authenticated else [])




@views.route('/add-to-cart/<int:item_id>')
@login_required
def add_to_cart(item_id):
    item_to_add = Product.query.get(item_id)
    item_exists = Cart.query.filter_by(product_link=item_id, customer_link=current_user.id).first()
    if item_exists:
        try:
            item_exists.quantity = item_exists.quantity + 1
            db.session.commit()
            flash(f' Quantity of { item_exists.product.product_name } has been updated')
            return redirect(request.referrer)
        except Exception as e:
            print('Quantity not Updated', e)
            flash(f'Quantity of { item_exists.product.product_name } not updated')
            return redirect(request.referrer)

    new_cart_item = Cart()
    new_cart_item.quantity = 1
    new_cart_item.product_link = item_to_add.id
    new_cart_item.customer_link = current_user.id

    try:
        db.session.add(new_cart_item)
        db.session.commit()
        flash(f'{new_cart_item.product.product_name} added to cart')
    except Exception as e:
        print('Item not added to cart', e)
        flash(f'{new_cart_item.product.product_name} has not been added to cart')

    return redirect(request.referrer)


@views.route('/cart')
@login_required
def show_cart():
    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    amount = 0
    for item in cart:
        amount += item.product.current_price * item.quantity

    return render_template('cart.html', cart=cart, amount=amount, total=amount+100)

@views.route('/pluscart')
@login_required
def plus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity = cart_item.quantity + 1
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()

        amount = 0

        for item in cart:
            amount += item.product.current_price * item.quantity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        }

        return jsonify(data)
    


@views.route('/minuscart')
@login_required
def minus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity = cart_item.quantity - 1
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()

        amount = 0

        for item in cart:
            amount += item.product.current_price * item.quantity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        }

        return jsonify(data)
    


@views.route('removecart')
@login_required
def remove_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        db.session.delete(cart_item)
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()

        amount = 0

        for item in cart:
            amount += item.product.current_price * item.quantity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        }

        return jsonify(data)
    

@views.route('/place-order', methods=['GET', 'POST'])
@login_required
def place_order():
    if request.method == 'POST':
        delivery_address = request.form.get('delivery_address')
        customer_cart = Cart.query.filter_by(customer_link=current_user.id)
        
        if customer_cart:
            try:
                total = 0
                for item in customer_cart:
                    total += item.product.current_price * item.quantity

                # Create orders for Cash on Delivery
                for item in customer_cart:
                    new_order = Order()
                    new_order.quantity = item.quantity
                    new_order.price = item.product.current_price
                    new_order.status = 'Pending (Cash on Delivery)'  # Status for COD
                    new_order.payment_id = item.id
                    new_order.product_link = item.product_link
                    new_order.customer_link = item.customer_link
                    new_order.delivery_address = delivery_address  # Save the address

                    db.session.add(new_order)

                    # Update product stock
                    product = Product.query.get(item.product_link)
                    product.in_stock -= item.quantity

                    # Remove item from cart
                    db.session.delete(item)

                db.session.commit()

                flash('Order placed successfully.')
                return redirect('/orders')
            except Exception as e:
                print(e)
                flash('Order not placed.')
                return redirect('/')
        else:
            flash('Your cart is empty.')
            return redirect('/')
    else:
        return redirect('/')




@views.route('/orders')
@login_required
def order():
    orders = Order.query.filter_by(customer_link=current_user.id).all()
    return render_template('orders.html', orders=orders)



@views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search')
        items = Product.query.filter(Product.product_name.ilike(f'%{search_query}%')).all()
        return render_template('search.html', items=items, cart=Cart.query.filter_by(customer_link=current_user.id).all()
                           if current_user.is_authenticated else [])

    return render_template('search.html')


@views.route('/delete-order/<int:order_id>', methods=['POST'])
@login_required
def delete_order(order_id):
    order = Order.query.get(order_id)
    
    if order:
        try:
            db.session.delete(order)
            db.session.commit()
            flash('Order deleted successfully', 'success')
        except Exception as e:
            flash('Error occurred while deleting the order', 'danger')
            db.session.rollback()
    else:
        flash('Order not found', 'danger')

    return redirect('/view-orders') # Redirect back to the orders page



#Crop Recommendation System
@views.route('/crop_recommendation')
def crop_recommendation():
    return render_template('crop_recommendation.html')

model = pickle.load(open('model.pkl','rb'))
sc = pickle.load(open('standscaler.pkl','rb'))
mx = pickle.load(open('minmaxscaler.pkl','rb'))

@views.route("/predict",methods=['POST'])
def predict():
    N = request.form['Nitrogen']
    P = request.form['Phosporus']
    K = request.form['Potassium']
    temp = request.form['Temperature']
    humidity = request.form['Humidity']
    ph = request.form['pH']
    rainfall = request.form['Rainfall']

    feature_list = [N, P, K, temp, humidity, ph, rainfall]
    single_pred = np.array(feature_list).reshape(1, -1)

    mx_features = mx.transform(single_pred)
    sc_mx_features = sc.transform(mx_features)
    prediction = model.predict(sc_mx_features)

    crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                 8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                 14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                 19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}

    if prediction[0] in crop_dict:
        crop = crop_dict[prediction[0]]
        result = "{} is the best crop to be cultivated right there".format(crop)
    else:
        result = "Sorry, we could not determine the best crop to be cultivated with the provided data."
    return render_template('crop_recommendation.html',result = result)



@views.route('/category/<int:category_id>')
def category_page(category_id):
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category.id).all()
    return render_template('category.html', category=category, products=products, 
                           cart=Cart.query.filter_by(customer_link=current_user.id).all() if current_user.is_authenticated else [])



