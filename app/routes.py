
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from app.models import db, Product, Order, OrderItem

main = Blueprint("main", __name__)


def obtener_carrito():
    carrito = session.get("cart", {})
    productos = []
    total = 0

    for producto_id, cantidad in carrito.items():
        producto = db.session.get(Product, int(producto_id))

        if producto:
            cantidad = int(cantidad)

            if cantidad > 0:
                subtotal = producto.price * cantidad

                productos.append({
                    "product": producto,
                    "quantity": cantidad,
                    "subtotal": subtotal
                })

                total += subtotal

    return productos, total


@main.app_context_processor
def datos_comunes():
    carrito = session.get("cart", {})

    return {
        "cart_count": sum(
            int(cantidad) for cantidad in carrito.values()
        )
    }


# Página principal: toda la tienda
@main.route("/")
def inicio():
    productos = Product.query.all()

    carrito, total = obtener_carrito()

    categorias = sorted({
        producto.category for producto in productos
    })

    return render_template(
        "index.html",
        products=productos,
        categories=categorias,
        cart_items=carrito,
        cart_total=total
    )


# Agregar productos al carrito
@main.route("/agregar/<int:product_id>", methods=["POST"])
def agregar(product_id):
    producto = db.get_or_404(Product, product_id)

    carrito = session.get("cart", {}).copy()
    clave = str(product_id)

    cantidad = int(carrito.get(clave, 0))

    if cantidad < producto.stock:
        carrito[clave] = cantidad + 1
        session["cart"] = carrito

        flash("Producto agregado al carrito.", "success")
    else:
        flash("No hay unidades disponibles.", "warning")

    return redirect(url_for("main.inicio", _anchor="productos"))


# Actualizar la cantidad
@main.route("/actualizar/<int:product_id>", methods=["POST"])
def actualizar(product_id):
    producto = db.session.get(Product, product_id)

    carrito = session.get("cart", {}).copy()

    cantidad = request.form.get(
        "quantity", default=1, type=int
    )

    if not producto or cantidad <= 0:
        carrito.pop(str(product_id), None)

    elif cantidad <= producto.stock:
        carrito[str(product_id)] = cantidad

    else:
        flash(
            "La cantidad supera el inventario disponible.",
            "warning"
        )

    session["cart"] = carrito

    return redirect(url_for("main.inicio", _anchor="carrito"))


# Eliminar un producto
@main.route("/eliminar/<int:product_id>", methods=["POST"])
def eliminar(product_id):
    carrito = session.get("cart", {}).copy()

    carrito.pop(str(product_id), None)

    session["cart"] = carrito

    flash("Producto eliminado del carrito.", "info")

    return redirect(url_for("main.inicio", _anchor="carrito"))


# Confirmar y guardar un pedido
@main.route("/comprar", methods=["POST"])
def comprar():
    carrito, total = obtener_carrito()

    nombre = request.form.get("name", "").strip()
    correo = request.form.get("email", "").strip().lower()

    if not carrito:
        flash("Tu carrito está vacío.", "warning")
        return redirect(url_for("main.inicio", _anchor="carrito"))

    if not nombre or not correo:
        flash("Completa tu nombre y correo.", "danger")
        return redirect(url_for("main.inicio", _anchor="carrito"))

    # Verificar nuevamente las existencias
    for item in carrito:
        if item["product"].stock < item["quantity"]:
            flash(
                "No hay suficientes unidades de "
                + item["product"].name,
                "warning"
            )

            return redirect(
                url_for("main.inicio", _anchor="carrito")
            )

    pedido = Order(
        customer_name=nombre,
        customer_email=correo,
        total=total
    )

    db.session.add(pedido)

    for item in carrito:
        producto = item["product"]

        producto.stock -= item["quantity"]

        detalle = OrderItem(
            order=pedido,
            product_id=producto.id,
            product_name=producto.name,
            quantity=item["quantity"],
            unit_price=producto.price
        )

        db.session.add(detalle)

    db.session.commit()

    session["cart"] = {}

    flash(
        f"Pedido #{pedido.id} registrado correctamente. "
        "Esta versión no procesa pagos reales.",
        "success"
    )

    return redirect(url_for("main.inicio", _anchor="inicio"))


# Página de error
@main.app_errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("404.html"), 404
