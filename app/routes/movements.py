import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..models import ProductMovement, Product, Location, db
from ..forms import MovementForm
from sqlalchemy import func, case, text  # ✅ added text

bp = Blueprint('movements', __name__, url_prefix='/movements')

@bp.route('/')
def list_movements():
    movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    return render_template('movements.html', movements=movements)

def _populate_choices(form):
    products = Product.query.order_by(Product.product_id).all()
    product_choices = [(p.product_id, f'{p.product_id} - {p.name}') for p in products]
    form.product_id.choices = product_choices

    locations = Location.query.order_by(Location.location_id).all()
    loc_choices = [('', '---')]
    loc_choices += [(l.location_id, f'{l.location_id} - {l.name}') for l in locations]
    form.from_location.choices = loc_choices
    form.to_location.choices = loc_choices

@bp.route('/create', methods=['GET', 'POST'])
def create_movement():
    form = MovementForm()
    _populate_choices(form)
    if form.validate_on_submit():
        movement_id = form.movement_id.data.strip() if form.movement_id.data and form.movement_id.data.strip() else str(uuid.uuid4())
        from_loc = form.from_location.data or None
        to_loc = form.to_location.data or None

        if from_loc == '':
            from_loc = None
        if to_loc == '':
            to_loc = None

        # basic validation: cannot have both from and to None
        if from_loc is None and to_loc is None:
            flash('Either From or To location must be provided.', 'danger')
        else:
            m = ProductMovement(
                movement_id=movement_id,
                product_id=form.product_id.data,
                from_location_id=from_loc,
                to_location_id=to_loc,
                qty=form.qty.data
            )
            db.session.add(m)
            db.session.commit()
            flash('Movement recorded.', 'success')
            return redirect(url_for('movements.list_movements'))
    return render_template('movement_form.html', form=form, action='Create')

@bp.route('/report')
def balance_report():
    # Use raw SQL logic via SQLAlchemy expressions:
    # For each product-location pair, balance = sum(to where loc) - sum(from where loc)
    sql = """
    SELECT p.product_id, l.location_id,
      COALESCE(SUM(CASE WHEN pm.to_location_id = l.location_id THEN pm.qty ELSE 0 END), 0)
      - COALESCE(SUM(CASE WHEN pm.from_location_id = l.location_id THEN pm.qty ELSE 0 END), 0) AS qty
    FROM product p
    CROSS JOIN location l
    LEFT JOIN product_movement pm
      ON pm.product_id = p.product_id
    GROUP BY p.product_id, l.location_id
    ORDER BY p.product_id, l.location_id;
    """

    # ✅ fix: wrap SQL in text()
    res = db.session.execute(text(sql)).fetchall()

    # Convert to list of dicts
    report = [{'product_id': r[0], 'location_id': r[1], 'qty': r[2]} for r in res]
    # Filter non-zero balances
    non_zero = [r for r in report if r['qty'] != 0]

    return render_template('balance_report.html', all_report=report)

