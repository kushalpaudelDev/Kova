from flask import Flask, render_template, session, redirect, url_for, request, jsonify

app = Flask(__name__)
app.secret_key = "shopkey123"

PRODUCTS = [
    {"id": 1, "name": "Leather Tote Bag", "price": 89.99, "category": "Bags", "image": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&q=80", "badge": "Bestseller"},
    {"id": 2, "name": "Minimalist Watch", "price": 149.00, "category": "Accessories", "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&q=80", "badge": "New"},
    {"id": 3, "name": "Canvas Sneakers", "price": 65.00, "category": "Footwear", "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&q=80", "badge": None},
    {"id": 4, "name": "Wool Sweater", "price": 120.00, "category": "Clothing", "image": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400&q=80", "badge": "Sale"},
    {"id": 5, "name": "Ceramic Mug Set", "price": 38.00, "category": "Home", "image": "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=400&q=80", "badge": None},
    {"id": 6, "name": "Linen Trousers", "price": 95.00, "category": "Clothing", "image": "https://images.unsplash.com/photo-1594938298603-c8148c4b4d2e?w=400&q=80", "badge": "New"},
    {"id": 7, "name": "Bamboo Sunglasses", "price": 54.00, "category": "Accessories", "image": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400&q=80", "badge": None},
    {"id": 8, "name": "Silk Scarf", "price": 72.00, "category": "Accessories", "image": "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=400&q=80", "badge": "Bestseller"},
]

def get_cart():
    return session.get("cart", {})

def cart_count():
    cart = get_cart()
    return sum(item["qty"] for item in cart.values())

def cart_total():
    cart = get_cart()
    return sum(item["price"] * item["qty"] for item in cart.values())

@app.context_processor
def inject_cart():
    return {"cart_count": cart_count(), "cart_total": round(cart_total(), 2)}

@app.route("/")
def index():
    category = request.args.get("category", "All")
    categories = ["All"] + sorted(set(p["category"] for p in PRODUCTS))
    filtered = PRODUCTS if category == "All" else [p for p in PRODUCTS if p["category"] == category]
    return render_template("index.html", products=filtered, categories=categories, active=category)

@app.route("/product/<int:pid>")
def product(pid):
    p = next((x for x in PRODUCTS if x["id"] == pid), None)
    if not p:
        return redirect(url_for("index"))
    related = [x for x in PRODUCTS if x["category"] == p["category"] and x["id"] != pid][:3]
    return render_template("product.html", product=p, related=related)

@app.route("/cart")
def cart():
    items = get_cart()
    return render_template("cart.html", items=items, total=round(cart_total(), 2))

@app.route("/add/<int:pid>", methods=["POST"])
def add_to_cart(pid):
    p = next((x for x in PRODUCTS if x["id"] == pid), None)
    if not p:
        return jsonify({"error": "Not found"}), 404
    cart = get_cart()
    key = str(pid)
    if key in cart:
        cart[key]["qty"] += 1
    else:
        cart[key] = {"name": p["name"], "price": p["price"], "image": p["image"], "qty": 1}
    session["cart"] = cart
    return jsonify({"count": cart_count(), "total": round(cart_total(), 2)})

@app.route("/remove/<int:pid>", methods=["POST"])
def remove_from_cart(pid):
    cart = get_cart()
    cart.pop(str(pid), None)
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/update/<int:pid>", methods=["POST"])
def update_cart(pid):
    qty = int(request.form.get("qty", 1))
    cart = get_cart()
    key = str(pid)
    if key in cart:
        if qty <= 0:
            cart.pop(key)
        else:
            cart[key]["qty"] = qty
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/checkout")
def checkout():
    session["cart"] = {}
    return render_template("checkout.html")

if __name__ == "__main__":
    app.run(debug=True)
