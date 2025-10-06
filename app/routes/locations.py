from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..models import Location
from ..forms import LocationForm
from .. import db

bp = Blueprint('locations', __name__, url_prefix='/locations')

@bp.route('/')
def list_locations():
    locations = Location.query.order_by(Location.location_id).all()
    return render_template('locations.html', locations=locations)

@bp.route('/create', methods=['GET', 'POST'])
def create_location():
    form = LocationForm()
    if form.validate_on_submit():
        existing = Location.query.get(form.location_id.data)
        if existing:
            flash('Location ID already exists.', 'danger')
        else:
            l = Location(location_id=form.location_id.data.strip(), name=form.name.data.strip())
            db.session.add(l)
            db.session.commit()
            flash('Location created.', 'success')
            return redirect(url_for('locations.list_locations'))
    return render_template('location_form.html', form=form, action='Create')

@bp.route('/edit/<location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    l = Location.query.get_or_404(location_id)
    form = LocationForm(obj=l)
    if form.validate_on_submit():
        l.name = form.name.data.strip()
        db.session.commit()
        flash('Location updated.', 'success')
        return redirect(url_for('locations.list_locations'))
    return render_template('location_form.html', form=form, action='Edit', edit=True)

@bp.route('/delete/<location_id>', methods=['POST'])
def delete_location(location_id):
    l = Location.query.get_or_404(location_id)
    db.session.delete(l)
    db.session.commit()
    flash('Location deleted.', 'success')
    return redirect(url_for('locations.list_locations'))
