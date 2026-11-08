from flask import Flask
from config import Config
from app.models import db, Product


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

        # Productos de ejemplo para la tienda
        if Product.query.count() == 0:
            productos = [
                Product(
                    name="Camiseta básica",
                    category="Ropa",
                    description="Camiseta cómoda para todos los días.",
                    price=35000,
                    stock=20,
                    image=""
                ),
                Product(
                    name="Mochila urbana",
                    category="Accesorios",
                    description="Ideal para estudiar y salir.",
                    price=78000,
                    stock=12,
                    image=""
                ),
                Product(
                    name="Botella reutilizable",
                    category="Accesorios",
                    description="Lleva tu bebida favorita.",
                    price=25000,
                    stock=30,
                    image=""
                ),
                Product(
                    name="Audífonos inalámbricos",
                    category="Tecnología",
                    description="Disfruta tu música donde quieras.",
                    price=65000,
                    stock=15,
                    image=""
                )
            ]

            db.session.add_all(productos)
            db.session.commit()

    return app
