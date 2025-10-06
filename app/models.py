from datetime import datetime
from . import db

class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)


    movements = db.relationship('ProductMovement', back_populates='product', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Product {self.product_id} - {self.name}>'

class Location(db.Model):
    __tablename__ = 'location'
    location_id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    movements_from = db.relationship('ProductMovement', foreign_keys='ProductMovement.from_location_id', back_populates='from_location')
    movements_to = db.relationship('ProductMovement', foreign_keys='ProductMovement.to_location_id', back_populates='to_location')

    def __repr__(self):
        return f'<Location {self.location_id} - {self.name}>'

class ProductMovement(db.Model):
    __tablename__ = 'product_movement'
    movement_id = db.Column(db.String(64), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    from_location_id = db.Column(db.String(64), db.ForeignKey('location.location_id'), nullable=True)
    to_location_id = db.Column(db.String(64), db.ForeignKey('location.location_id'), nullable=True)
    product_id = db.Column(db.String(64), db.ForeignKey('product.product_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    product = db.relationship('Product', back_populates='movements')
    from_location = db.relationship('Location', foreign_keys=[from_location_id], back_populates='movements_from')
    to_location = db.relationship('Location', foreign_keys=[to_location_id], back_populates='movements_to')

    def __repr__(self):
        return f'<Movement {self.movement_id} P:{self.product_id} {self.qty}>'
