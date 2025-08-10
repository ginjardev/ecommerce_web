from .models import Product, Cart
from flask_login import login_required, current_user
from flask import Blueprint, render_template, flash, redirect

views = Blueprint('views', __name__)

@views.route("/")
def home():
    items = Product.query.filter_by(flash_sale=True)

    return render_template("home.html", items = items) 



@views.route("/add-to-cart/<int:item_id>")
@login_required
def add_to_cart(item_id):
    item_to_add = Product.query.get(item_id)
    item_exists = Cart.query.filter_by(product_link=item_id, customer_link=current_user).first()
    if item_exists:
        try:
            item_exists.quantity = item_exists.quantity + 1
