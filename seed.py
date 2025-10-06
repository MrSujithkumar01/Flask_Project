from app import create_app, db
from app.models import Product, Location, ProductMovement
from uuid import uuid4
from random import choice, randint
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    db.create_all()
    # Clear existing
    ProductMovement.query.delete()
    Product.query.delete()
    Location.query.delete()
    db.session.commit()

    # Add products
    products = [
        Product(product_id='P001', name='Widget A', description='Basic widget'),
        Product(product_id='P002', name='Widget B', description='Advanced widget'),
        Product(product_id='P003', name='Gadget X', description='Gadget'),
    ]
    db.session.add_all(products)

    # Add locations
    locations = [
        Location(location_id='L001', name='Warehouse 1'),
        Location(location_id='L002', name='Warehouse 2'),
        Location(location_id='L003', name='Outlet'),
    ]
    db.session.add_all(locations)
    db.session.commit()

    prod_ids = [p.product_id for p in products]
    loc_ids = [l.location_id for l in locations]

    # Create movements: inbound, outbound, transfers
    movements = []
    for i in range(20):
        pid = choice(prod_ids)
        t = randint(0, 2)
        if t == 0:
            # inbound
            mv = ProductMovement(
                movement_id=str(uuid4()),
                product_id=pid,
                from_location_id=None,
                to_location_id=choice(loc_ids),
                qty=randint(5, 20),
                timestamp=datetime.utcnow() - timedelta(days=randint(0,10), hours=randint(0,23))
            )
        elif t == 1:
            # outbound
            mv = ProductMovement(
                movement_id=str(uuid4()),
                product_id=pid,
                from_location_id=choice(loc_ids),
                to_location_id=None,
                qty=randint(1, 10),
                timestamp=datetime.utcnow() - timedelta(days=randint(0,10), hours=randint(0,23))
            )
        else:
            a = choice(loc_ids)
            b = choice(loc_ids)
            if b == a:
                b = loc_ids[(loc_ids.index(a) + 1) % len(loc_ids)]
            mv = ProductMovement(
                movement_id=str(uuid4()),
                product_id=pid,
                from_location_id=a,
                to_location_id=b,
                qty=randint(1, 8),
                timestamp=datetime.utcnow() - timedelta(days=randint(0,10), hours=randint(0,23))
            )
        movements.append(mv)

    db.session.add_all(movements)
    db.session.commit()
    print('Seed complete.')
