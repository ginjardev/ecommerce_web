from .models import Product, Cart,Order
from flask_login import login_required, current_user
from flask import Blueprint, render_template, flash, redirect, request, jsonify
from . import db
from intasend import APIService

views = Blueprint('views', __name__)

API_PUBLISHABLE_KEY = 'ISPubKey_test_e005a552-9557-4ee5-b2a2-414656a6193f'
API_TOKEN = 'ISSecretKey_test_202da626-23bb-4715-875e-2b5b3ceb83ce'
PAYLINK = 'https://sandbox.intasend.com/pay/d27c15a8-bd40-47d4-b0b4-d739a95b462d/'

@views.route("/")
def home():
    items = Product.query.filter_by(flash_sale=True)

    return render_template("home.html", items = items, cart = Cart.query.filter_by(customer_link=current_user.id).all()
                           if current_user.is_authenticated else []) 



@views.route("/add-to-cart/<int:item_id>")
@login_required
def add_to_cart(item_id):
    item_to_add = Product.query.get(item_id)
    item_exists = Cart.query.filter_by(product_link=item_id, customer_link=current_user.id).first()
    if item_exists:
        try:
            item_exists.quantity += item_exists.quantity + 1
            db.session.commit()
            flash(f'Quantity of {item_to_add.product_name} updated.')
            return redirect(request.referrer)
        except Exception as e:
            print( 'Quantity not updated', e)
            flash(f'Quantity of {item_to_add.product_name} not updated.')
            return redirect(request.referrer)
        
    new_cart_item = Cart()
    new_cart_item.quantity = 1
    new_cart_item.product_link = item_to_add.id
    new_cart_item.customer_link = current_user.id

    try:
        db.session.add(new_cart_item)
        db.session.commit()
        flash(f'{new_cart_item.product_name} added to cart.')
    except Exception as e:
        print('Item not added to cart', e)
        flash(f'{new_cart_item.product.product_name} not added to cart.')

    return redirect(request.referrer)


@views.route('/cart')
@login_required
def show_cart():
    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    amount = 0
    for item in cart:
        amount += item.product.current_price  * item.quantity

    return render_template('cart.html', cart=cart, amount=amount, total=amount+200)


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
        cart_item.quantity = cart_item.quantity - 1 if cart_item.quantity > 1 else 1
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


@views.route('/removecart')
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
            amount += item.product.current_price * item.quamtity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        }

        jsonify(data)


@views.route('/place-order')
@login_required
def place_order():
    customer_cart = Cart.query.filter_by(customer_link=current_user.id)
    if customer_cart:
        try:
            total = 0
            for item in customer_cart:
                total += item.product.current_price * item.quantity

            service = APIService(publishable_key=API_PUBLISHABLE_KEY, token=API_TOKEN, test=True)
            create_order_response = service.collect.mpesa_stk_push(phone_number='254708374149', email=current_user.email, amount=total + 200, currency='USD',narrative='Order from E-commerce Website')


            for item in customer_cart:
                new_order = Order()
                new_order.quantity = item.quantity
                new_order.price = item.product.current_price 
                new_order.status = create_order_response['invoice']['state'].capitalize()
                new_order.payment_id = create_order_response['id']
                new_order.product_link = item.product_link
                new_order.customer_link = item.customer_link

                db.session.add(new_order)

                product = Product.query.get(item.product_link)
                product.in_stock = product.in_stock - item.quantity

                db.session.delete(item)

                db.session.commit()

                flash('Order placed successfully.')

                return "Order has been placed"
        except Exception as e:
            print(e)
            flash('Order not placed.')
            return redirect('/')
    else:
        flash('Your cart is empty.')
        return redirect('/')
