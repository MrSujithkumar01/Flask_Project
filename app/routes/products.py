from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..models import Product
from ..forms import ProductForm
from .. import db

bp = Blueprint('products', __name__, url_prefix='/products')

@bp.route('/')
def list_products():
    products = Product.query.order_by(Product.product_id).all()
    return render_template('products.html', products=products)

@bp.route('/create', methods=['GET', 'POST'])
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        existing = Product.query.get(form.product_id.data)
        if existing:
            flash('Product ID already exists.', 'danger')
        else:
            p = Product(product_id=form.product_id.data.strip(), name=form.name.data.strip(), quantity=form.quantity.data)
            db.session.add(p)
            db.session.commit()
            flash('Product created.', 'success')
            return redirect(url_for('products.list_products'))
    return render_template('product_form.html', form=form, action='Create')

@bp.route('/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    p = Product.query.get_or_404(product_id)
    form = ProductForm(obj=p)
    if form.validate_on_submit():
        p.name = form.name.data.strip()
        p.quantity = form.quantity.data
        db.session.commit()
        flash('Product updated.', 'success')
        return redirect(url_for('products.list_products'))
    return render_template('product_form.html', form=form, action='Edit', edit=True)

@bp.route('/delete/<product_id>', methods=['POST'])
def delete_product(product_id):
    p = Product.query.get_or_404(product_id)
    db.session.delete(p)
    db.session.commit()
    flash('Product deleted.', 'success')
    return redirect(url_for('products.list_products'))
